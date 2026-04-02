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
