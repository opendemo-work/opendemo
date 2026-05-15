# 华为云CLI命令速查表

> 华为云命令行工具完整参考手册，覆盖计算、存储、数据库、网络、安全等核心产品线

---

## 1. 安装与配置 (Installation & Config)

### 1.1 安装 Huawei Cloud CLI

Huawei Cloud CLI (`huaweicloud`) 基于 Python 开发，支持 Linux/macOS/Windows。

**Linux/macOS**

```bash
# 通过 pip 安装
pip install huaweicloudsdk

# 或通过安装脚本
curl -s https://obs.cn-north-4.myhuaweicloud.com/tools/cli/setup.obs?region=cn-north-4 -o huawei-cli-install.sh
bash huawei-cli-install.sh
```

**Windows**

```powershell
# 通过 pip 安装
pip install huaweicloudsdk

# 或下载 MSI 安装包
# https://support.huaweicloud.com/cli-reference/
```

**验证安装**

```bash
# 检查 CLI 版本
huaweicloud --version
# 输出: huaweicloud-cli 3.2.13

# 查看帮助
huaweicloud help
```

### 1.2 配置凭证

Huawei Cloud 使用 Access Key (`ak`) 和 Secret Access Key (`sk`) 进行认证。

**交互式配置**

```bash
huaweicloud config credentials --ak YOUR_ACCESS_KEY --sk YOUR_SECRET_KEY
```

**配置示例**

```bash
# 配置默认凭证
huaweicloud config credentials \
  --ak 07N5MF7HTQ8LH0000000 \
  --sk YdN5TL8uX2vBj9W5L8m3K8W6X7J2H9K4L9M6N8Q \
  --region cn-north-4

# 配置多个区域的凭证
huaweicloud config add-profile --profile northchina --ak YOUR_AK --sk YOUR_SK --region cn-north-1
```

**配置文件位置**

- Linux/macOS: `~/.huaweicloud/config`
- Windows: `C:\Users\<username>\.huaweicloud\config`

**手动编辑配置**

```bash
# 查看当前配置
cat ~/.huaweicloud/config
# 输出示例:
# [default]
# ak = 07N5MF7HTQ8LH0000000
# sk = ********
# region = cn-north-4
# project_id = 06c6610a361900f22f0c8db61a000000
```

### 1.3 全局参数

以下参数可在所有命令中使用：

| 参数 | 说明 | 示例 |
|------|------|------|
| `--region` | 指定区域 | `--region cn-north-4` |
| `--output` | 输出格式 (json/text/table) | `--output json` |
| `--access-key` | Access Key | `--access-key AK...` |
| `--secret-key` | Secret Key | `--secret-key SK...` |
| `--project-id` | 项目ID | `--project-id 06c6610a...` |
| `--profile` | 配置文件profile名 | `--profile myprofile` |
| `--timeout` | 请求超时时间(秒) | `--timeout 60` |
| `--verify-ssl` | 是否验证SSL | `--verify-ssl true` |

**常用组合**

```bash
# 指定区域输出JSON格式
huaweicloud ecs servers list --region cn-north-4 --output json

# 使用指定项目ID
huaweicloud vpc vpcs list --project-id 06c6610a361900f22f0c8db61a000000

# 使用自定义profile
huaweicloud obs ls --profile prod-profile
```

---

## 2. 计算服务 (Compute)

### 2.1 ECS 云服务器

ECS (Elastic Cloud Server) 是华为云的基础计算服务。

**查询云服务器列表**

```bash
huaweicloud ecs servers list --limit 10
```

```json
{
  "servers": [
    {
      "id": "4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00",
      "name": "WebServer-01",
      "status": "RUNNING",
      "flavor": "s6.small.1",
      "image": "7d8d2c6d-1a3b-4c8d-9e2f-1a0b2c3d4e5f",
      "vpc_id": "4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01",
      "created": "2026-03-15T08:30:00Z"
    },
    {
      "id": "8b3cd4ae-6e82-4d92-c2bb-6g3fe3d72b11",
      "name": "DBServer-01",
      "status": "RUNNING",
      "flavor": "s6.medium.2",
      "image": "7d8d2c6d-1a3b-4c8d-9e2f-1a0b2c3d4e5f",
      "vpc_id": "4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01",
      "created": "2026-03-15T09:00:00Z"
    }
  ],
  "count": 2
}
```

**查看单个云服务器详情**

```bash
huaweicloud ecs servers show 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00
```

```json
{
  "id": "4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00",
  "name": "WebServer-01",
  "status": "RUNNING",
  "flavor": {
    "id": "s6.small.1",
    "name": "通用型 S6"
  },
  "image": {
    "id": "7d8d2c6d-1a3b-4c8d-9e2f-1a0b2c3d4e5f",
    "name": "Ubuntu 22.04 LTS"
  },
  "vpc_id": "4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01",
  "subnet_id": "9c2de5bf-7f93-4e93-d3cc-7d4fe4e83c22",
  "nics": [
    {
      "net_id": "9c2de5bf-7f93-4e93-d3cc-7d4fe4e83c22",
      "ip_address": "192.168.0.15"
    }
  ],
  "public_ip": "1.2.3.4",
  "created": "2026-03-15T08:30:00Z"
}
```

**创建云服务器**

```bash
huaweicloud ecs servers create \
  --name WebServer-02 \
  --flavor s6.small.1 \
  --image 7d8d2c6d-1a3b-4c8d-9e2f-1a0b2c3d4e5f \
  --vpc 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01 \
  --subnet 9c2de5bf-7f93-4e93-d3cc-7d4fe4e83c22 \
  --key-name my-keypair \
  --security-group 8a9b0c1d-2e3f-4a5b-6c7d-8e9f0a1b2c3d \
  --count 1
```

