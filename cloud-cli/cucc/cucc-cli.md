# 联通云CLI命令速查表

> 中国联通联通云命令行工具完整参考手册，覆盖计算、存储、数据库、网络等核心产品线

---

## 1. 安装与配置

### 1.1 安装方法

联通云CLI工具名为`ucc`，可通过以下方式安装：

#### 通过pip安装

```bash
# Python 3.8+
pip install ucc-cli

# 验证安装
ucc version
```

**输出示例：**
```
ucc version 2.3.1
Build Date: 2026-03-15
Python Version: 3.10.12
```

#### 通过安装脚本（Linux/macOS）

```bash
# 下载安装脚本
curl -O https://install.cucloud.cn/ucc-install.sh

# 执行安装
chmod +x ucc-install.sh
sudo ./ucc-install.sh
```

#### 通过yum安装（CentOS/RHEL）

```bash
sudo yum install ucc-cli
```

#### 通过apt安装（Debian/Ubuntu）

```bash
sudo apt-get update
sudo apt-get install ucc-cli
```

### 1.2 配置凭证

首次使用需要配置访问密钥（Access Key）和区域信息：

```bash
# 交互式配置（推荐首次使用）
ucc configure

# 非交互式配置
ucc configure set --access-key AK1234567890ABCDEFGH
ucc configure set --secret-key aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890abcd
ucc configure set --region cn-north-7
```

**输出示例：**
```
Configure success.
Credential:
  Access Key: AK1234567890ABCDEFGH
  Secret Key: ********************************
  Region: cn-north-7
```

#### 凭证配置文件

默认配置文件位于 `~/.cucloud/credentials`：

```ini
[default]
access_key = AK1234567890ABCDEFGH
secret_key = aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890abcd
region = cn-north-7
output_format = json

[profile-dev]
access_key = AKDEV9876543210HIJKLM
secret_key = xYzAbCdEfGhIjKlMnOpQrStUvWxYz0987654321
region = cn-north-7
```

#### 多凭证管理

```bash
# 添加命名凭证
ucc configure add --profile production --access-key AKPRODXXXXXXXXXXXX --secret-key XXXXXXXXXXXXXXXXXXXXXXXXXXXX --region cn-north-7

# 切换凭证
ucc configure use --profile production

# 列出所有凭证
ucc configure list
```

**输出示例：**
```
Available profiles:
  default   - AK1234...DEFGH (cn-north-7)
  production - AKPROD...XXXX (cn-north-7)
  dev       - AKDEV...HIJK (cn-east-1)
```

### 1.3 全局参数

所有命令支持的全局参数：

| 参数 | 说明 | 示例 |
|------|------|------|
| `--profile` | 指定凭证配置 | `--profile production` |
| `--region` | 指定区域 | `--region cn-north-7` |
| `--output` | 输出格式 (json/table/text) | `--output json` |
| `--endpoint` | 自定义API端点 | `--endpoint https://api.cucloud.cn` |
| `--verify-ssl` | 启用SSL验证（默认true） | `--verify-ssl false` |
| `--timeout` | 请求超时（秒） | `--timeout 30` |
| `--debug` | 开启调试模式 | `--debug` |
| `--help` | 显示帮助信息 | `--help` |

```bash
# 组合使用全局参数
ucc ecs DescribeInstances --region cn-north-7 --output json --profile production
```

---

## 2. 计算服务

### 2.1 ECS云服务器

#### 查询实例列表

```bash
ucc ecs DescribeInstances
```

**输出示例：**
```json
{
  "Instances": [
    {
      "InstanceId": "ecs-uf6j3k9m2n7b4c5a",
      "InstanceName": "web-server-01",
      "InstanceType": "ucc.g3.large",
      "Status": "Running",
      "RegionId": "cn-north-7",
      "ZoneId": "cn-north-7a",
      "VpcId": "vpc-uf8k2l3n4m5b6c7d",
      "VSwitchId": "vsw-uf7g5h4j3k2m1n0p",
      "PublicIpAddress": "106.75.123.456",
      "PrivateIpAddress": "192.168.1.100",
      "CreatedTime": "2026-01-15T10:30:00Z",
      "Tags": [
        {"Key": "Environment", "Value": "Production"},
        {"Key": "Project", "Value": "E-Commerce"}
      ]
    },
    {
      "InstanceId": "ecs-uf7k4l5m6n8c9d0e",
      "InstanceName": "db-backup-server",
      "InstanceType": "ucc.g3.xlarge",
      "Status": "Stopped",
      "RegionId": "cn-north-7",
      "ZoneId": "cn-north-7b",
      "VpcId": "vpc-uf8k2l3n4m5b6c7d",
      "VSwitchId": "vsw-uf7g5h4j3k2m1n0p",
      "PublicIpAddress": "",
      "PrivateIpAddress": "192.168.1.200",
      "CreatedTime": "2026-02-20T14:22:00Z",
      "Tags": []
    }
  ],
  "TotalCount": 2,
  "PageNumber": 1,
  "PageSize": 10
}
```

#### 创建实例

```bash
ucc ecs RunInstances \
  --InstanceType ucc.g3.large \
  --ImageId img-uf2k3j4h5g6f7d8c \
  --VSwitchId vsw-uf7g5h4j3k2m1n0p \
  --InstanceName web-server-01 \
  --SecurityGroupId sg-uf1a2b3c4d5e6f7g \
  --InternetMaxBandwidthOut 50 \
  --Password Qwerty123! \
  --Quantity 1
```

**输出示例：**
```json
{
  "InstanceIdSets": [
    "ecs-uf9m8n7k6l5j4i3h"
  ],
  "OrderId": "ORD2026031500001",
  "TotalCount": 1,
  "FeeOfInstance": {
    "InstanceId": "ecs-uf9m8n7k6l5j4i3h",
    "InstanceChargeType": "PostPaid",
    "InternetFee": 0.50,
    "CpuCoreCount": 2,
    "MemorySize": 4
  }
}
```

#### 停止实例

```bash
# 停止单个实例
ucc ecs StopInstances --InstanceId ecs-uf6j3k9m2n7b4c5a

# 停止多个实例
ucc ecs StopInstances --InstanceId.1 ecs-uf6j3k9m2n7b4c5a --InstanceId.2 ecs-uf7k4l5m6n8c9d0e --Force true
```

**输出示例：**
```
Stopping instance(s)...
  ecs-uf6j3k9m2n7b4c5a ............ [Success]
  ecs-uf7k4l5m6n8c9d0e ............ [Success]
Completed: 2, Failed: 0
```

#### 重启实例

```bash
ucc ecs RebootInstances --InstanceId ecs-uf6j3k9m2n7b4c5a --Force true
```

**输出示例：**
```
Rebooting instance ecs-uf6j3k9m2n7b4c5a ...
Instance is rebooting.
```

#### 删除实例

```bash
# 删除单个实例（释放实例）
ucc ecs TerminateInstances --InstanceId ecs-uf7k4l5m6n8c9d0e --Force true
```

**输出示例：**
```
This operation will release the following instance(s):
  ecs-uf7k4l5m6n8c9d0e
Confirm? [y/N]: y
Releasing instance(s)...
  ecs-uf7k4l5m6n8c9d0e ............ [Success]
Instance has been released.
```

#### 查询镜像列表

