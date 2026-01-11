# Velero基础安装与配置演示

## 简介
本Demo演示如何在Kubernetes集群中安装Velero备份工具，并配置MinIO作为对象存储后端。Velero是VMware Tanzu提供的Kubernetes集群备份和恢复解决方案，支持集群资源备份、持久卷快照、跨集群迁移等功能。

## 学习目标
- 理解Velero的核心组件和架构
- 掌握使用Helm安装Velero的方法
- 学会配置对象存储后端（MinIO）
- 验证Velero安装的正确性

## 环境要求
- Kubernetes集群 >= v1.20（可使用minikube、kind或云厂商Kubernetes服务）
- kubectl >= v1.20
- Helm >= v3.0
- 8GB+ 可用内存
- 10GB+ 可用存储空间

> **提示**: 本演示使用MinIO作为测试环境的对象存储。生产环境建议使用AWS S3、Azure Blob Storage或Google Cloud Storage等托管服务。

## 文件说明
- `code/minio-deployment.yaml`: MinIO对象存储部署配置
- `code/minio-service.yaml`: MinIO服务暴露配置
- `code/velero-values.yaml`: Velero Helm安装配置文件
- `code/credentials-velero`: MinIO访问凭证文件（示例）
- `code/install.sh`: 一键安装脚本

## 架构说明

### Velero组件架构
```
┌─────────────────────────────────────────────────┐
│           Kubernetes Cluster                     │
│  ┌──────────────┐         ┌─────────────────┐  │
│  │ Velero CLI   │────────▶│ Velero Server   │  │
│  │              │         │ (Deployment)    │  │
│  └──────────────┘         └─────────────────┘  │
│                                   │              │
│                                   ▼              │
│                          ┌─────────────────┐    │
│                          │  MinIO Service  │    │
│                          │  (对象存储)     │    │
│                          └─────────────────┘    │
└─────────────────────────────────────────────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  备份数据存储   │
                          │  (Bucket:velero)│
                          └─────────────────┘
```

## 逐步实操指南

### 步骤1: 部署MinIO对象存储

MinIO是一个轻量级、S3兼容的对象存储服务，非常适合用于本地测试环境。

```bash
# 创建velero命名空间
kubectl create namespace velero

# 部署MinIO
kubectl apply -f code/minio-deployment.yaml
kubectl apply -f code/minio-service.yaml

# 等待MinIO Pod就绪
kubectl wait --for=condition=Ready pod -l app=minio -n velero --timeout=120s
```

**预期输出**:
```
namespace/velero created
deployment.apps/minio created
service/minio created
pod/minio-xxxx condition met
```

### 步骤2: 验证MinIO服务

```bash
# 检查MinIO Pod状态
kubectl get pods -n velero -l app=minio

# 获取MinIO Service信息
kubectl get svc -n velero -l app=minio
```

**预期输出**:
```
NAME                     READY   STATUS    RESTARTS   AGE
minio-5d56f7c9b6-xxxxx   1/1     Running   0          30s

NAME    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
minio   ClusterIP   10.96.123.456   <none>        9000/TCP   30s
```

### 步骤3: 安装Velero CLI（可选）

如果您还没有安装Velero CLI工具，请按照以下步骤安装：

**Linux/macOS**:
```bash
# 下载Velero CLI
wget https://github.com/vmware-tanzu/velero/releases/download/v1.12.3/velero-v1.12.3-linux-amd64.tar.gz

# 解压并安装
tar -xvf velero-v1.12.3-linux-amd64.tar.gz
sudo mv velero-v1.12.3-linux-amd64/velero /usr/local/bin/

# 验证安装
velero version --client-only
```

**Windows** (使用Chocolatey):
```powershell
choco install velero
```