```json
{
  "id": "2c5ea7cd-8d82-4e93-b2bb-8f4ge5e84d33",
  "name": "WebServer-02",
  "status": "BUILD",
  "flavor": "s6.small.1",
  "vpc_id": "4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01",
  "created": "2026-05-14T10:30:00Z"
}
```

**停止云服务器**

```bash
huaweicloud ecs servers stop 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00
# 输出: Stop server request submitted. Server ID: 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00
```

**重启云服务器**

```bash
huaweicloud ecs servers reboot 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00 --type SOFT
# 输出: Reboot server request submitted. Server ID: 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00
```

**删除云服务器**

```bash
huaweicloud ecs servers delete 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00
# 输出: Server deleted successfully. Server ID: 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00
```

**查询可用镜像**

```bash
huaweicloud ecs images list --limit 10
```

```json
{
  "images": [
    {
      "id": "7d8d2c6d-1a3b-4c8d-9e2f-1a0b2c3d4e5f",
      "name": "Ubuntu 22.04 LTS 64bit",
      "os_type": "Linux",
      "os_version": "Ubuntu 22.04"
    },
    {
      "id": "8e9f1a2b-3c4d-5e6f-7a8b-9c0d1e2f3a4b",
      "name": "Windows Server 2022 Datacenter",
      "os_type": "Windows",
      "os_version": "Windows Server 2022"
    }
  ]
}
```

**创建云硬盘**

```bash
huaweicloud ecs volumes create \
  --name DataVolume \
  --volume-type SSD \
  --size 100 \
  --availability-zone cn-north-4a
```

```json
{
  "id": "7f8d2c6e-1b3c-4d5e-6f7a-8b9c0d1e2f3a4",
  "name": "DataVolume",
  "volume_type": "SSD",
  "size": 100,
  "status": "available",
  "availability_zone": "cn-north-4a"
}
```

**挂载云硬盘**

```bash
huaweicloud ecs volumes attach 7f8d2c6e-1b3c-4d5e-6f7a-8b9c0d1e2f3a4 \
  --server 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00
# 输出: Volume attached successfully. Attachment ID: 8b9c0d1e-2f3a-4b5c-6d7e-8f9a0b1c2d3e
```

**卸载云硬盘**

```bash
huaweicloud ecs volumes detach 7f8d2c6e-1b3c-4d5e-6f7a-8b9c0d1e2f3a4 \
  --server 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00
# 输出: Volume detached successfully.
```

### 2.2 CCE 容器集群

CCE (Cloud Container Engine) 是华为云的 Kubernetes 托管服务。

**查询容器集群列表**

```bash
huaweicloud cce clusters list
```

```json
{
  "items": [
    {
      "metadata": {
        "uid": "4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00",
        "name": "production-cluster",
        "display_name": "生产集群"
      },
      "spec": {
        "category": "Kubernetes",
        "flavor": "KubernetesCluster",
        "version": "1.28"
      },
      "status": {
        "phase": "Available"
      }
    }
  ]
}
```

**创建容器集群**

```bash
huaweicloud cce clusters create \
  --name production-cluster \
  --flavor KubernetesCluster \
  --vpc vpc-id \
  --subnet subnet-id \
  --container_network_cidr 10.0.0.0/16 \
  --service_network_cidr 172.16.0.0/16 \
  --version 1.28
```

```json
{
  "apiVersion": "v3",
  "kind": "Cluster",
  "metadata": {
    "uid": "4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00",
    "name": "production-cluster"
  },
  "status": {
    "phase": "Creating"
  }
}
```

**扩缩容集群节点**

```bash
# 扩容节点池 - 添加3个节点
huaweicloud cce nodePools scale cluster-uid \
  --nodepool-id np-uid \
  --desired 5

# 缩容节点池
huaweicloud cce nodePools scale cluster-uid \
  --nodepool-id np-uid \
  --desired 2
```

**删除容器集群**

```bash
huaweicloud cce clusters delete production-cluster
# 输出: Cluster deletion started. This may take several minutes.
```

**获取集群证书**

```bash
huaweicloud cce clusters get-cert cluster-uid
```

```yaml
apiVersion: v1
kind: Config
preferences: {}
clusters:
- name: production-cluster
  cluster:
    server: https://10.0.0.10:5443
    certificate-authority-data: LS0tLS1CRUdJTi...
contexts:
- name: production-cluster
  context:
    cluster: production-cluster
    user: cluster-admin
current-context: production-cluster
users:
- name: cluster-admin
  user:
    token: <cluster-token>
```

### 2.3 函数工作流 FunctionGraph

FunctionGraph 是华为云的函数即服务 (FaaS) 平台。

**查询函数列表**

```bash
huaweicloud functiongraph functions list --group default --limit 20
```

```json
{
  "functions": [
    {
      "function_urn": "urn:fss:cn-north-4:06c6610a36:functiongraph:default:my-image-resizer:latest",
      "name": "my-image-resizer",
      "runtime": "Python 3.9",
      "timeout": 30,
      "memory_size": 256,
      "count": 1
    },
    {
      "function_urn": "urn:fss:cn-north-4:06c6610a36:functiongraph:default:webhook-handler:latest",
      "name": "webhook-handler",
      "runtime": "Node.js 18",
      "timeout": 60,
      "memory_size": 512,
      "count": 1
    }
  ]
}
```

**创建函数**

```bash
huaweicloud functiongraph functions create \
  --name image-processor \
  --runtime "Python 3.9" \
  --handler index.handler \
  --memory-size 256 \
  --timeout 30 \
  --code-type zip \
  --code-url ./image-processor.zip
```

**调用函数**