```bash
# 查询公共镜像
ucc ecs DescribeImages --ImageOwnerCode system

# 查询自定义镜像
ucc ecs DescribeImages --ImageOwnerCode self

# 按镜像ID查询
ucc ecs DescribeImages --ImageId img-uf2k3j4h5g6f7d8c
```

**输出示例：**
```json
{
  "Images": [
    {
      "ImageId": "img-uf2k3j4h5g6f7d8c",
      "ImageName": "Ubuntu 22.04 LTS 64位",
      "ImageOwner": "system",
      "OSName": "Ubuntu 22.04 LTS 64位",
      "Architecture": "x86_64",
      "ImageSize": 40,
      "Status": "Available",
      "CreationTime": "2026-01-10T08:00:00Z"
    },
    {
      "ImageId": "img-uf3l4k5j6h7g8f9e",
      "ImageName": "CentOS 7.9 64位",
      "ImageOwner": "system",
      "OSName": "CentOS 7.9 64位",
      "Architecture": "x86_64",
      "ImageSize": 40,
      "Status": "Available",
      "CreationTime": "2026-01-10T08:00:00Z"
    },
    {
      "ImageId": "img-uf4m5n6k7j8i9h0g",
      "ImageName": "Windows Server 2022 数据中心版",
      "ImageOwner": "system",
      "OSName": "Windows Server 2022 数据中心版",
      "Architecture": "x86_64",
      "ImageSize": 60,
      "Status": "Available",
      "CreationTime": "2026-01-12T08:00:00Z"
    }
  ],
  "TotalCount": 3
}
```

#### 创建云硬盘

```bash
ucc ecs CreateDisk \
  --DiskName data-disk-01 \
  --DiskSize 500 \
  --DiskCategory cloud_efficiency \
  --ZoneId cn-north-7a \
  --Description "业务数据盘"
```

**输出示例：**
```json
{
  "DiskId": "disk-uf5n6o7k8l9m0n1p",
  "DiskName": "data-disk-01",
  "DiskSize": 500,
  "DiskCategory": "cloud_efficiency",
  "ZoneId": "cn-north-7a",
  "Status": "Available",
  "CreationTime": "2026-03-15T10:00:00Z"
}
```

#### 挂载云硬盘

```bash
ucc ecs AttachDisk --DiskId disk-uf5n6o7k8l9m0n1p --InstanceId ecs-uf6j3k9m2n7b4c5a
```

**输出示例：**
```
Attaching disk disk-uf5n6o7k8l9m0n1p to instance ecs-uf6j3k9m2n7b4c5a ...
Disk has been attached successfully.
```

---

### 2.2 容器服务

#### 查询容器集群列表

```bash
ucc cs DescribeClusters
```

**输出示例：**
```json
{
  "Clusters": [
    {
      "ClusterId": "cs-uf8k9l0m1n2o3p4q",
      "ClusterName": "production-k8s-cluster",
      "ClusterType": "Kubernetes",
      "KubernetesVersion": "1.28.5",
      "Status": "Running",
      "RegionId": "cn-north-7",
      "NodeCount": 5,
      "MasterNodeCount": 3,
      "VpcId": "vpc-uf8k2l3n4m5b6c7d",
      "VSwitchIds": ["vsw-uf7g5h4j3k2m1n0p", "vsw-uf8h6i5k4j3l2m1n"],
      "CreatedTime": "2026-01-20T09:00:00Z"
    },
    {
      "ClusterId": "cs-uf9l0m1n2o3p4q5r",
      "ClusterName": "dev-test-cluster",
      "ClusterType": "Kubernetes",
      "KubernetesVersion": "1.27.3",
      "Status": "Running",
      "RegionId": "cn-north-7",
      "NodeCount": 2,
      "MasterNodeCount": 1,
      "VpcId": "vpc-uf8k2l3n4m5b6c7d",
      "VSwitchIds": ["vsw-uf7g5h4j3k2m1n0p"],
      "CreatedTime": "2026-02-15T14:30:00Z"
    }
  ],
  "TotalCount": 2
}
```

#### 创建容器集群

```bash
ucc cs CreateCluster \
  --ClusterName production-k8s-cluster \
  --KubernetesVersion 1.28.5 \
  --VpcId vpc-uf8k2l3n4m5b6c7d \
  --VSwitchId.1 vsw-uf7g5h4j3k2m1n0p \
  --VSwitchId.2 vsw-uf8h6i5k4j3l2m1n \
  --MasterInstanceType ucc.g3.large \
  --MasterInstanceCount 3 \
  --WorkerInstanceType ucc.g3.xlarge \
  --WorkerInstanceCount 5 \
  --ContainerCidr 172.20.0.0/16 \
  --ServiceCidr 172.21.0.0/20
```

**输出示例：**
```json
{
  "ClusterId": "cs-uf0m1n2o3p4q5r6s",
  "ClusterName": "production-k8s-cluster",
  "Status": "Creating",
  "TaskId": "task-uf1n2o3p4q5r6s7t",
  "CreatedTime": "2026-03-15T10:00:00Z",
  "ExpectedTime": "2026-03-15T10:15:00Z"
}
```

#### 扩容容器集群

```bash
# 添加Worker节点
ucc cs ScaleCluster --ClusterId cs-uf8k9l0m1n2o3p4q --WorkerInstanceCount 8

# 添加Master节点（仅支持奇数扩展）
ucc cs ScaleCluster --ClusterId cs-uf8k9l0m1n2o3p4q --MasterInstanceCount 5
```

**输出示例：**
```
Scaling cluster cs-uf8k9l0m1n2o3p4q ...
Current worker count: 5
Target worker count: 8
Adding 3 worker node(s) to cluster ...
  Node instance: ecs-uf2k3l4m5n6o7p8q .... [Success]
  Node instance: ecs-uf3l4m5n6o7p8q9r .... [Success]
  Node instance: ecs-uf4m5n6o7p8q9r0s .... [Success]
Cluster scaling completed.
```

#### 删除容器集群

```bash
ucc cs DeleteCluster --ClusterId cs-uf9l0m1n2o3p4q5r --Force true
```

**输出示例：**
```
Deleting cluster cs-uf9l0m1n2o3p4q5r ...
  Removing worker nodes .... [Success]
  Releasing master nodes .... [Success]
  Cleaning up network resources .... [Success]
Cluster cs-uf9l0m1n2o3p4q5r has been deleted.
```

---

## 3. 存储服务

### 3.1 OBS对象存储

OBS（Object Storage Service）是联通云的对象存储服务，CLI命令以`obs`开头：

#### 列出桶

```bash
# 列出所有存储桶
ucc obs ls

# 详细列表格式
ucc obs ls --long
```

**输出示例：**
```
Bucket Name                   Region         Creation Date         Status
---------------------------   ------------   -------------------   --------
production-assets-bucket      cn-north-7     2026-01-10 08:00:00   Running
backup-data-2026              cn-north-7     2026-01-15 14:30:00   Running
logs-archive                  cn-east-1      2026-02-01 10:00:00   Running
```

#### 创建桶

```bash
# 创建标准存储桶
ucc obs mb obs://my-app-bucket --region cn-north-7

# 创建低频访问存储桶
ucc obs mb obs://infrequent-access-bucket --storage-class IA
```

**输出示例：**
```
Make bucket obs://my-app-bucket ... [Success]
Bucket created: my-app-bucket
Location: cn-north-7
Storage Class: Standard
```

#### 上传文件