或者直接从[Velero GitHub Releases](https://github.com/vmware-tanzu/velero/releases)下载对应平台的二进制文件。

### 步骤4: 准备MinIO访问凭证

创建凭证文件用于Velero访问MinIO：

```bash
# 创建凭证文件
cat > code/credentials-velero << EOF
[default]
aws_access_key_id = minio
aws_secret_access_key = minio123
EOF
```

### 步骤5: 使用Helm安装Velero

```bash
# 添加Velero Helm仓库
helm repo add vmware-tanzu https://vmware-tanzu.github.io/helm-charts
helm repo update

# 使用配置文件安装Velero
helm install velero vmware-tanzu/velero \
  --namespace velero \
  --values code/velero-values.yaml \
  --create-namespace

# 或者使用命令行参数直接安装
helm install velero vmware-tanzu/velero \
  --namespace velero \
  --set-file credentials.secretContents.cloud=code/credentials-velero \
  --set configuration.provider=aws \
  --set configuration.backupStorageLocation.name=default \
  --set configuration.backupStorageLocation.bucket=velero \
  --set configuration.backupStorageLocation.config.region=minio \
  --set configuration.backupStorageLocation.config.s3ForcePathStyle=true \
  --set configuration.backupStorageLocation.config.s3Url=http://minio.velero.svc:9000 \
  --set initContainers[0].name=velero-plugin-for-aws \
  --set initContainers[0].image=velero/velero-plugin-for-aws:v1.8.0 \
  --set initContainers[0].volumeMounts[0].mountPath=/target \
  --set initContainers[0].volumeMounts[0].name=plugins
```

### 步骤6: 验证Velero安装

```bash
# 检查Velero Pod状态
kubectl get pods -n velero

# 使用Velero CLI检查版本
velero version

# 检查BackupStorageLocation状态
velero backup-location get

# 查看Velero日志
kubectl logs deployment/velero -n velero
```

**预期输出 - Pod状态**:
```
NAME                      READY   STATUS    RESTARTS   AGE
minio-5d56f7c9b6-xxxxx    1/1     Running   0          5m
velero-7b8c5d8f9c-xxxxx   1/1     Running   0          2m
```

**预期输出 - Velero版本**:
```
Client:
        Version: v1.12.3
        Git commit: abc123def456

Server:
        Version: v1.12.3
```

**预期输出 - BackupStorageLocation**:
```
NAME      PROVIDER   BUCKET/PREFIX   PHASE       LAST VALIDATED   ACCESS MODE   DEFAULT
default   aws        velero          Available   10s              ReadWrite     true
```

> ✅ 如果看到`PHASE`为`Available`，说明Velero已成功连接到MinIO对象存储！

### 步骤7: 创建测试备份验证安装

```bash
# 创建一个简单的测试备份（备份velero命名空间自身）
velero backup create test-backup --include-namespaces velero

# 等待备份完成
velero backup describe test-backup --details

# 查看备份列表
velero backup get
```

**预期输出**:
```
NAME          STATUS      ERRORS   WARNINGS   CREATED                         EXPIRES   STORAGE LOCATION   SELECTOR
test-backup   Completed   0        0          2026-01-11 23:45:00 +0800 CST   29d       default            <none>
```

### 步骤8: 清理测试备份

```bash
# 删除测试备份
velero backup delete test-backup --confirm
```

## 代码解析

### minio-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: minio
  namespace: velero
spec:
  selector:
    matchLabels:
      app: minio
  template:
    metadata:
      labels:
        app: minio
    spec:
      containers:
      - name: minio
        image: minio/minio:latest
        args:
        - server
        - /data
        env:
        - name: MINIO_ROOT_USER
          value: "minio"
        - name: MINIO_ROOT_PASSWORD
          value: "minio123"
        ports:
        - containerPort: 9000
        volumeMounts:
        - name: data
          mountPath: /data
      volumes:
      - name: data
        emptyDir: {}
```

**关键配置说明**:
- `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD`: MinIO的访问凭证
- `emptyDir`: 使用临时存储（生产环境应使用PersistentVolumeClaim）
- `server /data`: MinIO以单节点模式启动

### velero-values.yaml核心配置
```yaml
configuration:
  provider: aws
  backupStorageLocation:
    name: default
    bucket: velero
    config:
      region: minio
      s3ForcePathStyle: "true"
      s3Url: http://minio.velero.svc:9000

credentials:
  useSecret: true
  secretContents:
    cloud: |
      [default]
      aws_access_key_id = minio
      aws_secret_access_key = minio123

initContainers:
  - name: velero-plugin-for-aws
    image: velero/velero-plugin-for-aws:v1.8.0
    volumeMounts:
      - mountPath: /target
        name: plugins
```

**关键参数说明**:
- `provider: aws`: 使用AWS插件（MinIO兼容S3 API）
- `s3ForcePathStyle`: 强制使用路径风格访问（MinIO要求）
- `s3Url`: MinIO服务的内部地址
- `initContainers`: 安装AWS插件以支持S3兼容存储

## 常见问题解答

### Q1: BackupStorageLocation状态显示Unavailable怎么办？

**A**: 检查以下几点：
1. MinIO Pod是否正常运行：`kubectl get pods -n velero -l app=minio`
2. 访问凭证是否正确：`kubectl get secret -n velero cloud-credentials -o yaml`
3. 网络连接是否正常：`kubectl exec -n velero deployment/velero -- curl http://minio.velero.svc:9000`
4. 查看Velero日志：`kubectl logs -n velero deployment/velero`

### Q2: 如何在生产环境中部署Velero？

**A**: 生产环境建议：
- 使用云厂商的对象存储服务（AWS S3、Azure Blob、GCS）
- 为MinIO配置持久化存储（PersistentVolume）
- 启用HTTPS和适当的访问控制
- 配置备份保留策略和定时备份
- 部署在高可用的Kubernetes集群上

### Q3: Velero CLI和Server版本不匹配会有影响吗？

**A**: 建议保持版本一致。如果出现不兼容，CLI会给出警告。可以通过`velero version`查看版本信息。

### Q4: 如何卸载Velero？

**A**: 执行以下命令：
```bash
helm uninstall velero -n velero
kubectl delete namespace velero
```

### Q5: MinIO的数据会持久化吗？

**A**: 当前配置使用`emptyDir`，Pod重启后数据会丢失。生产环境应使用PersistentVolumeClaim：
```yaml
volumes:
- name: data
  persistentVolumeClaim:
    claimName: minio-pvc
```

## 扩展学习建议

1. **对象存储选型**: 
   - 了解AWS S3、Azure Blob Storage、Google Cloud Storage的差异
   - 学习MinIO的高可用部署模式

2. **Velero高级功能**:
   - 持久卷快照（VolumeSnapshot）
   - 备份钩子（Backup Hooks）
   - 跨集群迁移（Cluster Migration）

3. **监控和告警**:
   - 集成Prometheus监控Velero metrics
   - 配置备份失败告警

4. **备份策略优化**:
   - 增量备份与全量备份的权衡
   - 备份窗口规划
   - 异地容灾备份

## 参考资料
- [Velero官方文档](https://velero.io/docs/v1.12/)
- [MinIO官方文档](https://min.io/docs/minio/linux/index.html)
- [Velero GitHub仓库](https://github.com/vmware-tanzu/velero)
- [Helm Charts for Velero](https://github.com/vmware-tanzu/helm-charts)

## 下一步

完成基础安装后，您可以继续学习：
- **namespace-backup**: 命名空间级别备份演示
- **cluster-backup**: 集群级别全量备份演示
- **scheduled-backup**: 定时备份策略配置演示