```bash
# 同步调用
huaweicloud functiongraph functions invoke \
  --function-name my-image-resizer \
  --input '{"action": "resize", "width": 800, "height": 600}'
```

```json
{
  "result": {
    "statusCode": 200,
    "body": {
      "processed_url": "https://my-bucket.obs.cn-north-4.myhuaweicloud.com/processed/image.jpg",
      "processing_time_ms": 245
    }
  }
}
```

**删除函数**

```bash
huaweicloud functiongraph functions delete my-image-resizer
# 输出: Function deleted: my-image-resizer
```

---

## 3. 存储服务 (Storage)

### 3.1 OBS 对象存储

OBS (Object Storage Service) 是华为云的对象存储服务，兼容 S3 协议。

**OBS 命令使用 `obsutil` 工具**

```bash
# 安装 obsutil
curl -s https://obs.cn-north-4.myhuaweicloud.com/tools/obsutil -o obsutil && chmod +x obsutil

# 配置 OBS 凭证
./obsutil config -ak=YOUR_ACCESS_KEY -sk=YOUR_SECRET_KEY -endpoint=obs.cn-north-4.myhuaweicloud.com
```

**列出桶**

```bash
obsutil ls obs://
# 输出:
# obs://my-bucket-001
# obs://my-bucket-002
# obs://logs-archive-2026
# obs://cdn-source-files
```

**创建桶**

```bash
obsutil mb obs://my-new-bucket-cn-north-4
# 输出:
# Create bucket [obs://my-new-bucket-cn-north-4] successfully, status code is 200
```

**复制对象**

```bash
# 复制本地文件到 OBS
obsutil cp ./local-file.txt obs://my-bucket-001/documents/
# 输出:
# [LocalFile]=./local-file.txt -> [obs://my-bucket-001/documents/local-file.txt]
# Upload successfully, status code is 200

# 复制 OBS 对象到本地
obsutil cp obs://my-bucket-001/documents/report.pdf ./

# 批量复制
obsutil cp -r ./datafolder obs://my-bucket-001/backup/
```

**删除对象**

```bash
obsutil rm obs://my-bucket-001/documents/old-file.txt
# 输出:
# Delete object [obs://my-bucket-001/documents/old-file.txt] successfully, status code is 204
```

**同步目录**

```bash
obsutil sync ./local-folder obs://my-bucket-001/remote-folder/
# 输出:
# [Sync]local-folder -> obs://my-bucket-001/remote-folder/
# Summary: TotalCount=15, SuccessCount=15, FailedCount=0
```

**设置 CORS 规则**

```bash
obsutil cors set obs://my-bucket-001 -cors_file cors.json
```

```json
// cors.json
{
  "corsRules": [
    {
      "allowedOrigin": "https://www.example.com",
      "allowedMethod": ["GET", "POST", "PUT"],
      "allowedHeader": ["Authorization", "Content-Type"],
      "maxAgeSeconds": 3600
    }
  ]
}
```

**生命周期规则**

```bash
obsutil lifecycle set obs://my-bucket-001 -lf_file lifecycle.json
```

```json
// lifecycle.json
{
  "rules": [
    {
      "id": "archive-logs",
      "prefix": "logs/",
      "status": "Enabled",
      "expiration": {
        "days": 90
      },
      "transitions": [
        {
          "days": 30,
          "storageClass": "WARM"
        },
        {
          "days": 60,
          "storageClass": "COLD"
        }
      ]
    }
  ]
}
```

**静态网站托管**

```bash
obsutil website set obs://my-bucket-001 \
  --index-file index.html \
  --error-file error.html \
  --redirect-rule redirect.html
# 输出: Set website configuration successfully.
```

**生成签名 URL**

```bash
# 生成下载签名URL，有效期1小时
obsutil sign obs://my-bucket-001/documents/private.pdf -expire=3600
# 输出:
# https://my-bucket-001.obs.cn-north-4.myhuaweicloud.com/documents/private.pdf?AWSAccessKeyId=...&Expires=...&Signature=...

# 生成上传签名URL
obsutil sign obs://my-bucket-001/documents/upload.txt -expire=1800 -to PUT
```

### 3.2 云硬盘 EVS

EVS (Elastic Volume Service) 提供块存储服务。

**查询云硬盘列表**

```bash
huaweicloud evs volumes list --status available
```

```json
{
  "volumes": [
    {
      "id": "7f8d2c6e-1b3c-4d5e-6f7a-8b9c0d1e2f3a4",
      "name": "DataVolume-01",
      "volume_type": "SSD",
      "size": 500,
      "status": "available",
      "availability_zone": "cn-north-4a",
      "created_at": "2026-04-01T10:00:00Z"
    }
  ]
}
```

**创建云硬盘**

```bash
huaweicloud evs volumes create \
  --name BackupVolume \
  --volume-type SSD \
  --size 200 \
  --availability-zone cn-north-4a \
  --multiattach false
```

**挂载/卸载云硬盘**

```bash
# 挂载
huaweicloud evs volumes attach 7f8d2c6e-1b3c-4d5e-6f7a-8b9c0d1e2f3a4 \
  --server-id 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00

# 卸载
huaweicloud evs volumes detach 7f8d2c6e-1b3c-4d5e-6f7a-8b9c0d1e2f3a4 \
  --server-id 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00
```

**删除云硬盘**

```bash
huaweicloud evs volumes delete 7f8d2c6e-1b3c-4d5e-6f7a-8b9c0d1e2f3a4
# 输出: Delete volume request submitted. Volume ID: 7f8d2c6e-1b3c-4d5e-6f7a-8b9c0d1e2f3a4
```

**创建快照**

```bash
huaweicloud evs snapshots create \
  --name DailyBackup-0514 \
  --volume-id 7f8d2c6e-1b3c-4d5e-6f7a-8b9c0d1e2f3a4
```

