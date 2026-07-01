<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Velero Backup

Velero集群备份与灾难恢复演示。

## 什么是Velero

Velero是Kubernetes集群备份、恢复和迁移工具：

```
备份流程:
┌─────────┐     ┌─────────┐     ┌─────────┐
│   Velero │───▶│  Backup │───▶│  Object │
│   Client │    │  (CRD)  │    │ Storage │
└─────────┘     └────┬────┘     └─────────┘
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐
    │   PV    │ │Resource │ │Metadata │
    │Snapshot │ │  YAML   │ │         │
    └─────────┘ └─────────┘ └─────────┘
```

## 安装Velero

```bash
# 安装CLI
curl -L https://github.com/vmware-tanzu/velero/releases/latest/download/velero-linux-amd64.tar.gz | tar xz
sudo mv velero /usr/local/bin/

# 安装服务端 (AWS S3示例)
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.6.0 \
  --bucket my-backup-bucket \
  --backup-location-config region=us-east-1 \
  --snapshot-location-config region=us-east-1 \
  --secret-file ./aws-credentials
```

## 备份操作

### 创建备份
```bash
# 全集群备份
velero backup create full-backup

# 备份指定命名空间
velero backup create production-backup \
  --include-namespaces production \
  --include-resources deployments,pods,pvc

# 带PV快照的备份
velero backup create app-with-data \
  --include-namespaces myapp \
  --snapshot-volumes \
  --volume-snapshot-locations aws-default

# 定时备份
velero schedule create daily-backup \
  --schedule="0 2 * * *" \
  --include-namespaces production
```

### 查看备份
```bash
# 列出备份
velero backup get

# 查看备份详情
velero backup describe full-backup

# 查看备份日志
velero backup logs full-backup
```

## 恢复操作

```bash
# 列出可恢复的备份
velero backup get

# 恢复整个备份
velero restore create --from-backup full-backup

# 恢复指定资源
velero restore create --from-backup production-backup \
  --include-resources deployments \
  --include-namespaces production

# 恢复到新命名空间
velero restore create --from-backup full-backup \
  --namespace-mappings old-ns:new-ns
```

## 备份存储位置

```yaml
apiVersion: velero.io/v1
kind: BackupStorageLocation
metadata:
  name: default
  namespace: velero
spec:
  provider: aws
  objectStorage:
    bucket: my-backup-bucket
    prefix: cluster-backups
  config:
    region: us-east-1
    s3ForcePathStyle: "true"
```

## 学习要点

1. 备份策略设计
2. PV快照机制
3. 跨集群迁移
4. 灾难恢复演练
5. 存储后端配置

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 Kubernetes 核心概念
- ✅ 掌握相关的资源配置与命令
- ✅ 能够在本地集群中复现

## 🚀 快速开始

### 部署资源

```bash
./scripts/apply.sh
```

### 检查状态

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