```bash
# 上传单个文件
ucc obs cp ./app.tar.gz obs://my-app-bucket/app/v1.0/app.tar.gz

# 上传并设置HTTP头
ucc obs cp ./index.html obs://my-app-bucket/static/index.html \
  --content-type text/html \
  --cache-control "max-age=3600"

# 递归上传目录
ucc obs cp -r ./dist obs://my-app-bucket/static/ \
  --exclude "*.map" \
  --exclude "node_modules/*"
```

**输出示例：**
```
Uploading ./app.tar.gz to obs://my-app-bucket/app/v1.0/app.tar.gz ...
  File Size: 156.32 MB
  Progress: [████████████████████] 100%
  Upload Speed: 12.45 MB/s
  ETag: "d41d8cd98f00b204e9800998ecf8427e"
Upload completed successfully.
```

#### 删除对象

```bash
# 删除单个对象
ucc obs rm obs://my-app-bucket/old-file.txt

# 批量删除（带确认）
ucc obs rm obs://my-app-bucket/temp/*

# 强制删除（不确认）
ucc obs rm obs://my-app-bucket/logs/*.log --force
```

**输出示例：**
```
Deleting object: obs://my-app-bucket/old-file.txt ... [Success]
Deleting objects matching: obs://my-app-bucket/temp/*
  temp/cache.dat .... [Success]
  temp/tmp001.log .... [Success]
  temp/tmp002.log .... [Success]
Deleted 3 objects.
```

#### 同步目录

```bash
# 同步本地目录到OBS（增量同步）
ucc obs sync ./uploads obs://my-app-bucket/user-uploads/ \
  --delete \
  --exclude "*.tmp" \
  --exclude ".DS_Store"
```

**输出示例：**
```
Syncing ./uploads to obs://my-app-bucket/user-uploads/ ...
Comparing file lists ...
  Added:    12 files
  Updated:  5 files
  Deleted:  3 files (remote only)
  Skipped:  156 files (up to date)
Starting sync operation ...
  [████████████████████] 100%
Sync completed.
  Uploaded: 17 files (156.78 MB)
  Deleted:  3 files (remote)
  Duration: 45.23s
```

---

### 3.2 云硬盘

#### 查询云硬盘列表

```bash
ucc ecs DescribeDisks --DiskType all
```

**输出示例：**
```json
{
  "Disks": [
    {
      "DiskId": "disk-uf5n6o7k8l9m0n1p",
      "DiskName": "data-disk-01",
      "DiskType": "Data",
      "DiskCategory": "cloud_efficiency",
      "DiskSize": 500,
      "Status": "In_use",
      "InstanceId": "ecs-uf6j3k9m2n7b4c5a",
      "Device": "/dev/vdb",
      "MountTime": "2026-03-15T10:30:00Z",
      "CreationTime": "2026-03-15T10:00:00Z",
      "AutoSnapshotPolicyId": "asp-uf2k3j4h5g6f"
    },
    {
      "DiskId": "disk-uf6o7p8k9l0m1n2q",
      "DiskName": "backup-disk",
      "DiskType": "Data",
      "DiskCategory": "cloud_ssd",
      "DiskSize": 200,
      "Status": "Available",
      "InstanceId": "",
      "Device": "",
      "MountTime": "",
      "CreationTime": "2026-02-20T11:00:00Z",
      "AutoSnapshotPolicyId": ""
    }
  ],
  "TotalCount": 2,
  "PageNumber": 1,
  "PageSize": 10
}
```

#### 创建云硬盘

```bash
# 创建高效云盘
ucc ecs CreateDisk \
  --DiskName sql-data-disk \
  --DiskSize 1000 \
  --DiskCategory cloud_efficiency \
  --ZoneId cn-north-7a

# 创建SSD云盘
ucc ecs CreateDisk \
  --DiskName redis-data-disk \
  --DiskSize 500 \
  --DiskCategory cloud_ssd \
  --ZoneId cn-north-7a \
  --Encrypted true
```

**输出示例：**
```json
{
  "DiskId": "disk-uf7p8q9k0l1m2n3r",
  "DiskName": "sql-data-disk",
  "DiskSize": 1000,
  "DiskCategory": "cloud_efficiency",
  "ZoneId": "cn-north-7a",
  "Status": "Available",
  "CreationTime": "2026-03-15T10:00:00Z"
}
```

#### 挂载云硬盘

```bash
ucc ecs AttachDisk --DiskId disk-uf7p8q9k0l1m2n3r --InstanceId ecs-uf6j3k9m2n7b4c5a
```

**输出示例：**
```
Attaching disk disk-uf7p8q9k0l1m2n3r to instance ecs-uf6j3k9m2n7b4c5a ...
Device: /dev/vdc
Disk has been attached successfully.
```

---

## 4. 数据库服务

### 4.1 MySQL

#### 查询数据库列表

```bash
ucc rds DescribeDatabases --DBInstanceId mysql-uf1a2b3c4d5e6f
```

**输出示例：**
```json
{
  "Databases": [
    {
      "DBName": "app_production",
      "CharacterSetName": "utf8mb4",
      "Status": "Running",
      "TablesCount": 45,
      "Size": 12.50,
      "CreationTime": "2026-01-15T10:00:00Z"
    },
    {
      "DBName": "app_log",
      "CharacterSetName": "utf8mb4",
      "Status": "Running",
      "TablesCount": 8,
      "Size": 25.30,
      "CreationTime": "2026-01-20T14:30:00Z"
    },
    {
      "DBName": "analytics",
      "CharacterSetName": "utf8mb4",
      "Status": "Running",
      "TablesCount": 23,
      "Size": 156.80,
      "CreationTime": "2026-02-01T09:00:00Z"
    }
  ],
  "TotalCount": 3
}
```

#### 创建数据库

```bash
ucc rds CreateDatabase \
  --DBInstanceId mysql-uf1a2b3c4d5e6f \
  --DBName new_app_db \
  --CharacterSetName utf8mb4 \
  --Description "新应用数据库"
```

**输出示例：**
```json
{
  "DBName": "new_app_db",
  "CharacterSetName": "utf8mb4",
  "Status": "Creating",
  "CreationTime": "2026-03-15T10:00:00Z",
  "Message": "Database creation in progress"
}
```

#### 创建数据库账号

```bash
ucc rds CreateAccount \
  --DBInstanceId mysql-uf1a2b3c4d5e6f \
  --AccountName app_admin \
  --AccountPassword Qwerty123! \
  --Description "应用管理员账号"
```

**输出示例：**
```json
{
  "AccountName": "app_admin",
  "DBInstanceId": "mysql-uf1a2b3c4d5e6f",
  "AccountStatus": "Creating",
  "CreationTime": "2026-03-15T10:05:00Z"
}
```

#### 授权账号权限

```bash
ucc rds GrantPrivilege \
  --DBInstanceId mysql-uf1a2b3c4d5e6f \
  --AccountName app_admin \
  --DBName new_app_db \
  --Privilege ReadWrite
```

**输出示例：**
```
Granting privilege to account app_admin on new_app_db ...
  Privilege: ReadWrite
  Grant completed successfully.
```

#### 创建备份

```bash
# 创建全量备份
ucc rds CreateBackup --DBInstanceId mysql-uf1a2b3c4d5e6f

# 创建指定数据库备份
ucc rds CreateBackup \
  --DBInstanceId mysql-uf1a2b3c4d5e6f \
  --BackupMethod physical \
  --DBName app_production
```