```json
{
  "id": "9a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d",
  "name": "DailyBackup-0514",
  "volume_id": "7f8d2c6e-1b3c-4d5e-6f7a-8b9c0d1e2f3a4",
  "size": 200,
  "status": "creating"
}
```

### 3.3 文件存储 SFS

SFS (Scalable File Service) 提供 NFS 文件存储。

**查询文件共享列表**

```bash
huaweicloud sfs shares list
```

```json
{
  "shares": [
    {
      "id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
      "name": "shared-folder",
      "path": "/shared-folder",
      "size": 1024,
      "share_proto": "NFS",
      "status": "available"
    }
  ]
}
```

**创建文件共享**

```bash
huaweicloud sfs shares create \
  --name team-storage \
  --share-type NFS \
  --size 1024 \
  --vpc-id 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01
```

**删除文件共享**

```bash
huaweicloud sfs shares delete a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d
# 输出: Share deleted successfully.
```

---

## 4. 数据库服务 (Database)

### 4.1 RDS 数据库

RDS (Relational Database Service) 支持 MySQL、PostgreSQL、SQL Server 等。

**查询数据库列表**

```bash
huaweicloud rds databases list --instance-id rds-instance-uid
```

```json
{
  "databases": [
    {
      "name": "app_db",
      "charset": "utf8mb4",
      "collate_set": "utf8mb4_general_ci"
    },
    {
      "name": "analytics_db",
      "charset": "utf8mb4",
      "collate_set": "utf8mb4_general_ci"
    }
  ]
}
```

**创建数据库**

```bash
huaweicloud rds databases create \
  --instance-id rds-instance-uid \
  --name new_application \
  --charset utf8mb4
```

```json
{
  "name": "new_application",
  "charset": "utf8mb4",
  "created": "2026-05-14T12:00:00Z"
}
```

**查询用户列表**

```bash
huaweicloud rds users list --instance-id rds-instance-uid
```

```json
{
  "users": [
    {
      "name": "app_user",
      "host": "%",
      " databases": ["app_db"]
    }
  ]
}
```

**创建用户**

```bash
huaweicloud rds users create \
  --instance-id rds-instance-uid \
  --name app_user \
  --password "SecureP@ssw0rd!" \
  --host "%"
```

**授权用户权限**

```bash
huaweicloud rds users grant \
  --instance-id rds-instance-uid \
  --username app_user \
  --database app_db \
  --privileges SELECT,INSERT,UPDATE,DELETE
# 输出: User privileges granted successfully.
```

**创建备份**

```bash
huaweicloud rds backups create \
  --instance-id rds-instance-uid \
  --name weekly-full-backup \
  --backup-type full
```

```json
{
  "id": "backup-8a9b0c1d-2e3f-4a5b-6c7d-8e9f0a1b2c3d",
  "instance_id": "rds-instance-uid",
  "status": "BUILDING",
  "type": "full",
  "size": 50,
  "created": "2026-05-14T02:00:00Z"
}
```

**恢复实例**

```bash
huaweicloud rds instances restore \
  --instance-id rds-instance-uid \
  --backup-id backup-8a9b0c1d-2e3f-4a5b-6c7d-8e9f0a1b2c3d \
  --target-instance "rds-restored-0614"
```

### 4.2 Redis 缓存数据库

**查询 Redis 实例列表**

```bash
huaweicloud redis instances list --region cn-north-4
```

```json
{
  "instances": [
    {
      "id": "redis-instance-001",
      "name": "CacheCluster-01",
      "type": "cluster",
      "engine": "Redis",
      "engine_version": "6.2",
      "capacity": 1024,
      "status": "normal",
      "vpc_id": "vpc-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01"
    }
  ]
}
```

**创建 Redis 实例**

```bash
huaweicloud redis instances create \
  --name cache-prod \
  --engine Redis \
  --engine-version 6.2 \
  --flavor redis.search.ha \
  --capacity 1024 \
  --vpc-id 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01 \
  --subnet-id 9c2de5bf-7f93-4e93-d3cc-7d4fe4e83c22
```

**创建账户**

```bash
huaweicloud redis accounts create \
  --instance-id redis-instance-001 \
  --account-name appcache \
  --password "C@cheP@ss123"
```

**修改实例规格**

```bash
huaweicloud redis instances modify \
  --instance-id redis-instance-001 \
  --new-capacity 2048 \
  --backup-available true
```

### 4.3 GaussDB 分布式数据库

**查询 GaussDB 实例**

```bash
huaweicloud gaussdb instances list --db-type GaussDB
```

```json
{
  "instances": [
    {
      "id": "gaussdb-instance-001",
      "name": "GaussDB-Primary",
      "db_type": "GaussDB",
      "db_version": "8.0",
      "status": "normal",
      "flavor": "GaussDB.Mysql.8.xLarge.4",
      "vpc_id": "vpc-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01"
    }
  ]
}
```

**创建 GaussDB 实例**

```bash
huaweicloud gaussdb instances create \
  --name gaussdb-prod \
  --db-type GaussDB \
  --db-version 8.0 \
  --flavor GaussDB.Mysql.8.xLarge.4 \
  --capacity 200 \
  --vpc-id 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01
```

### 4.4 DDS (MongoDB) 文档数据库

DDS (Document Database Service) 是华为云的 MongoDB 兼容文档数据库服务。

**查询 DDS 实例列表**

```bash
huaweicloud dds instances list --region cn-north-4
```

```json
{
  "instances": [
    {
      "id": "dds-xxxxxxxx",
      "name": "my-dds",
      "status": "normal",
      "engine": "dds-community",
      "engine_version": "4.4",
      "flavor": "dds.community.dds.small",
      "availability_zone": "cn-north-4a"
    }
  ]
}
```

