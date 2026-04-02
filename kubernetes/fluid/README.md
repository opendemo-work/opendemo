# Fluid Data Acceleration

Fluid数据集加速引擎部署演示。

## 什么是Fluid

Fluid是云原生数据加速引擎，为AI/大数据提供数据集抽象：

```
Fluid架构:
┌─────────────────────────────────────────────────────────┐
│                   Application                          │
│              (Training/Inference)                       │
├─────────────────────────────────────────────────────────┤
│              Dataset (CRD)                              │
│         (数据抽象与缓存管理)                              │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │Runtime  │  │Runtime  │  │Runtime  │  │Runtime  │   │
│  │(Alluxio)│  │ (JuiceFS)│  │(JindoFS)│  │(GooseFS)│   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │
├─────────────────────────────────────────────────────────┤
│              Cache Workers (缓存层)                      │
├─────────────────────────────────────────────────────────┤
│              Underlay Storage                           │
│         (HDFS/S3/OSS/Ceph)                              │
└─────────────────────────────────────────────────────────┘
```

## 安装部署

```bash
# 安装Fluid
helm repo add fluid https://fluid-cloudnative.github.io/charts
helm install fluid fluid/fluid

# 验证
kubectl get pods -n fluid-system
```

## 使用示例

```yaml
# 创建Dataset和Runtime
apiVersion: data.fluid.io/v1alpha1
kind: Dataset
metadata:
  name: imagenet
spec:
  mounts:
  - mountPoint: oss://bucket/imagenet/
    name: data
    options:
      fs.oss.endpoint: oss-cn-beijing.aliyuncs.com
    encryptOptions:
    - name: fs.oss.accessKeyId
      valueFrom:
        secretKeyRef:
          name: oss-secret
          key: access-key-id
---
apiVersion: data.fluid.io/v1alpha1
kind: AlluxioRuntime
metadata:
  name: imagenet
spec:
  replicas: 3
  data:
    replicas: 1
  tieredstore:
    levels:
    - mediumtype: SSD
      path: /alluxio/ssd
      quota: 100Gi
      high: "0.99"
      low: "0.8"
```

## 数据预热

```bash
# 创建DataLoad进行预热
kubectl apply -f - <<EOF
apiVersion: data.fluid.io/v1alpha1
kind: DataLoad
metadata:
  name: imagenet-warmup
spec:
  dataset:
    name: imagenet
    namespace: default
  loadMetadata: true
  target:
    - path: /
      replicas: 1
EOF

# 查看进度
kubectl get dataload imagenet-warmup
```

## 学习要点

1. 数据集抽象概念
2. 缓存Runtime选择
3. 数据预热策略
4. 亲和性调度
5. 性能监控优化