**输出示例：**
```json
{
  "BackupId": "backup-uf2b3c4d5e6f7g8h",
  "DBInstanceId": "mysql-uf1a2b3c4d5e6f",
  "BackupStatus": "Success",
  "BackupType": "FullBackup",
  "BackupMethod": "Logical",
  "BackupSize": 1256.78,
  "BackupStartTime": "2026-03-15T02:00:00Z",
  "BackupEndTime": "2026-03-15T02:15:30Z"
}
```

---

### 4.2 Redis

#### 查询Redis实例列表

```bash
ucc kvstore DescribeInstances --RegionId cn-north-7
```

**输出示例：**
```json
{
  "Instances": [
    {
      "InstanceId": "redis-uf3c4d5e6f7g8h9j",
      "InstanceName": "session-cache-prod",
      "InstanceType": "Redis",
      "EngineVersion": "7.0",
      "Status": "Running",
      "RegionId": "cn-north-7",
      "ZoneId": "cn-north-7a",
      "VpcId": "vpc-uf8k2l3n4m5b6c7d",
      "VSwitchId": "vsw-uf7g5h4j3k2m1n0p",
      "Capacity": 4096,
      "Connections": 1250,
      "QPS": 8500,
      "CreatedTime": "2026-01-10T08:00:00Z"
    },
    {
      "InstanceId": "redis-uf4d5e6f7g8h9j0k",
      "InstanceName": "data-cache-cluster",
      "InstanceType": "Redis Cluster",
      "EngineVersion": "7.0",
      "Status": "Running",
      "RegionId": "cn-north-7",
      "ZoneId": "cn-north-7a",
      "VpcId": "vpc-uf8k2l3n4m5b6c7d",
      "VSwitchId": "vsw-uf7g5h4j3k2m1n0p",
      "Capacity": 16384,
      "Connections": 4500,
      "QPS": 25000,
      "CreatedTime": "2026-02-01T10:00:00Z"
    }
  ],
  "TotalCount": 2
}
```

#### 创建Redis实例

```bash
ucc kvstore CreateInstance \
  --InstanceName user-cache-prod \
  --RegionId cn-north-7 \
  --ZoneId cn-north-7a \
  --VpcId vpc-uf8k2l3n4m5b6c7d \
  --VSwitchId vsw-uf7g5h4j3k2m1n0p \
  --InstanceType Redis \
  --EngineVersion 7.0 \
  --Capacity 8192 \
  --SecurityGroupId sg-uf1a2b3c4d5e6f7g
```

**输出示例：**
```json
{
  "InstanceId": "redis-uf5e6f7g8h9j0k1l",
  "InstanceName": "user-cache-prod",
  "Status": "Creating",
  "OrderId": "ORD2026031500002",
  "ExpectedTime": "2026-03-15T10:20:00Z",
  "Spec": {
    "Capacity": 8192,
    "EngineVersion": "7.0",
    "InstanceType": "Redis"
  }
}
```

---

### 4.3 MongoDB

#### 查询MongoDB实例列表

```bash
ucc mongodb DescribeInstances --RegionId cn-north-7
```

**输出示例：**
```json
{
  "Instances": [
    {
      "InstanceId": "mongodb-uf6f7g8h9j0k1l2m",
      "InstanceName": "content-db-prod",
      "InstanceType": "ReplicaSet",
      "EngineVersion": "6.0",
      "Status": "Running",
      "RegionId": "cn-north-7",
      "ZoneId": "cn-north-7a",
      "VpcId": "vpc-uf8k2l3n4m5b6c7d",
      "VSwitchId": "vsw-uf7g5h4j3k2m1n0p",
      "Capacity": 500,
      "Connections": 450,
      "QPS": 3200,
      "CreatedTime": "2026-01-05T08:00:00Z"
    }
  ],
  "TotalCount": 1
}
```

#### 创建MongoDB实例

```bash
ucc mongodb CreateInstance \
  --InstanceName logs-mongodb \
  --RegionId cn-north-7 \
  --ZoneId cn-north-7a \
  --VpcId vpc-uf8k2l3n4m5b6c7d \
  --VSwitchId vsw-uf7g5h4j3k2m1n0p \
  --InstanceType ReplicaSet \
  --EngineVersion 6.0 \
  --Capacity 200 \
  --NodeCount 3
```

**输出示例：**
```json
{
  "InstanceId": "mongodb-uf7g8h9j0k1l2m3n",
  "InstanceName": "logs-mongodb",
  "Status": "Creating",
  "OrderId": "ORD2026031500003",
  "ExpectedTime": "2026-03-15T10:25:00Z",
  "Spec": {
    "Capacity": 200,
    "EngineVersion": "6.0",
    "InstanceType": "ReplicaSet",
    "NodeCount": 3
  }
}
```

---

## 5. 网络服务

### 5.1 VPC

#### 查询VPC列表

```bash
ucc vpc DescribeVpcs
```

**输出示例：**
```json
{
  "Vpcs": [
    {
      "VpcId": "vpc-uf8k2l3n4m5b6c7d",
      "VpcName": "production-vpc",
      "CidrBlock": "192.168.0.0/16",
      "Status": "Available",
      "RegionId": "cn-north-7",
      "VRouterId": "vrt-uf8k2l3n4m5b6c7d",
      "Description": "生产环境VPC",
      "CreatedTime": "2026-01-01T08:00:00Z"
    },
    {
      "VpcId": "vpc-uf9l3m4n5o6d7e8f",
      "VpcName": "development-vpc",
      "CidrBlock": "10.0.0.0/16",
      "Status": "Available",
      "RegionId": "cn-north-7",
      "VRouterId": "vrt-uf9l3m4n5o6d7e8f",
      "Description": "开发环境VPC",
      "CreatedTime": "2026-01-15T10:00:00Z"
    }
  ],
  "TotalCount": 2
}
```

#### 创建VPC

```bash
ucc vpc CreateVpc \
  --VpcName app-vpc \
  --CidrBlock 172.16.0.0/12 \
  --Description "应用VPC"
```

**输出示例：**
```json
{
  "VpcId": "vpc-uf0m4n5o6p7e8f9g",
  "VpcName": "app-vpc",
  "CidrBlock": "172.16.0.0/12",
  "Status": "Available",
  "VRouterId": "vrt-uf0m4n5o6p7e8f9g",
  "CreatedTime": "2026-03-15T10:00:00Z"
}
```

#### 查询交换机列表

```bash
ucc vpc DescribeVSwitches --VpcId vpc-uf8k2l3n4m5b6c7d
```

**输出示例：**
```json
{
  "VSwitches": [
    {
      "VSwitchId": "vsw-uf7g5h4j3k2m1n0p",
      "VSwitchName": "web-tier-subnet",
      "VpcId": "vpc-uf8k2l3n4m5b6c7d",
      "CidrBlock": "192.168.1.0/24",
      "ZoneId": "cn-north-7a",
      "Status": "Available",
      "AvailableIpAddressCount": 245,
      "CreatedTime": "2026-01-01T08:00:00Z"
    },
    {
      "VSwitchId": "vsw-uf8h6i5k4j3l2m1n",
      "VSwitchName": "app-tier-subnet",
      "VpcId": "vpc-uf8k2l3n4m5b6c7d",
      "CidrBlock": "192.168.2.0/24",
      "ZoneId": "cn-north-7a",
      "Status": "Available",
      "AvailableIpAddressCount": 250,
      "CreatedTime": "2026-01-01T08:00:00Z"
    },
    {
      "VSwitchId": "vsw-uf9i7j6k5l4m3n2o",
      "VSwitchName": "db-tier-subnet",
      "VpcId": "vpc-uf8k2l3n4m5b6c7d",
      "CidrBlock": "192.168.3.0/24",
      "ZoneId": "cn-north-7b",
      "Status": "Available",
      "AvailableIpAddressCount": 250,
      "CreatedTime": "2026-01-01T08:00:00Z"
    }
  ],
  "TotalCount": 3
}
```