**创建 DDS 副本集实例**

```bash
huaweicloud dds instance create --region cn-north-4 \
  --name my-dds \
  --engine dds-community \
  --engine_version 4.4 \
  --flavor dds.community.dds.small \
  --availability_zone cn-north-4a \
  --vpc_id vpc-xxxxxxxx \
  --subnet_id subnet-xxxxxxxx \
  --security_group_id sg-xxxxxxxx \
  --port 8635 \
  --storage_mode hybrid \
  --disk_encryption_id "xxxxxxxx" \
  --ssl_status enabled
```

**创建分片集群实例**

```bash
huaweicloud dds shard instance create --region cn-north-4 \
  --name my-dds-shard \
  --engine dds-community \
  --engine_version 4.4 \
  --num_shards 3 \
  --shard_flavor dds.shard.dds.small \
  --shard_storage 10 \
  --mongos_flavor dds.mongos.small \
  --mongos_count 2
```

**创建数据库账号**

```bash
huaweicloud dds user create --region cn-north-4 \
  --instance_id dds-xxxxxxxx \
  --username myuser \
  --password "MyP@ssw0rd!" \
  --roles '[{"role":"readWrite","db":"mydb"}]'
```

**查询数据库列表**

```bash
huaweicloud dds database list --region cn-north-4 --instance_id dds-xxxxxxxx
```

**创建数据库**

```bash
huaweicloud dds database create --region cn-north-4 \
  --instance_id dds-xxxxxxxx \
  --db_name mydb
```

**备份实例**

```bash
huaweicloud dds backup create --region cn-north-4 --instance_id dds-xxxxxxxx
```

**查询备份列表**

```bash
huaweicloud dds backup list --region cn-north-4 --instance_id dds-xxxxxxxx
```

**变配**

```bash
huaweicloud dds instance resize --region cn-north-4 \
  --instance_id dds-xxxxxxxx \
  --flavor dds.community.dds.medium
```

**设置 SSL**

```bash
huaweicloud dds ssl modify --region cn-north-4 \
  --instance_id dds-xxxxxxxx \
  --ssl_status enabled
```

**删除实例**

```bash
huaweicloud dds instance delete --region cn-north-4 --instance_id dds-xxxxxxxx
```

---

## 5. 网络服务 (Networking)

### 5.1 VPC 虚拟私有云

VPC (Virtual Private Cloud) 提供隔离的网络环境。

**查询 VPC 列表**

```bash
huaweicloud vpc vpcs list
```

```json
{
  "vpcs": [
    {
      "id": "4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01",
      "name": "production-vpc",
      "cidr": "192.168.0.0/16",
      "status": "OK",
      "created_at": "2026-01-15T08:00:00Z"
    }
  ]
}
```

**创建 VPC**

```bash
huaweicloud vpc vpcs create \
  --name development-vpc \
  --cidr 10.0.0.0/16
```

```json
{
  "id": "8b3cd4ae-6e82-4d92-c2bb-6g3fe3d72b11",
  "name": "development-vpc",
  "cidr": "10.0.0.0/16",
  "status": "CREATING"
}
```

**查询子网列表**

```bash
huaweicloud vpc subnets list --vpc-id 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01
```

```json
{
  "subnets": [
    {
      "id": "9c2de5bf-7f93-4e93-d3cc-7d4fe4e83c22",
      "name": "web-subnet",
      "cidr": "192.168.0.0/24",
      "gateway_ip": "192.168.0.1",
      "az": "cn-north-4a",
      "vpc_id": "4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01"
    }
  ]
}
```

**创建子网**

```bash
huaweicloud vpc subnets create \
  --name api-subnet \
  --vpc-id 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01 \
  --cidr 192.168.1.0/24 \
  --gateway-ip 192.168.1.1 \
  --az cn-north-4a
```

**查询路由表**

```bash
huaweicloud vpc rout-tables list --vpc-id 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01
```

**创建路由表**

```bash
huaweicloud vpc rout-tables create \
  --name custom-route-table \
  --vpc-id 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01 \
  --routes '[{"destination":"0.0.0.0/0","nexthop":"local"}]'
```

**创建 NAT 网关**

```bash
huaweicloud vpc nat-gateways create \
  --name prod-nat \
  --vpc-id 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01 \
  --spec large \
  --router-id 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01
```

```json
{
  "id": "nat-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01",
  "name": "prod-nat",
  "spec": "large",
  "status": "ACTIVE",
  "vpc_id": "4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01"
}
```

### 5.2 ELB 负载均衡

ELB (Elastic Load Balance) 提供高可用负载均衡服务。

**查询负载均衡器列表**

```bash
huaweicloud elb loadbalancers list --region cn-north-4
```

```json
{
  "loadbalancers": [
    {
      "id": "elb-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00",
      "name": "web-lb",
      "type": "Application",
      "vpc_id": "4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01",
      "vip": "1.2.3.4",
      "status": "ACTIVE"
    }
  ]
}
```

**创建 Application 负载均衡器**

```bash
huaweicloud elb loadbalancers create \
  --name api-lb \
  --type application \
  --vpc-id 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01 \
  --subnet-id 9c2de5bf-7f93-4e93-d3cc-7d4fe4e83c22
```

```json
{
  "id": "elb-8b3cd4ae-6e82-4d92-c2bb-6g3fe3d72b11",
  "name": "api-lb",
  "type": "Application",
  "vip": "1.2.3.5",
  "status": "ACTIVE"
}
```

**查询后端服务器组**

```bash
huaweicloud elb pools list --loadbalancer-id elb-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00
```

