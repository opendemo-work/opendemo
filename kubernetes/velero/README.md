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