#### 创建交换机

```bash
ucc vpc CreateVSwitch \
  --VSwitchName web-subnet \
  --VpcId vpc-uf0m4n5o6p7e8f9g \
  --CidrBlock 172.16.1.0/24 \
  --ZoneId cn-north-7a
```

**输出示例：**
```json
{
  "VSwitchId": "vsw-uf1j8k7l6m5n4o3p",
  "VSwitchName": "web-subnet",
  "VpcId": "vpc-uf0m4n5o6p7e8f9g",
  "CidrBlock": "172.16.1.0/24",
  "ZoneId": "cn-north-7a",
  "Status": "Creating",
  "AvailableIpAddressCount": 253,
  "CreatedTime": "2026-03-15T10:05:00Z"
}
```

#### 创建路由表

```bash
ucc vpc CreateRouteTable \
  --VpcId vpc-uf0m4n5o6p7e8f9g \
  --RouteTableName custom-route-table
```

**输出示例：**
```json
{
  "RouteTableId": "rtb-uf2k8l7m6n5o4p3q",
  "RouteTableName": "custom-route-table",
  "VpcId": "vpc-uf0m4n5o6p7e8f9g",
  "Status": "Available",
  "RouteTableType": "Custom",
  "CreatedTime": "2026-03-15T10:10:00Z"
}
```

---

### 5.2 负载均衡

#### 查询负载均衡实例

```bash
ucc slb DescribeLoadBalancers --RegionId cn-north-7
```

**输出示例：**
```json
{
  "LoadBalancers": [
    {
      "LoadBalancerId": "lb-uf3l8m7n6o5p4q3r",
      "LoadBalancerName": "web-slb-prod",
      "LoadBalancerType": "application",
      "Status": "active",
      "RegionId": "cn-north-7",
      "AddressType": "internet",
      "InternetChargeType": "paybytraffic",
      "VpcId": "vpc-uf8k2l3n4m5b6c7d",
      "VSwitchId": "vsw-uf7g5h4j3k2m1n0p",
      "Address": "106.75.234.123",
      "Port": 80,
      "MasterZoneId": "cn-north-7a",
      "SlaveZoneId": "cn-north-7b",
      "CreatedTime": "2026-01-10T08:00:00Z"
    },
    {
      "LoadBalancerId": "lb-uf4m9n8o6p5q4r2s",
      "LoadBalancerName": "internal-slb",
      "LoadBalancerType": "application",
      "Status": "active",
      "RegionId": "cn-north-7",
      "AddressType": "intranet",
      "VpcId": "vpc-uf8k2l3n4m5b6c7d",
      "VSwitchId": "vsw-uf8h6i5k4j3l2m1n",
      "Address": "192.168.2.100",
      "Port": 8080,
      "MasterZoneId": "cn-north-7a",
      "SlaveZoneId": "cn-north-7b",
      "CreatedTime": "2026-02-01T10:00:00Z"
    }
  ],
  "TotalCount": 2
}
```

#### 创建负载均衡实例

```bash
# 创建公网负载均衡
ucc slb CreateLoadBalancer \
  --LoadBalancerName api-slb-prod \
  --RegionId cn-north-7 \
  --LoadBalancerSpec slb.s2.medium \
  --AddressType internet \
  --InternetChargeType paybybandwidth \
  --Bandwidth 100 \
  --VpcId vpc-uf8k2l3n4m5b6c7d \
  --VSwitchId vsw-uf7g5h4j3k2m1n0p \
  --MasterZoneId cn-north-7a \
  --SlaveZoneId cn-north-7b

# 创建私网负载均衡
ucc slb CreateLoadBalancer \
  --LoadBalancerName internal-api-slb \
  --RegionId cn-north-7 \
  --LoadBalancerSpec slb.s2.small \
  --AddressType intranet \
  --VpcId vpc-uf8k2l3n4m5b6c7d \
  --VSwitchId vsw-uf8h6i5k4j3l2m1n
```

**输出示例：**
```json
{
  "LoadBalancerId": "lb-uf5n9o7p6q5r4s2t",
  "LoadBalancerName": "api-slb-prod",
  "LoadBalancerType": "application",
  "Status": "active",
  "RegionId": "cn-north-7",
  "AddressType": "internet",
  "Address": "106.75.245.134",
  "MasterZoneId": "cn-north-7a",
  "CreatedTime": "2026-03-15T10:00:00Z"
}
```

#### 添加后端服务器

```bash
# 添加后端服务器组
ucc slb RegisterTargets \
  --LoadBalancerId lb-uf3l8m7n6o5p4q3r \
  --BackendServers [
    {"ServerId": "ecs-uf6j3k9m2n7b4c5a", "Port": 80, "Weight": 100},
    {"ServerId": "ecs-uf7k4l5m6n8c9d0e", "Port": 80, "Weight": 100}
  ]
```

**输出示例：**
```
Registering targets to load balancer lb-uf3l8m7n6o5p4q3r ...
  ecs-uf6j3k9m2n7b4c5a:80 .... [Success]
  ecs-uf7k4l5m6n8c9d0e:80 .... [Success]
Registered 2 target(s) successfully.
```

---

### 5.3 弹性IP

#### 查询弹性IP列表

```bash
ucc eip DescribeEips --RegionId cn-north-7
```

**输出示例：**
```json
{
  "EipAddresses": [
    {
      "AllocationId": "eip-uf6o8p9q0r1s2t3u",
      "IpAddress": "106.75.180.250",
      "Status": "InUse",
      "InstanceType": "Ecs",
      "InstanceId": "ecs-uf6j3k9m2n7b4c5a",
      "Bandwidth": 100,
      "InternetChargeType": "paybytraffic",
      "RegionId": "cn-north-7",
      "CreationTime": "2026-01-10T08:00:00Z"
    },
    {
      "AllocationId": "eip-uf7p9q0r1s2t3u4v",
      "IpAddress": "106.75.190.120",
      "Status": "Available",
      "InstanceType": "",
      "InstanceId": "",
      "Bandwidth": 50,
      "InternetChargeType": "paybybandwidth",
      "RegionId": "cn-north-7",
      "CreationTime": "2026-02-15T14:00:00Z"
    }
  ],
  "TotalCount": 2
}
```

#### 申请弹性IP

```bash
# 按流量计费弹性IP
ucc eip AllocateEipAddress \
  --RegionId cn-north-7 \
  --Bandwidth 100 \
  --InternetChargeType paybytraffic

# 按带宽计费弹性IP
ucc eip AllocateEipAddress \
  --RegionId cn-north-7 \
  --Bandwidth 200 \
  --InternetChargeType paybybandwidth \
  --ISP BGP
```

