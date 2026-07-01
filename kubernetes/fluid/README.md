<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

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

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
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

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
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


---

## 📚 扩展阅读

### 相关概念

- 概念 1：补充说明
- 概念 2：补充说明
- 概念 3：补充说明

### 常见问题

#### Q1：本案例适用于哪些场景？

**A**：本案例适用于学习、实验和工程参考。

#### Q2：如何验证运行结果？

**A**：按照 README 中的命令执行，并观察输出是否符合预期。

#### Q3：遇到问题时如何排查？

**A**：检查环境依赖是否正确安装，查看命令输出和日志信息。

### 推荐资源

- [OpenDemo 官方文档](https://github.com/opendemo)
- [相关技术官方文档](https://example.com)

### 进阶主题

- [ ] 进阶主题 1
- [ ] 进阶主题 2
- [ ] 进阶主题 3

---

*本 README 为自动生成模板，请根据实际案例内容补充完善。*
