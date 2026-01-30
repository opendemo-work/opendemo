# 生产环境成本优化指南

## 1. 资源规划与优化

### 1.1 实例类型选择策略

```yaml
# 成本优化的节点池配置
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: ml-training-cluster
  region: us-west-2
managedNodeGroups:
- name: spot-training-nodes
  instanceTypes: ["p3dn.24xlarge", "p3.16xlarge", "p2.16xlarge"]
  spot: true
  minSize: 0
  maxSize: 20
  desiredCapacity: 2
  volumeSize: 100
  volumeType: gp3
  labels:
    node-group: spot-training
    cost-optimized: "true"
  taints:
    - key: spot-instance
      value: "true"
      effect: NoSchedule

- name: on-demand-training-nodes
  instanceTypes: ["p3.8xlarge", "p3.2xlarge"]
  spot: false
  minSize: 1
  maxSize: 5
  desiredCapacity: 1
  volumeSize: 200
  volumeType: io2
  labels:
    node-group: on-demand-training
    cost-optimized: "false"
```

### 1.2 自动扩缩容配置

```yaml
# KEDA + Prometheus自动扩缩容
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: training-job-scaler
  namespace: production-training
spec:
  scaleTargetRef:
    name: training-deployment
  pollingInterval: 30
  cooldownPeriod: 300
  minReplicaCount: 0
  maxReplicaCount: 10
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus-server.monitoring.svc:8080
      metricName: training_queue_length
      threshold: '5'
      query: sum(kube_job_status_active{job="training-jobs"})
```

## 2. 存储成本优化

### 2.1 分层存储策略

```yaml
# 不同性能等级的StorageClass
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: training-fast-ssd
provisioner: kubernetes.io/aws-ebs
parameters:
  type: io2
  iopsPerGB: "50"
  fsType: ext4
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: training-standard
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  fsType: ext4
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: training-archive
provisioner: kubernetes.io/aws-ebs
parameters:
  type: st1
  fsType: ext4
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```

### 2.2 数据生命周期管理

```python
# 数据生命周期管理脚本
import boto3
import datetime

class DataLifecycleManager:
    def __init__(self, bucket_name):
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name
    
    def apply_lifecycle_policy(self):
        """应用生命周期策略"""
        lifecycle_config = {
            'Rules': [
                {
                    'ID': 'MoveToInfrequentAccess',
                    'Status': 'Enabled',
                    'Filter': {'Prefix': 'training-data/'},
                    'Transitions': [
                        {
                            'Days': 30,
                            'StorageClass': 'STANDARD_IA'
                        },
                        {
                            'Days': 90,
                            'StorageClass': 'GLACIER'
                        }
                    ],
                    'Expiration': {
                        'Days': 365
                    }
                }
            ]
        }
        
        self.s3_client.put_bucket_lifecycle_configuration(
            Bucket=self.bucket_name,
            LifecycleConfiguration=lifecycle_config
        )
    
    def cleanup_old_checkpoints(self, days_old=7):
        """清理旧的检查点"""
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_old)
        
        paginator = self.s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=self.bucket_name, Prefix='checkpoints/')
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    if obj['LastModified'] < cutoff_date:
                        self.s3_client.delete_object(
                            Bucket=self.bucket_name,
                            Key=obj['Key']
                        )
                        print(f"Deleted: {obj['Key']}")

# 使用示例
manager = DataLifecycleManager('ml-training-bucket')
manager.apply_lifecycle_policy()
manager.cleanup_old_checkpoints()
```

## 3. 训练成本监控

### 3.1 成本监控仪表板

```yaml
# Grafana成本监控面板
apiVersion: integreatly.org/v1alpha1
kind: GrafanaDashboard
metadata:
  name: training-cost-dashboard
  namespace: monitoring
spec:
  json: |
    {
      "dashboard": {
        "title": "ML Training Cost Analytics",
        "panels": [
          {
            "title": "Hourly Training Cost",
            "type": "graph",
            "targets": [
              {
                "expr": "sum by (job_name) (rate(aws_billing_cost_estimate_usd[1h]))",
                "legendFormat": "{{job_name}}"
              }
            ]
          },
          {
            "title": "Resource Utilization Efficiency",
            "type": "table",
            "targets": [
              {
                "expr": "avg by (pod) (container_cpu_usage_seconds_total) / avg by (pod) (kube_pod_container_resource_requests{resource=\"cpu\"})",
                "legendFormat": "CPU Efficiency"
              }
            ]
          },
          {
            "title": "Cost Per Model Trained",
            "type": "stat",
            "targets": [
              {
                "expr": "sum(aws_billing_cost_estimate_usd) / count(kube_job_completion_time_seconds)",
                "legendFormat": "Average Cost Per Training"
              }
            ]
          }
        ]
      }
    }
```

### 3.2 预算告警配置

```yaml
# 成本预算告警
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: training-cost-alerts
  namespace: monitoring
spec:
  groups:
  - name: training.cost.rules
    rules:
    - alert: HighTrainingCost
      expr: rate(aws_billing_cost_estimate_usd[1h]) > 10
      for: 15m
      labels:
        severity: warning
      annotations:
        summary: "High training cost detected"
        description: "Current hourly training cost is {{ $value }} USD"
    
    - alert: BudgetExceeded
      expr: sum(aws_billing_cost_estimate_usd) > 1000
      for: 1m
      labels:
        severity: critical
      annotations:
        summary: "Monthly budget exceeded"
        description: "Total training cost has exceeded $1000 this month"
```

## 4. 优化最佳实践

### 4.1 训练效率优化

```python
# 训练效率优化配置
class TrainingOptimizer:
    def __init__(self):
        self.optimizations = {
            'mixed_precision': True,
            'gradient_accumulation': 4,
            'prefetch_factor': 2,
            'num_workers': 4,
            'pin_memory': True
        }
    
    def calculate_cost_savings(self, baseline_hours, optimized_hours, hourly_rate):
        """计算成本节约"""
        baseline_cost = baseline_hours * hourly_rate
        optimized_cost = optimized_hours * hourly_rate
        savings = baseline_cost - optimized_cost
        savings_percentage = (savings / baseline_cost) * 100
        
        return {
            'baseline_cost': baseline_cost,
            'optimized_cost': optimized_cost,
            'savings': savings,
            'savings_percentage': savings_percentage
        }

# 优化前后对比
optimizer = TrainingOptimizer()
results = optimizer.calculate_cost_savings(
    baseline_hours=100,  # 基线100小时
    optimized_hours=60,   # 优化后60小时
    hourly_rate=8.0       # 每小时$8
)

print(f"成本节约: ${results['savings']:.2f} ({results['savings_percentage']:.1f}%)")
```

这套完整的成本优化方案可以帮助您：
✅ 降低30-50%的训练成本
✅ 提高资源利用效率
✅ 建立完善的成本监控体系
✅ 实现自动化的成本控制
