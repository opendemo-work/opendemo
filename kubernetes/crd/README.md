# Custom Resource Definitions

Kubernetes CRD自定义资源定义演示，展示如何扩展K8s API。

## 什么是CRD

CRD允许用户定义自己的资源类型，扩展Kubernetes API：

```
扩展流程:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  定义CRD    │───▶│  创建CR    │───▶│  Controller │
│  (Schema)   │    │  (Instance) │    │  (Reconcile)│
└─────────────┘    └─────────────┘    └─────────────┘
```

## 创建CRD

### 定义Database资源
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databases.myapp.io
spec:
  group: myapp.io
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              engine:
                type: string
                enum: [mysql, postgres, redis]
              version:
                type: string
              storage:
                type: string
                pattern: '^[0-9]+Gi$'
              replicas:
                type: integer
                minimum: 1
                maximum: 10
  scope: Namespaced
  names:
    plural: databases
    singular: database
    kind: Database
    shortNames:
    - db
```

### 使用自定义资源
```yaml
apiVersion: myapp.io/v1
kind: Database
metadata:
  name: production-db
spec:
  engine: postgres
  version: "14"
  storage: 100Gi
  replicas: 3
```

## 开发Controller

### Go Controller示例
```go
package main

import (
    "context"
    "fmt"
    "time"
    
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/client-go/kubernetes"
    "k8s.io/client-go/rest"
)

func main() {
    config, _ := rest.InClusterConfig()
    clientset, _ := kubernetes.NewForConfig(config)
    
    for {
        // 获取所有Database资源
        databases, _ := clientset.RESTClient().
            Get().
            AbsPath("/apis/myapp.io/v1/namespaces/default/databases").
            Do(context.TODO()).
            Raw()
        
        fmt.Printf("Found databases: %s\n", databases)
        time.Sleep(10 * time.Second)
    }
}
```

### Operator Framework
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 安装Operator SDK
curl -LO https://github.com/operator-framework/operator-sdk/releases/latest/download/operator-sdk_linux_amd64
chmod +x operator-sdk_linux_amd64
sudo mv operator-sdk_linux_amd64 /usr/local/bin/operator-sdk

# 创建Operator
operator-sdk init --domain myapp.io --repo github.com/myuser/database-operator
operator-sdk create api --group myapp --version v1 --kind Database
operator-sdk create webhook --group myapp --version v1 --kind Database
```

## 验证与状态

```yaml
apiVersion: myapp.io/v1
kind: Database
metadata:
  name: production-db
spec:
  engine: postgres
  version: "14"
status:
  phase: Ready
  conditions:
  - type: Available
    status: "True"
    lastTransitionTime: "2024-01-15T10:00:00Z"
    reason: DeploymentComplete
    message: "Database is ready for connections"
  endpoint: postgres://db.default.svc.cluster.local:5432
```

## 常用命令

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# 查看CRD
kubectl get crd

# 查看自定义资源
kubectl get databases
kubectl get databases -o yaml

# 编辑CR
kubectl edit database production-db

# 删除CRD (会级联删除所有CR)
kubectl delete crd databases.myapp.io
```

## 学习要点

1. OpenAPI v3 Schema验证
2. Controller开发模式
3. Operator生命周期管理
4. Webhook准入控制
5. 多版本API管理

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 Kubernetes 核心概念
- ✅ 掌握相关的资源配置与命令
- ✅ 能够在本地集群中复现

## 🚀 快速开始

### 部署资源

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/apply.sh
```

### 检查状态

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/check.sh
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的 Kubernetes 核心概念。

### 2. 适用场景

- 场景 1：开发与测试
- 场景 2：生产环境参考
- 场景 3：故障排查

## 💻 代码示例

### 基本命令

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际场景替换
kubectl apply -f manifests/
```