```json
{
  "pools": [
    {
      "id": "pool-8a9b0c1d-2e3f-4a5b-6c7d-8e9f0a1b2c3d",
      "name": "backend-pool-01",
      "lb_algorithm": "ROUND_ROBIN",
      "protocol": "HTTP"
    }
  ]
}
```

**创建后端服务器组**

```bash
huaweicloud elb pools create \
  --name backend-pool-web \
  --loadbalancer-id elb-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00 \
  --protocol HTTP \
  --algorithm ROUND_ROBIN
```

**查询后端服务器**

```bash
huaweicloud elb members list --pool-id pool-8a9b0c1d-2e3f-4a5b-6c7d-8e9f0a1b2c3d
```

**添加后端服务器**

```bash
huaweicloud elb members create \
  --pool-id pool-8a9b0c1d-2e3f-4a5b-6c7d-8e9f0a1b2c3d \
  --subnet-id 9c2de5bf-7f93-4e93-d3cc-7d4fe4e83c22 \
  --protocol-port 80 \
  --address 192.168.0.15 \
  --weight 100
```

```json
{
  "id": "member-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00",
  "address": "192.168.0.15",
  "protocol_port": 80,
  "weight": 100,
  "status": "healthy"
}
```

### 5.3 弹性 IP

**查询带宽列表**

```bash
huaweicloud vpc bandwidths list
```

```json
{
  "bandwidths": [
    {
      "id": "bandwidth-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00",
      "name": "shared-bandwidth",
      "size": 500,
      "type": "PER",
      "share_type": "WHOLE"
    }
  ]
}
```

**创建带宽**

```bash
huaweicloud vpc bandwidths create \
  --name dedicated-bandwidth \
  --size 100 \
  --type PER
```

**绑定弹性 IP**

```bash
huaweicloud vpc bandwidths associate \
  --bandwidth-id bandwidth-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00 \
  --publicip-id publicip-8b3cd4ae-6e82-4d92-c2bb-6g3fe3d72b11
```

**解绑弹性 IP**

```bash
huaweicloud vpc bandwidths disassociate \
  --bandwidth-id bandwidth-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00 \
  --publicip-id publicip-8b3cd4ae-6e82-4d92-c2bb-6g3fe3d72b11
```

---

## 6. CDN 与加速

CDN (Content Delivery Network) 提供全球内容加速服务。

**查询加速域名列表**

```bash
huaweicloud cdn domain list --service_area mainland
```

```json
{
  "domains": [
    {
      "id": "cdn-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00",
      "domain_name": "cdn.example.com",
      "type": "accelerate",
      "service_area": "mainland",
      "status": "online",
      "cname": "cdn.example.com.w.cdngslb.com"
    }
  ]
}
```

**创建加速域名**

```bash
huaweicloud cdn domain create \
  --name cdn.example.com \
  --type accelerate \
  --service-area mainland \
  --origin {"domain":"origin.example.com","port":443,"obs_bucket_type":"public"}
```

```json
{
  "id": "cdn-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00",
  "domain_name": "cdn.example.com",
  "status": "configuring"
}
```

**启用/禁用域名**

```bash
# 启用域名
huaweicloud cdn domain enable cdn-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00

# 禁用域名
huaweicloud cdn domain disable cdn-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00
```

**刷新缓存**

```bash
huaweicloud cdn domain purge-cache \
  --domain cdn.example.com \
  --urls '["https://cdn.example.com/images/*","https://cdn.example.com/js/app.js"]'
```

```json
{
  "task_id": "purge-task-8a9b0c1d-2e3f-4a5b-6c7d-8e9f0a1b2c3d",
  "status": "processing",
  "total": 2
}
```

**预热缓存**

```bash
huaweicloud cdn domain preload-cache \
  --domain cdn.example.com \
  --urls '["https://cdn.example.com/banner-2026.jpg"]'
```

---

## 7. 安全服务 (Security)

### 7.1 DEW 密钥管理

DEW (Data Encryption Workshop) 提供密钥管理服务。

**查询密钥列表**

```bash
huaweicloud kms keys list --key_state 1
```

```json
{
  "keys": [
    {
      "key_id": "4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00",
      "key_alias": "prod-data-key",
      "key_state": "1",
      "key_type": "1",
      "description": "Production data encryption key",
      "creation_timestamp": "2026-03-15T08:00:00Z"
    }
  ]
}
```

**创建密钥**

```bash
huaweicloud kms keys create \
  --alias backup-encryption-key \
  --key_type 1 \
  --description "Backup encryption key for archives"
```

```json
{
  "key_id": "8b3cd4ae-6e82-4d92-c2bb-6g3fe3d72b11",
  "key_alias": "backup-encryption-key",
  "key_state": "1"
}
```

**加密数据**

```bash
huaweicloud kms encrypt-data \
  --key-id 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00 \
  --plain-text "SensitiveData123" \
  --encryption-algorithm AES-256
```

```json
{
  "cipher_text": "A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6...",
  "key_id": "4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00"
}
```

**解密数据**

```bash
huaweicloud kms decrypt-data \
  --key-id 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00 \
  --cipher-text "A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6..."
```

```json
{
  "plain_text": "SensitiveData123",
  "key_id": "4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00"
}
```

**删除密钥**

```bash
huaweicloud kms keys delete 8b3cd4ae-6e82-4d92-c2bb-6g3fe3d72b11
# 输出: Key scheduled for deletion after 7 days pending grace period.
```

### 7.2 安全组

**查询安全组列表**

```bash
huaweicloud vpc security-groups list --vpc-id 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01
```

```json
{
  "security_groups": [
    {
      "id": "8a9b0c1d-2e3f-4a5b-6c7d-8e9f0a1b2c3d",
      "name": "web-sg",
      "vpc_id": "4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01",
      "description": "Security group for web servers"
    }
  ]
}
```

**创建安全组**