**输出示例：**
```json
{
  "AllocationId": "eip-uf8q0r1s2t3u4v5w",
  "IpAddress": "106.75.200.180",
  "Status": "Available",
  "Bandwidth": 100,
  "InternetChargeType": "paybytraffic",
  "ISP": "BGP",
  "CreationTime": "2026-03-15T10:00:00Z"
}
```

#### 绑定弹性IP

```bash
# 绑定到ECS实例
ucc eip AssociateEipAddress \
  --AllocationId eip-uf8q0r1s2t3u4v5w \
  --InstanceId ecs-uf7k4l5m6n8c9d0e \
  --InstanceType Ecs
```

**输出示例：**
```
Associating EIP eip-uf8q0r1s2t3u4v5w (106.75.200.180) with instance ecs-uf7k4l5m6n8c9d0e ...
EIP has been associated successfully.
```

---

## 6. 监控

### 6.1 云监控

#### 查询监控指标列表

```bash
ucc cms ListMetrics --Namespace acs_ecs_dashboard
```

**输出示例：**
```json
{
  "Metrics": [
    {
      "Namespace": "acs_ecs_dashboard",
      "MetricName": "cpu_utilization",
      "Dimensions": [
        {"InstanceId": "i-uf6j3k9m2n7b4c5a"}
      ],
      "Statistics": ["Average", "Minimum", "Maximum"],
      "Period": 60
    },
    {
      "Namespace": "acs_ecs_dashboard",
      "MetricName": "memory_utilization",
      "Dimensions": [
        {"InstanceId": "i-uf6j3k9m2n7b4c5a"}
      ],
      "Statistics": ["Average", "Minimum", "Maximum"],
      "Period": 60
    },
    {
      "Namespace": "acs_ecs_dashboard",
      "MetricName": "disk_read_bytes",
      "Dimensions": [
        {"InstanceId": "i-uf6j3k9m2n7b4c5a", "Device": "vda"}
      ],
      "Statistics": ["Average", "Sum"],
      "Period": 60
    },
    {
      "Namespace": "acs_ecs_dashboard",
      "MetricName": "network_in_rate",
      "Dimensions": [
        {"InstanceId": "i-uf6j3k9m2n7b4c5a"}
      ],
      "Statistics": ["Average", "Maximum"],
      "Period": 60
    }
  ],
  "TotalCount": 4
}
```

#### 查询监控数据

```bash
# 查询CPU使用率
ucc cms GetMetricData \
  --Namespace acs_ecs_dashboard \
  --MetricName cpu_utilization \
  --Dimensions [{"InstanceId": "ecs-uf6j3k9m2n7b4c5a"}] \
  --StartTime 2026-03-15T00:00:00Z \
  --EndTime 2026-03-15T12:00:00Z \
  --Period 300
```

**输出示例：**
```json
{
  "Code": "Success",
  "Message": "Request successful",
  "RequestId": "req-uf1n2o3p4q5r6s7t",
  "MetricName": "cpu_utilization",
  "Namespace": "acs_ecs_dashboard",
  "Period": 300,
  "Datapoints": [
    {
      "Timestamp": "2026-03-15T00:00:00Z",
      "Average": 23.45,
      "Minimum": 18.20,
      "Maximum": 28.90
    },
    {
      "Timestamp": "2026-03-15T00:05:00Z",
      "Average": 25.10,
      "Minimum": 19.50,
      "Maximum": 32.40
    },
    {
      "Timestamp": "2026-03-15T00:10:00Z",
      "Average": 22.80,
      "Minimum": 17.30,
      "Maximum": 27.60
    }
  ],
  "OriginData": [
    {"instanceId": "ecs-uf6j3k9m2n7b4c5a", "cpu": 23.45}
  ]
}
```

#### 创建告警规则

```bash
# 创建CPU告警
ucc cms CreateAlarm \
  --AlarmName cpu-high-alarm-prod \
  --MetricNamespace acs_ecs_dashboard \
  --MetricName cpu_utilization \
  --Dimensions [{"InstanceId": "ecs-uf6j3k9m2n7b4c5a"}] \
  --Condition "Average >= 80" \
  --Period 300 \
  --EvaluationCount 3 \
  --NotifyType 2 \
  --ContactGroups [{"GroupId": "g-uf1a2b3c4d5e6f"}] \
  --SilenceTime 86400

# 创建内存告警
ucc cms CreateAlarm \
  --AlarmName memory-high-alarm-prod \
  --MetricNamespace acs_ecs_dashboard \
  --MetricName memory_utilization \
  --Dimensions [{"InstanceId": "ecs-uf6j3k9m2n7b4c5a"}] \
  --Condition "Average >= 85" \
  --Period 300 \
  --EvaluationCount 3 \
  --NotifyType 2 \
  --ContactGroups [{"GroupId": "g-uf1a2b3c4d5e6f"}]
```

**输出示例：**
```json
{
  "AlarmId": "alarm-uf2n3o4p5q6r7s8t",
  "AlarmName": "cpu-high-alarm-prod",
  "Status": "enable",
  "MetricNamespace": "acs_ecs_dashboard",
  "MetricName": "cpu_utilization",
  "Condition": "Average >= 80",
  "Period": 300,
  "EvaluationCount": 3,
  "CreatedTime": "2026-03-15T10:00:00Z"
}
```

---

## 7. 资源管理

### 7.1 IAM

#### 查询用户列表

```bash
ucc iam ListUsers
```

**输出示例：**
```json
{
  "Users": [
    {
      "UserId": "u-uf3k4l5m6n7o8p9q",
      "UserName": "devops-admin",
      "DisplayName": "运维管理员",
      "Email": "devops@example.com",
      "Mobile": "+86-138****1234",
      "Status": "Active",
      "CreateDate": "2026-01-01T08:00:00Z",
      "LastLoginDate": "2026-03-14T15:30:00Z"
    },
    {
      "UserId": "u-uf4l5m6n7o8p9q0r",
      "UserName": "app-developer",
      "DisplayName": "应用开发者",
      "Email": "developer@example.com",
      "Mobile": "+86-139****5678",
      "Status": "Active",
      "CreateDate": "2026-01-15T10:00:00Z",
      "LastLoginDate": "2026-03-15T09:15:00Z"
    },
    {
      "UserId": "u-uf5m6n7o8p9q0r1s",
      "UserName": "data-analyst",
      "DisplayName": "数据分析师",
      "Email": "analyst@example.com",
      "Mobile": "+86-136****9012",
      "Status": "Active",
      "CreateDate": "2026-02-01T14:00:00Z",
      "LastLoginDate": "2026-03-10T11:20:00Z"
    }
  ],
  "TotalCount": 3
}
```

#### 创建用户

```bash
ucc iam CreateUser \
  --UserName app-operator \
  --DisplayName "应用运营" \
  --Email operator@example.com \
  --Mobile "+86-137****3456" \
  --Description "应用运营人员"
```

**输出示例：**
```json
{
  "UserId": "u-uf6n7o8p9q0r1s2t",
  "UserName": "app-operator",
  "DisplayName": "应用运营",
  "Email": "operator@example.com",
  "Mobile": "+86-137****3456",
  "Status": "Active",
  "CreateDate": "2026-03-15T10:00:00Z"
}
```

#### 创建访问密钥

```bash
# 为用户创建访问密钥
ucc iam CreateAccessKey --UserName app-operator
```

