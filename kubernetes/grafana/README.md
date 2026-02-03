# Grafana 可视化平台演示

## 🎯 概述

Grafana是领先的开源可视化和分析平台，专门用于监控和可观测性。本演示展示了如何在Kubernetes环境中部署Grafana，并创建专业的监控仪表板。

## 🏗️ 组件架构

### 核心功能
- **主要用途**: 数据可视化和监控仪表板
- **技术栈**: Grafana + Prometheus数据源
- **部署方式**: Helm Chart部署

### 数据流向
```mermaid
graph LR
    A[Prometheus] --> B[Grafana]
    C[Loki] --> B
    D[Tempo] --> B
    B --> E[Dashboard UI]
```

## 🚀 部署指南

### 独立部署Grafana
```bash
# 添加Grafana Helm仓库
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# 部署Grafana
helm install grafana grafana/grafana \
  --namespace monitoring \
  --set adminPassword=admin123 \
  --set persistence.enabled=true \
  --set persistence.size=10Gi
```

### 配置数据源
```bash
# 获取Grafana密码
kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

# 端口转发访问
kubectl port-forward -n monitoring svc/grafana 3000:80
# 访问 http://localhost:3000 用户名: admin 密码: 上述获取的密码
```

## 📁 配置文件

### 数据源配置
```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus-prometheus.monitoring:9090
    access: proxy
    isDefault: true
  - name: Loki
    type: loki
    url: http://loki.monitoring:3100
    access: proxy
```

### 仪表板配置
```yaml
apiVersion: 1
providers:
  - name: 'default'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    editable: true
    options:
      path: /var/lib/grafana/dashboards
```

## 🔧 核心功能演示

### 功能1: 创建监控仪表板
```bash
# 创建示例仪表板配置
cat > dashboard-example.yaml << EOF
{
  "dashboard": {
    "id": null,
    "title": "Kubernetes Cluster Overview",
    "tags": ["kubernetes", "overview"],
    "timezone": "browser",
    "panels": [
      {
        "type": "graph",
        "title": "CPU Usage",
        "targets": [
          {
            "expr": "sum(rate(container_cpu_usage_seconds_total[5m])) by (pod)",
            "legendFormat": "{{pod}}"
          }
        ]
      }
    ]
  },
  "folderId": 0,
  "overwrite": false
}
EOF

# 应用仪表板
curl -X POST \
  -H "Content-Type: application/json" \
  -d @dashboard-example.yaml \
  http://admin:admin123@localhost:3000/api/dashboards/db
```

### 功能2: 配置告警通知
```bash
# 创建告警渠道配置
cat > alert-channel.json << EOF
{
  "name": "Slack Alerts",
  "type": "slack",
  "settings": {
    "url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
  }
}
EOF

# 添加告警渠道
curl -X POST \
  -H "Content-Type: application/json" \
  -d @alert-channel.json \
  http://admin:admin123@localhost:3000/api/alert-notifications
```

## 📊 监控与日志

### 常用查询示例
```promql
# 集群CPU使用率
100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# 内存使用率
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# Pod重启次数
increase(kube_pod_container_status_restarts_total[1h])

# 网络流量
rate(container_network_receive_bytes_total[5m])
```

### 日志查看
```bash
# 查看Grafana日志
kubectl logs -n monitoring deploy/grafana

# 查看插件日志
kubectl logs -n monitoring deploy/grafana -c grafana-plugin
```

## 🔍 故障排除

### 常见问题
1. **问题**: 无法连接数据源
   - **检查**: 网络策略和Service连接
   - **解决方案**: 验证服务可达性和认证配置

2. **问题**: 仪表板加载缓慢
   - **检查**: 查询优化和缓存设置
   - **解决方案**: 优化查询语句，调整时间范围

### 健康检查
```bash
# 检查Grafana健康状态
kubectl exec -n monitoring deploy/grafana -- wget -qO- http://localhost:3000/api/health

# 检查数据源连接
curl -s http://admin:admin123@localhost:3000/api/datasources | jq '.[].name'
```

## 🧪 测试验证

### 功能测试脚本
```bash
#!/bin/bash
# test-grafana.sh

echo "Testing Grafana setup..."

# 检查服务状态
if kubectl get pods -n monitoring -l app.kubernetes.io/name=grafana | grep Running; then
    echo "✓ Grafana is running"
else
    echo "✗ Grafana is not running"
    exit 1
fi

# 测试API访问
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://admin:admin123@localhost:3000/api/health)
if [ "$STATUS" = "200" ]; then
    echo "✓ Grafana API is accessible"
else
    echo "✗ Grafana API is not accessible"
fi
```

### 性能测试
```bash
# 测试并发访问
ab -n 1000 -c 10 http://admin:admin123@localhost:3000/

# 监控资源使用
kubectl top pods -n monitoring -l app.kubernetes.io/name=grafana
```

## 📈 最佳实践

### 性能优化配置
```yaml
grafana.ini:
  server:
    max_connections: 100
  analytics:
    reporting_enabled: false
  log:
    level: info
    
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "1Gi"
    cpu: "500m"
```

### 安全配置
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 472
  fsGroup: 472

# 启用匿名访问控制
env:
  GF_AUTH_ANONYMOUS_ENABLED: "false"
  GF_SECURITY_ADMIN_PASSWORD: "__SECRET__"
```

## 🚀 升级维护

### 版本升级
```bash
# 检查可用版本
helm search repo grafana/grafana

# 执行升级
helm upgrade grafana grafana/grafana \
  --namespace monitoring \
  --version 6.50.0 \
  --reuse-values
```

### 备份恢复
```bash
# 备份仪表板
kubectl exec -n monitoring deploy/grafana -- find /var/lib/grafana/dashboards -name "*.json" -exec cp {} /tmp/ \;

# 备份配置
kubectl get secret -n monitoring grafana -o yaml > grafana-secret-backup.yaml
```

## 📚 相关资源

### 官方文档
- [Grafana官方文档](https://grafana.com/docs/)
- [Grafana Kubernetes集成](https://grafana.com/docs/grafana/latest/setup-grafana/installation/kubernetes/)

### 社区资源
- Grafana社区论坛
- Kubernetes监控仪表板模板库

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 贡献流程
1. Fork项目仓库
2. 创建功能分支
3. 提交代码更改
4. 编写测试用例
5. 发起Pull Request

## 📄 许可证

本项目采用 Apache 2.0 许可证

---
*最后更新: 2026年2月3日*