```bash
huaweicloud vpc security-groups create \
  --name api-sg \
  --vpc-id 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01 \
  --description "Security group for API servers"
```

**创建安全组规则**

```bash
# 允许 HTTPS 入站
huaweicloud vpc security-group-rules create \
  --security-group-id 8a9b0c1d-2e3f-4a5b-6c7d-8e9f0a1b2c3d \
  --direction ingress \
  --protocol tcp \
  --port 443 \
  --remote-ip-prefix 0.0.0.0/0
```

```json
{
  "id": "rule-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00",
  "security_group_id": "8a9b0c1d-2e3f-4a5b-6c7d-8e9f0a1b2c3d",
  "direction": "ingress",
  "protocol": "tcp",
  "port": 443,
  "remote_ip_prefix": "0.0.0.0/0"
}
```

### 7.3 WAF 云 Web 应用防火墙

**查询防护域名**

```bash
huaweicloud waf domain list --region cn-north-4
```

```json
{
  "items": [
    {
      "id": "waf-domain-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00",
      "domain": "www.example.com",
      "protect_status": 1,
      "access_status": 1
    }
  ]
}
```

**创建防护域名**

```bash
huaweicloud waf domain create \
  --domain www.example.com \
  --proxy true \
  --certificate-id cert-8a9b0c1d-2e3f-4a5b-6c7d-8e9f0a1b2c3d
```

**修改域名防护策略**

```bash
huaweicloud waf domain modify-protect \
  --domain-id waf-domain-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00 \
  --level medium \
  --status 1
```

---

## 8. 中间件

### 8.1 DMS 消息队列

DMS (Distributed Message Service) 提供 Kafka/RabbitMQ 兼容消息队列。

**查询队列列表 (RabbitMQ)**

```bash
huaweicloud dms queues list --engine rabbitmq
```

```json
{
  "queues": [
    {
      "queue_id": "queue-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00",
      "name": "orders.queue",
      "engine": "rabbitmq",
      "max_msgs": 10000,
      "msg_validity_period": 2592000,
      "subscriptions": 3
    }
  ]
}
```

**创建队列 (RabbitMQ)**

```bash
huaweicloud dms queues create \
  --name notifications.queue \
  --engine rabbitmq \
  --vpc-id 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01 \
  --flavor rabbitmq.cluster.xlarge
```

**发送消息**

```bash
huaweicloud dms queues send-message \
  --queue-name orders.queue \
  --message '{"order_id": "ORD-2026-0514", "amount": 299.99, "customer": "user@example.com"}'
```

```json
{
  "message_id": "msg-8a9b0c1d-2e3f-4a5b-6c7d-8e9f0a1b2c3d",
  "result": "success"
}
```

**消费消息**

```bash
huaweicloud dms queues consume-message \
  --queue-name orders.queue \
  --max-messages 10 \
  --wait-timeout 30
```

**删除队列**

```bash
huaweicloud dms queues delete orders.queue
# 输出: Queue deletion completed. Queue name: orders.queue
```

### 8.2 Kafka 消息队列

**查询 Kafka 实例列表**

```bash
huaweicloud dms kafka instances list --region cn-north-4
```

```json
{
  "instances": [
    {
      "instance_id": "kafka-instance-001",
      "name": "event-streaming",
      "engine": "kafka",
      "version": "2.7",
      "spec": "kafka.physical.small",
      "status": "running",
      "vpc_id": "4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01"
    }
  ]
}
```

**创建 Kafka 实例**

```bash
huaweicloud dms kafka instances create \
  --name data-pipeline-kafka \
  --engine kafka \
  --version 2.7 \
  --flavor kafka.physical.small \
  --storage 600 \
  --vpc-id 4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a01 \
  --subnet-id 9c2de5bf-7f93-4e93-d3cc-7d4fe4e83c22
```

**查询 Topic**

```bash
huaweicloud dms kafka topics list --instance-id kafka-instance-001
```

```json
{
  "topics": [
    {
      "id": "topic-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00",
      "name": "user-events",
      "partitions": 6,
      "replication_factor": 3
    }
  ]
}
```

**创建 Topic**

```bash
huaweicloud dms kafka topics create \
  --instance-id kafka-instance-001 \
  --name transaction-events \
  --partitions 12 \
  --replication-factor 3
```

### 8.3 ROMA 集成平台

**查询应用列表**

```bash
huaweicloud roma apps list --instance-id roma-instance-001
```

```json
{
  "apps": [
    {
      "id": "app-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00",
      "name": "integration-app",
      "instance_id": "roma-instance-001"
    }
  ]
}
```

**创建应用**

```bash
huaweicloud roma apps create \
  --name microservice-bridge \
  --instance-id roma-instance-001 \
  --description "Bridge for microservice integration"
```

---

## 9. 监控与日志

### 9.1 云监控 CloudEye

**查询指标列表**

```bash
huaweicloud ces metrics list --namespace SYS.ECS
```

```json
{
  "metrics": [
    {
      "namespace": "SYS.ECS",
      "metric_name": "cpu_usage",
      "dimensions": [
        {"name": "instance_id", "value": "4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00"}
      ],
      "unit": "percent"
    },
    {
      "namespace": "SYS.ECS",
      "metric_name": "memory_usage",
      "dimensions": [...],
      "unit": "percent"
    }
  ]
}
```

**获取指标数据**

```bash
huaweicloud ces metrics get-data \
  --namespace SYS.ECS \
  --metric_name cpu_usage \
  --dimensions instance_id=4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00 \
  --from 1747200000000 \
  --to 1747286400000 \
  --period 300
```

```json
{
  "data": [
    {
      "timestamp": 1747200000000,
      "value": 45.2
    },
    {
      "timestamp": 1747200300000,
      "value": 48.7
    }
  ]
}
```