**输出示例：**
```json
{
  "AccessKey": {
    "AccessKeyId": "AK1234567890OPQRSTU",
    "AccessKeySecret": "aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890",
    "Status": "Active",
    "CreateDate": "2026-03-15T10:05:00Z"
  },
  "Message": "Save the AccessKeySecret. It cannot be retrieved again."
}
```

> **重要提示**: AccessKeySecret只会在创建时返回一次，请妥善保存。若丢失，需要重新创建访问密钥。

---

## 8. 安全服务

### 8.1 密钥管理KMS

#### 查询密钥列表

```bash
ucc kms ListKeys --RegionId cn-east-1
```

**输出示例：**
```json
{
  "Keys": [
    {
      "KeyId": "key-uf1a2b3c4d5e6f7g",
      "KeyArn": "acs:kms:cn-east-1:123456789012:key/key-uf1a2b3c4d5e6f7g",
      "KeyUsage": "ENCRYPT/DECRYPT",
      "KeyStatus": "Enabled",
      "CreateDate": "2026-01-15T10:00:00Z"
    }
  ],
  "TotalCount": 1
}
```

#### 创建密钥

```bash
ucc kms CreateKey --RegionId cn-east-1 --KeyUsage ENCRYPT/DECRYPT
```

**输出示例：**
```json
{
  "KeyId": "key-uf2b3c4d5e6f7g8h",
  "KeyArn": "acs:kms:cn-east-1:123456789012:key/key-uf2b3c4d5e6f7g8h",
  "KeyUsage": "ENCRYPT/DECRYPT",
  "KeyStatus": "Enabled",
  "CreateDate": "2026-03-15T10:00:00Z"
}
```

#### 加密数据

```bash
ucc kms Encrypt --RegionId cn-east-1 --KeyId key-uf2b3c4d5e6f7g8h --Plaintext "SGVsbG8gV29ybGQ="
```

**输出示例：**
```json
{
  "KeyId": "key-uf2b3c4d5e6f7g8h",
  "CiphertextBlob": "Dbase+WQPjFY...",
  "RequestId": "req-uf1n2o3p4q5r6s7t"
}
```

#### 解密数据

```bash
ucc kms Decrypt --RegionId cn-east-1 --KeyId key-uf2b3c4d5e6f7g8h --CiphertextBlob "Dbase+WQPjFY..."
```

**输出示例：**
```json
{
  "KeyId": "key-uf2b3c4d5e6f7g8h",
  "Plaintext": "SGVsbG8gV29ybGQ=",
  "RequestId": "req-uf2o3p4q5r6s7t8u"
}
```

---

### 8.2 安全组

#### 查询安全组

```bash
ucc ecs DescribeSecurityGroups --RegionId cn-east-1
```

**输出示例：**
```json
{
  "SecurityGroups": [
    {
      "SecurityGroupId": "sg-uf1a2b3c4d5e6f7g",
      "SecurityGroupName": "web-sg-prod",
      "VpcId": "vpc-uf8k2l3n4m5b6c7d",
      "SecurityGroupType": "normal",
      "Description": "Web服务器安全组",
      "CreationTime": "2026-01-10T08:00:00Z"
    }
  ],
  "TotalCount": 1
}
```

#### 创建安全组

```bash
ucc ecs CreateSecurityGroup --RegionId cn-east-1 --SecurityGroupName my-sg --VpcId vpc-uf8k2l3n4m5b6c7d
```

**输出示例：**
```json
{
  "SecurityGroupId": "sg-uf2b3c4d5e6f7g8h",
  "SecurityGroupName": "my-sg",
  "VpcId": "vpc-uf8k2l3n4m5b6c7d",
  "CreationTime": "2026-03-15T10:00:00Z"
}
```

#### 添加安全组规则

```bash
# 开放SSH端口
ucc ecs AuthorizeSecurityGroup --RegionId cn-east-1 \
  --SecurityGroupId sg-uf2b3c4d5e6f7g8h \
  --IpProtocol tcp \
  --PortRange 22/22 \
  --SourceCidrIp 0.0.0.0/0

# 开放HTTP/HTTPS端口
ucc ecs AuthorizeSecurityGroup --RegionId cn-east-1 \
  --SecurityGroupId sg-uf2b3c4d5e6f7g8h \
  --IpProtocol tcp \
  --PortRange 80/80 \
  --SourceCidrIp 0.0.0.0/0
```

**输出示例：**
```
Authorizing security group sg-uf2b3c4d5e6f7g8h ...
  Rule added: tcp 22/22 from 0.0.0.0/0 .... [Success]
Security group rule added successfully.
```

---

## 9. 中间件服务

### 9.1 Kafka消息队列

#### 查询Kafka实例

```bash
ucc kafka DescribeInstances --RegionId cn-east-1
```

**输出示例：**
```json
{
  "Instances": [
    {
      "InstanceId": "kafka-uf1a2b3c4d5e6f",
      "InstanceName": "log-kafka-prod",
      "RegionId": "cn-east-1",
      "ZoneId": "cn-east-1a",
      "VpcId": "vpc-uf8k2l3n4m5b6c7d",
      "VSwitchId": "vsw-uf7g5h4j3k2m1n0p",
      "Status": "Running",
      "DiskType": "cloud_ssd",
      "DiskSize": 1200,
      "ProduceQuota": 50,
      "ConsumeQuota": 100,
      "CreatedTime": "2026-01-20T10:00:00Z"
    }
  ],
  "TotalCount": 1
}
```

#### 创建Topic

```bash
ucc kafka CreateTopic --RegionId cn-east-1 \
  --InstanceId kafka-uf1a2b3c4d5e6f \
  --Topic my-topic \
  --Partitions 6 \
  --ReplicationFactor 3
```

**输出示例：**
```json
{
  "TopicId": "topic-uf2b3c4d5e6f7g",
  "Topic": "my-topic",
  "InstanceId": "kafka-uf1a2b3c4d5e6f",
  "Partitions": 6,
  "ReplicationFactor": 3,
  "Status": "Running",
  "CreationTime": "2026-03-15T10:05:00Z"
}
```

#### 查询Topic列表

```bash
ucc kafka DescribeTopics --RegionId cn-east-1 --InstanceId kafka-uf1a2b3c4d5e6f
```

**输出示例：**
```json
{
  "TopicList": [
    {
      "Topic": "my-topic",
      "Partitions": 6,
      "ReplicationFactor": 3,
      "BrokerList": [
        {"BrokerId": 0, "Host": "192.168.1.100", "Port": 9092},
        {"BrokerId": 1, "Host": "192.168.1.101", "Port": 9092},
        {"BrokerId": 2, "Host": "192.168.1.102", "Port": 9092}
      ]
    }
  ],
  "TotalCount": 1
}
```

---

### 9.2 RabbitMQ消息队列

#### 查询RabbitMQ实例

```bash
ucc rabbitmq DescribeInstances --RegionId cn-east-1
```

**输出示例：**
```json
{
  "Instances": [
    {
      "InstanceId": "rabbitmq-uf1a2b3c4d5e6f",
      "InstanceName": "order-queue-prod",
      "RegionId": "cn-east-1",
      "ZoneId": "cn-east-1a",
      "VpcId": "vpc-uf8k2l3n4m5b6c7d",
      "VSwitchId": "vsw-uf7g5h4j3k2m1n0p",
      "Status": "Running",
      "NodeCount": 3,
      "Specifications": "rabbitmq.enterprise.x4",
      "CreatedTime": "2026-01-25T10:00:00Z"
    }
  ],
  "TotalCount": 1
}
```

