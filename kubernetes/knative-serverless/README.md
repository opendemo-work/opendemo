# Knative Serverless

Knative无服务器平台实践。

## 什么是Knative

Knative是Kubernetes上的无服务器平台：

```
Knative组件:
┌─────────────────────────────────────────────────────────┐
│  Serving (服务管理)                                       │
│  - Service                                               │
│  - Revision                                              │
│  - Route                                                 │
├─────────────────────────────────────────────────────────┤
│  Eventing (事件驱动)                                      │
│  - Source                                                │
│  - Broker                                                │
│  - Trigger                                               │
└─────────────────────────────────────────────────────────┘
```

## 安装Knative

```bash
# 安装Knative Serving
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.12.0/serving-crds.yaml
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.12.0/serving-core.yaml

# 安装网络层 (Kourier)
kubectl apply -f https://github.com/knative/net-kourier/releases/download/knative-v1.12.0/kourier.yaml
```

## 部署Serverless服务

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: hello-world
spec:
  template:
    spec:
      containers:
        - image: gcr.io/knative-samples/helloworld-go
          env:
            - name: TARGET
              value: "Knative"
```

## 学习要点

1. 无服务器架构
2. 自动扩缩容
3. 事件驱动
4. 服务版本管理
5. 冷启动优化