**创建告警规则**

```bash
huaweicloud ces alarm-rules create \
  --name high-cpu-alarm \
  --namespace SYS.ECS \
  --metric-name cpu_usage \
  --condition '{"comparisonOperator":">=","threshold":80,"period":300}' \
  --alarm-actions '[{"type":"notification","notificationList":["alarm-action-001"]}]'
```

### 9.2 日志服务 LTS

LTS (Log Tank Service) 收集和分析日志。

**查询日志组**

```bash
huaweicloud lts groups list
```

```json
{
  "log_groups": [
    {
      "log_group_name": "app-logs",
      "id": "group-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00",
      "ttl": 7,
      "log_amount": 15234
    }
  ]
}
```

**创建日志组**

```bash
huaweicloud lts groups create \
  --name kubernetes-logs \
  --ttl 30
```

**创建日志流**

```bash
huaweicloud lts streams create \
  --group-id group-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00 \
  --stream-name web-server \
  --ttl 7
```

**查询日志**

```bash
huaweicloud lts logs query \
  --group-name app-logs \
  --stream-name web-server \
  --query "level:ERROR" \
  --start-time 1747200000000 \
  --end-time 1747286400000 \
  --limit 100
```

---

## 10. 身份与访问管理 IAM

IAM (Identity and Access Management) 控制资源访问权限。

**查询用户列表**

```bash
huaweicloud iam users list
```

```json
{
  "users": [
    {
      "id": "user-4a7ba6ed-5d91-4a91-b1aa-5f2ed2c61a00",
      "name": "developer",
      "email": "dev@example.com",
      "enabled": true,
      "created_at": "2026-01-15T08:00:00Z"
    }
  ]
}
```

**创建用户**

```bash
huaweicloud iam users create \
  --name data-engineer \
  --password "SecureP@ss123" \
  --email "data@example.com"
```

**创建访问密钥**

```bash
huaweicloud iam access-keys create \
  --user-name data-engineer
```

```json
{
  "access_key": "AK7N5MF7HTQ8LH0000000",
  "secret_key": "YdN5TL8uX2vBj9W5L8m3K8W6X7J2H9K4L9M6N8Q",
  "status": "Active",
  "create_time": "2026-05-14T12:00:00Z"
}
```

**绑定用户策略**

```bash
huaweicloud iam users attach-policy \
  --user-name data-engineer \
  --policy-id a2a8c6d9-3e4f-5a6b-8c7d-9e0f1a2b3c4d \
  --policy-type group
```

**创建委托**

```bash
huaweicloud iam agencies create \
  --name cross-account-access \
  --description "Cross account access for CI/CD pipeline" \
  --trust-domain domain-123456 \
  --trust-domain-id 123456789012345678
```

```json
{
  "agency": {
    "id": "agency-8a9b0c1d-2e3f-4a5b-6c7d-8e9f0a1b2c3d",
    "name": "cross-account-access",
    "trust_domain_id": "123456789012345678"
  }
}
```

---

## 11. 附录: 产品 CLI 名称映射表

| 中文名称 | CLI 服务名 | API 命名空间 | 说明 |
|---------|-----------|-------------|------|
| 云服务器 | `ecs` | ECS | Elastic Cloud Server |
| 容器引擎 | `cce` | CCE | Cloud Container Engine |
| 函数工作流 | `functiongraph` | FUNCTIONGRAPH | FaaS 平台 |
| 对象存储 | `obs` | OBS | Object Storage Service |
| 云硬盘 | `evs` | EVS | Elastic Volume Service |
| 文件存储 | `sfs` | SFS | Scalable File Service |
| 关系数据库 | `rds` | RDS | Relational Database Service |
| 分布式缓存 | `redis` | Redis/DCS | Redis Cache Service |
| GaussDB | `gaussdb` | GAUSSDB | 分布式数据库 |
| 文档数据库 | `dds` | DDS | Document Database Service |
| 虚拟私有云 | `vpc` | VPC | Virtual Private Cloud |
| 负载均衡 | `elb` | ELB | Elastic Load Balance |
| NAT网关 | `vpc` | VPC | NAT Gateway |
| CDN | `cdn` | CDN | Content Delivery Network |
| 密钥管理 | `kms` | KMS | Key Management Service |
| 安全组 | `vpc` | VPC | Security Group |
| WAF | `waf` | WAF | Web Application Firewall |
| 消息队列 | `dms` | DMS | Distributed Message Service |
| Kafka | `dms` | DMS | Kafka Message Queue |
| 云监控 | `ces` | CES | Cloud Eye Service |
| 日志服务 | `lts` | LTS | Log Tank Service |
| 身份管理 | `iam` | IAM | Identity and Access Management |
| 密钥管理(新) | `dew` | DEW | Data Encryption Workshop |
| 镜像服务 | `ims` | IMS | Image Management Service |
| 弹性IP | `vpc` | VPC | Elastic IP |
| 域名服务 | `dns` | DNS | Domain Name Service |
| 堡垒机 | `bastionhost` | BASI | Bastion Host |
| 密钥管理 | `kms` | KMS | Key Management Service |
| 证书管理 | `cloudcertificate` | CCM | Cloud Certificate Manager |

**全局参数速查**

```bash
# 常用组合示例
huaweicloud --region cn-north-4 --output json ecs servers list
huaweicloud --profile prod-profile obs ls obs://my-bucket
huaweicloud --project-id 06c6610a361900f22f0c8db61a000000 vpc vpcs list
```

**帮助资源**

- CLI 文档: https://support.huaweicloud.com/cli-reference/
- API 文档: https://developer.huaweicloud.com/
- 区域终端节点: https://developer.huaweicloud.com/endpoint