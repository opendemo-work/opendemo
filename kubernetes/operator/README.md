# Kubernetes Operator

Kubernetes Operator开发与部署演示，展示自动化运维复杂应用的最佳实践。

## 什么是Operator

Operator使用自定义资源定义(CRD)和Controller来封装特定应用的运维知识：

```
Operator模式:
┌─────────────────────────────────────────────────────────┐
│                   Custom Resource                        │
│              (应用的期望状态描述)                         │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   Controller Loop                        │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │ Observe │─▶│  Diff   │─▶│  Act    │─▶│  Wait   │   │
│  │ (观察)  │  │ (对比)  │  │ (执行)  │  │ (等待)  │   │
│  └─────────┘  └─────────┘  └─────────┘  └────┬────┘   │
│                                               │        │
└───────────────────────────────────────────────┼────────┘
                                                │
                         ┌──────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   Actual State                         │
│              (K8s原生资源集合)                           │
└─────────────────────────────────────────────────────────┘
```

## Operator Framework

### 架构组件
```
Operator SDK架构:
┌─────────────────────────────────────────────────────────┐
│                   Operator Manager                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Reconcile │  │    Event    │  │    Cache    │     │
│  │    Loop     │  │   Handler   │  │   Manager   │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Scheme    │  │   Client    │  │   Leader    │     │
│  │   Builder   │  │   (读写)     │  │   Election  │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

## 开发Operator

### 创建项目
```bash
# 初始化项目
operator-sdk init --domain example.com --repo github.com/example/mysql-operator

# 创建API
operator-sdk create api --group database --version v1 --kind MySQL

# 创建Webhook
operator-sdk create webhook --group database --version v1 --kind MySQL
```

### Reconcile逻辑
```go
func (r *MySQLReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := log.FromContext(ctx)
    
    // 获取MySQL实例
    mysql := &databasev1.MySQL{}
    if err := r.Get(ctx, req.NamespacedName, mysql); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    
    // 创建Deployment
    deployment := r.deploymentForMySQL(mysql)
    if err := r.Create(ctx, deployment); err != nil {
        if errors.IsAlreadyExists(err) {
            // 已存在则更新
            existing := &appsv1.Deployment{}
            r.Get(ctx, types.NamespacedName{Name: deployment.Name, Namespace: deployment.Namespace}, existing)
            existing.Spec = deployment.Spec
            r.Update(ctx, existing)
        }
    }
    
    // 创建Service
    service := r.serviceForMySQL(mysql)
    r.Create(ctx, service)
    
    // 更新状态
    mysql.Status.Phase = "Running"
    r.Status().Update(ctx, mysql)
    
    return ctrl.Result{RequeueAfter: 30 * time.Second}, nil
}
```

## 安装Operator

### OLM (Operator Lifecycle Manager)
```bash
# 安装OLM
operator-sdk olm install

# 部署Operator
make deploy IMG=myregistry/mysql-operator:v1.0.0

# 通过OLM安装
kubectl create -f config/manifests/mysql-operator.yaml
```

### Helm方式
```bash
helm repo add mysql-operator https://charts.mysql.io
helm install mysql-operator mysql-operator/mysql-operator
```

## 常用Operators

| Operator | 用途 | 安装 |
|----------|------|------|
| prometheus-operator | 监控部署 | helm/prometheus-community/kube-prometheus-stack |
| cert-manager | 证书管理 | helm/jetstack/cert-manager |
| rook-ceph | 存储编排 | helm/rook/rook-ceph |
| strimzi | Kafka管理 | helm/strimzi/strimzi-kafka-operator |
| zalando-postgres | PostgreSQL | kubectl apply -f operator.yaml |

## 学习要点

1. Controller模式与Reconcile循环
2. 自定义资源状态管理
3. Operator生命周期
4. 多版本API迁移
5. 测试与调试技巧