#### 创建队列

```bash
ucc rabbitmq CreateQueue --RegionId cn-east-1 \
  --InstanceId rabbitmq-uf1a2b3c4d5e6f \
  --QueueName order-queue \
  --Durable true
```

**输出示例：**
```json
{
  "QueueName": "order-queue",
  "InstanceId": "rabbitmq-uf1a2b3c4d5e6f",
  "Durable": true,
  "AutoDelete": false,
  "Status": "Running",
  "CreationTime": "2026-03-15T10:10:00Z"
}
```

#### 查询队列列表

```bash
ucc rabbitmq DescribeQueues --RegionId cn-east-1 --InstanceId rabbitmq-uf1a2b3c4d5e6f
```

**输出示例：**
```json
{
  "QueueList": [
    {
      "QueueName": "order-queue",
      "Durable": true,
      "MessageCount": 1250,
      "ConsumerCount": 3
    }
  ],
  "TotalCount": 1
}
```

---

## 10. 附录：产品CLI名称映射表

### 10.1 服务模块与CLI命令前缀

| 产品线 | CLI前缀 | 服务说明 |
|--------|---------|----------|
| 计算 | `ucc ecs` | 云服务器ECS |
| 容器服务 | `ucc cs` | 容器服务Kubernetes |
| 对象存储 | `ucc obs` | 对象存储服务 |
| 云硬盘 | `ucc ecs` | 云硬盘（ECS模块） |
| 关系型数据库 | `ucc rds` | MySQL/PostgreSQL |
| 键值存储 | `ucc kvstore` | Redis |
| 文档数据库 | `ucc mongodb` | MongoDB |
| 虚拟私有云 | `ucc vpc` | VPC网络 |
| 负载均衡 | `ucc slb` | 负载均衡SLB |
| 弹性IP | `ucc eip` | 弹性公网IP |
| 云监控 | `ucc cms` | 云监控服务 |
| 身份认证 | `ucc iam` | 身份认证管理 |
| 密钥管理 | `ucc kms` | 密钥管理服务 |
| 安全组 | `ucc ecs` | 安全组（ECS模块） |
| Kafka消息队列 | `ucc kafka` | Kafka消息队列 |
| RabbitMQ消息队列 | `ucc rabbitmq` | RabbitMQ消息队列 |

### 10.2 常用命令速查表

| 功能 | 命令 |
|------|------|
| 配置凭证 | `ucc configure` |
| 查询实例 | `ucc ecs DescribeInstances` |
| 创建实例 | `ucc ecs RunInstances` |
| 停止实例 | `ucc ecs StopInstances` |
| 重启实例 | `ucc ecs RebootInstances` |
| 删除实例 | `ucc ecs TerminateInstances` |
| 查询镜像 | `ucc ecs DescribeImages` |
| 创建硬盘 | `ucc ecs CreateDisk` |
| 挂载硬盘 | `ucc ecs AttachDisk` |
| 查询桶列表 | `ucc obs ls` |
| 创建桶 | `ucc obs mb` |
| 上传文件 | `ucc obs cp` |
| 删除对象 | `ucc obs rm` |
| 同步文件 | `ucc obs sync` |
| 查询VPC | `ucc vpc DescribeVpcs` |
| 创建VPC | `ucc vpc CreateVpc` |
| 查询交换机 | `ucc vpc DescribeVSwitches` |
| 创建交换机 | `ucc vpc CreateVSwitch` |
| 查询SLB | `ucc slb DescribeLoadBalancers` |
| 创建SLB | `ucc slb CreateLoadBalancer` |
| 查询EIP | `ucc eip DescribeEips` |
| 申请EIP | `ucc eip AllocateEipAddress` |
| 绑定EIP | `ucc eip AssociateEipAddress` |
| 查询监控指标 | `ucc cms ListMetrics` |
| 查询监控数据 | `ucc cms GetMetricData` |
| 创建告警 | `ucc cms CreateAlarm` |
| 查询用户 | `ucc iam ListUsers` |
| 创建用户 | `ucc iam CreateUser` |
| 创建访问密钥 | `ucc iam CreateAccessKey` |

### 10.3 区域代码对照表

| 区域代码 | 区域名称 |
|----------|----------|
| cn-north-7 | 华北一（廊坊） |
| cn-north-9 | 华北二（北京） |
| cn-east-1 | 华东一（上海） |
| cn-east-2 | 华东二（杭州） |
| cn-south-1 | 华南一（广州） |
| cn-south-2 | 华南二（深圳） |
| cn-central-1 | 华中一（武汉） |
| cn-northwest-1 | 西北一（西安） |
| cn-southwest-1 | 西南一（成都） |

### 10.4 实例类型对照表

| 类型族 | 说明 | 适用场景 |
|--------|------|----------|
| ucc.g3.large | 通用型 2核4G | Web应用、中小型数据库 |
| ucc.g3.xlarge | 通用型 4核8G | 应用服务器、中等负载 |
| ucc.g3.2xlarge | 通用型 8核16G | 高负载应用、数据处理 |
| ucc.c3.large | 计算型 2核4G | 计算密集型应用 |
| ucc.c3.xlarge | 计算型 4核8G | 高性能计算、HPC |
| ucc.m3.large | 内存型 2核8G | 缓存服务器、Redis |
| ucc.m3.xlarge | 内存型 4核16G | 大型缓存、内存数据库 |
| ucc.s3.large | 存储型 2核4G | 日志处理、大数据分析 |
| ucc.s3.xlarge | 存储型 4核8G | 文件服务器、数据仓库 |
| ucc.ga3.large | GPU型 2核4G + T4 | AI推理、图形渲染 |
| ucc.ga3.xlarge | GPU型 4核8G + T4 | 深度学习、图形计算 |

---

## 11. 附录：快速参考

### 获取帮助

```bash
# 查看全局帮助
ucc help

# 查看子服务帮助
ucc ecs help

# 查看具体命令帮助
ucc ecs DescribeInstances help
```

### 输出格式

```bash
# JSON格式（默认）
ucc ecs DescribeInstances --output json

# 表格格式
ucc ecs DescribeInstances --output table

# 纯文本格式
ucc ecs DescribeInstances --output text
```

### 常用组合示例

```bash
# 一键创建Web应用环境
ucc ecs RunInstances --InstanceType ucc.g3.large --ImageId img-uf2k3j4h5g6f7d8c --InstanceName web-01 --SecurityGroupId sg-uf1a2b3c4d5e6f7g && \
ucc eip AllocateEipAddress --Bandwidth 100 && \
ucc slb CreateLoadBalancer --LoadBalancerName web-slb && \
ucc cms CreateAlarm --AlarmName web-cpu-alarm --MetricName cpu_utilization --Condition "Average >= 80"

# 批量关闭开发环境
ucc ecs DescribeInstances --Tag "Environment=Development" --output json | jq -r '.Instances[].InstanceId' | xargs -I {} ucc ecs StopInstances --InstanceId {}

# 查看本月费用
ucc billing QueryMonthBill --BillingCycle 2026-03
```

---

> **文档版本**: v1.0
> **最后更新**: 2026年3月
> **联通云CLI版本**: 2.3.1+