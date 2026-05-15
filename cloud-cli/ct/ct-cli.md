# 电信云CLI命令速查表

> 中国电信天翼云命令行工具完整参考手册，覆盖计算、存储、数据库、网络等核心产品线

---

## 1. 安装与配置

### 安装方法

```bash
# Linux/macOS 安装
curl -O https://ctccLOUD-cli-cn-east-1.s3.cn-east-1.amazonaws.com.cn/ctcli/latest/ctcli-linux-amd64.tar.gz
tar -xzf ctcli-linux-amd64.tar.gz
sudo ./ctcli install

# macOS Homebrew 安装
brew install ctcloud/tap/ctcli

# 验证安装
ctcli version
```

**输出示例:**
```
CT-CLI v3.2.1
Build: 2026-04-15T08:30:00+0800
Go Version: go1.21.8
```

### 配置凭证

```bash
# 交互式配置（推荐首次使用）
ctcli configure

# 非交互式配置
ctcli configure set --access-key AKTP1a2b3c4d5e6f7g8h9i0j
ctcli configure set --secret-key SKTPxxxxxxxxxxxxxxxxxxxxxx
ctcli configure set --region cn-east-1
ctcli configure set --output json

# 查看当前配置
ctcli configure list
```

**输出示例:**
```
[default]
access-key = AKTP1a2b3c4d5e6f7g8h9i0j
secret-key = ********************
region = cn-east-1
output = json
```

### 全局参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--region` | 地域ID | `--region cn-north-1` |
| `--access-key` | 访问密钥 | `--access-key AKTPxxxx` |
| `--secret-key` | 密钥Secret | `--secret-key SKTPxxxx` |
| `--output` | 输出格式 | `--output json/yaml/table` |
| `--endpoint` | 自定义端点 | `--endpoint https://ctcc.cn-east-1.ctyunapi.cn` |
| `--profile` | 配置文件 Profile | `--profile production` |
| `--verbose` | 详细输出 | `--verbose` |
| `--page-size` | 分页大小 | `--page-size 100` |

```bash
# 使用指定Profile执行命令
ctcli ecs DescribeInstances --profile production

# 指定地域和输出格式
ctcli ecs DescribeInstances --region cn-south-1 --output table
```

---

## 2. 计算服务

### ECS云服务器

#### 查询云服务器实例列表

```bash
ctcli ecs DescribeInstances --region cn-east-1
```

**输出示例:**
```json
{
  "InstanceSets": [
    {
      "InstanceId": "i-xxxxxxxxxxx01",
      "InstanceName": "web-server-01",
      "InstanceType": "s6.large.2",
      "Status": "Running",
      "PublicIpAddress": ["180.x.x.x"],
      "PrivateIpAddress": ["192.168.1.10"],
      "VpcId": "vpc-xxxxxxxx",
      "VSwitchId": "vsw-xxxxxxxx",
      "CreatedTime": "2026-03-15T10:30:00Z",
      "ExpiredTime": "2027-03-15T10:30:00Z"
    },
    {
      "InstanceId": "i-xxxxxxxxxxx02",
      "InstanceName": "db-server-01",
      "InstanceType": "s6.xlarge.4",
      "Status": "Running",
      "PublicIpAddress": [],
      "PrivateIpAddress": ["192.168.1.20"],
      "VpcId": "vpc-xxxxxxxx",
      "VSwitchId": "vsw-xxxxxxxx",
      "CreatedTime": "2026-02-20T14:20:00Z",
      "ExpiredTime": "2027-02-20T14:20:00Z"
    }
  ],
  "TotalCount": 2,
  "PageSize": 10,
  "PageNumber": 1
}
```

#### 创建云服务器实例

```bash
ctcli ecs RunInstances \
  --InstanceType s6.large.2 \
  --ImageId img-xxxxxxxx \
  --VSwitchId vsw-xxxxxxxx \
  --SecurityGroupId sg-xxxxxxxx \
  --InstanceName web-server-new \
  --InternetMaxBandwidthOut 50 \
  --Password P@ssw0rd123 \
  --Count 1
```

**输出示例:**
```json
{
  "InstanceIdSet": ["i-xxxxxxxxxxx03"],
  "OrderId": "ORDER-202603150001",
  "RequestId": "f0e1d2c3-b4a5-6f7e-8d9c-0b1a2c3d4e5f"
}
```

#### 停止云服务器实例

```bash
ctcli ecs StopInstances --InstanceId.1 i-xxxxxxxxxxx01 --Force false
```

**输出示例:**
```json
{
  "RequestId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "InstanceIdSet": ["i-xxxxxxxxxxx01"],
  "PreviousStatus": "Running",
  "CurrentStatus": "Stopping"
}
```

#### 重启云服务器实例

```bash
ctcli ecs RebootInstances --InstanceId.1 i-xxxxxxxxxxx01 --Force false
```

**输出示例:**
```json
{
  "RequestId": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
  "InstanceIdSet": ["i-xxxxxxxxxxx01"],
  "PreviousStatus": "Running",
  "CurrentStatus": "Rebooting"
}
```

#### 删除云服务器实例

```bash
ctcli ecs TerminateInstances --InstanceId.1 i-xxxxxxxxxxx03 --Force false
```

**输出示例:**
```json
{
  "RequestId": "c3d4e5f6-a7b8-9012-cdef-345678901234",
  "InstanceIdSet": ["i-xxxxxxxxxxx03"]
}
```

#### 查询可用镜像

```bash
ctcli ecs DescribeImages --RegionId cn-east-1 --ImageOwner self
```

**输出示例:**
```json
{
  "Images": [
    {
      "ImageId": "img-ubuntu2204-lts",
      "ImageName": "Ubuntu 22.04 LTS 64位",
      "OsName": "Ubuntu 22.04 LTS",
      "Architecture": "x86_64",
      "ImageOwner": "self",
      "Status": "Available",
      "CreatedTime": "2026-01-10T08:00:00Z"
    },
    {
      "ImageId": "img-centos7u9",
      "ImageName": "CentOS 7.9 64位",
      "OsName": "CentOS 7.9",
      "Architecture": "x86_64",
      "ImageOwner": "self",
      "Status": "Available",
      "CreatedTime": "2026-01-08T08:00:00Z"
    }
  ],
  "TotalCount": 2
}
```

#### 创建云硬盘

```bash
ctcli ecs CreateDisk \
  --DiskName data-disk-01 \
  --DiskSize 500 \
  --DiskCategory cloud_ssd \
  --ZoneId cn-east-1a
```

**输出示例:**
```json
{
  "DiskId": "disk-xxxxxxxx01",
  "RequestId": "d4e5f6a7-b8c9-0123-defa-456789012345",
  "OrderId": "ORDER-202603150002"
}
```

#### 挂载云硬盘

```bash
ctcli ecs AttachDisk --InstanceId i-xxxxxxxxxxx01 --DiskId disk-xxxxxxxx01
```

**输出示例:**
```json
{
  "RequestId": "e5f6a7b8-c9d0-1234-efab-567890123456",
  "InstanceId": "i-xxxxxxxxxxx01",
  "DiskId": "disk-xxxxxxxx01",
  "Status": "attaching"
}
```

### 容器服务

#### 查询容器集群列表

```bash
ctcli cs DescribeClusters
```

**输出示例:**
```json
{
  "Clusters": [
    {
      "ClusterId": "ccs-xxxxxxxx01",
      "ClusterName": "production-cluster",
      "ClusterType": "ManagedKubernetes",
      "KubernetesVersion": "1.28",
      "Status": "Running",
      "NodeCount": 5,
      "VpcId": "vpc-xxxxxxxx",
      "CreatedTime": "2026-02-01T09:00:00Z"
    }
  ],
  "TotalCount": 1
}
```

#### 创建容器集群

```bash
ctcli cs CreateCluster \
  --ClusterName production-cluster \
  --ClusterType ManagedKubernetes \
  --KubernetesVersion 1.28 \
  --VpcId vpc-xxxxxxxx \
  --VSwitchIds vsw-xxxxxxxx01,vsw-xxxxxxxx02 \
  --ContainerRuntime containerd \
  --NodeCount 3
```

**输出示例:**
```json
{
  "ClusterId": "ccs-xxxxxxxx02",
  "RequestId": "f6a7b8c9-d0e1-2345-fabc-678901234567",
  "TaskId": "task-xxxxxxxx",
  "Status": "Creating"
}
```

#### 扩容容器集群

```bash
ctcli cs ScaleCluster --ClusterId ccs-xxxxxxxx01 --NodeCount 8
```

**输出示例:**
```json
{
  "RequestId": "a7b8c9d0-e1f2-3456-abcd-789012345678",
  "ClusterId": "ccs-xxxxxxxx01",
  "DesiredNodeCount": 8,
  "CurrentNodeCount": 5,
  "TaskId": "task-yyyyyyyy"
}
```

#### 删除容器集群

```bash
ctcli cs DeleteCluster --ClusterId ccs-xxxxxxxx02 --Force true
```

**输出示例:**
```json
{
  "RequestId": "b8c9d0e1-f2a3-4567-bcde-890123456789",
  "ClusterId": "ccs-xxxxxxxx02",
  "Status": "Deleting"
}
```

---

## 3. 存储服务

### OBS对象存储

OBS（Object Storage Service）是电信云的对象存储服务，支持多种命令操作。

#### 列出桶列表

```bash
ctcli obs ls
```

**输出示例:**
```
2026-03-15 10:30:00  bucket-app-logs
2026-03-10 14:20:00  bucket-media-files
2026-02-28 09:15:00  bucket-backup-data
```

#### 创建桶

```bash
ctcli obs mb obs://bucket-app-logs --region cn-east-1
```

**输出示例:**
```
Make bucket successfully
Bucket: bucket-app-logs
Region: cn-east-1
```

#### 上传对象

```bash
ctcli obs cp ./app.log obs://bucket-app-logs/logs/$(date +%Y%m%d)/app.log
```

**输出示例:**
```
upload: ./app.log -> obs://bucket-app-logs/logs/20260315/app.log
ETag: "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
```

#### 删除对象

```bash
ctcli obs rm obs://bucket-app-logs/logs/20260310/app.log
```

**输出示例:**
```
Delete object obs://bucket-app-logs/logs/20260310/app.log successfully
```

#### 同步目录

```bash
ctcli obs sync ./backup-data obs://bucket-backup-data/backup/ --region cn-east-1
```

**输出示例:**
```
Syncing...
Upload: backup-data/file001.tar.gz -> obs://bucket-backup-data/backup/file001.tar.gz
Upload: backup-data/file002.tar.gz -> obs://bucket-backup-data/backup/file002.tar.gz
Upload: backup-data/file003.tar.gz -> obs://bucket-backup-data/backup/file003.tar.gz
Sync completed. 3 objects uploaded.
```

### 云硬盘

#### 查询云硬盘列表

```bash
ctcli ecs DescribeDisks --RegionId cn-east-1
```

**输出示例:**
```json
{
  "Disks": [
    {
      "DiskId": "disk-xxxxxxxx01",
      "DiskName": "data-disk-01",
      "DiskType": "data",
      "DiskCategory": "cloud_ssd",
      "DiskSize": 500,
      "Status": "In_use",
      "InstanceId": "i-xxxxxxxxxxx01",
      "CreatedTime": "2026-03-15T11:00:00Z",
      "ExpiredTime": "2027-03-15T11:00:00Z"
    },
    {
      "DiskId": "disk-xxxxxxxx02",
      "DiskName": "system-disk",
      "DiskType": "system",
      "DiskCategory": "cloud_efficiency",
      "DiskSize": 40,
      "Status": "In_use",
      "InstanceId": "i-xxxxxxxxxxx01",
      "CreatedTime": "2026-01-10T08:00:00Z",
      "ExpiredTime": "2027-01-10T08:00:00Z"
    }
  ],
  "TotalCount": 2
}
```

#### 创建云硬盘

```bash
ctcli ecs CreateDisk \
  --DiskName backup-disk \
  --DiskSize 1000 \
  --DiskCategory cloud_efficiency \
  --ZoneId cn-east-1a \
  --RegionId cn-east-1
```

**输出示例:**
```json
{
  "DiskId": "disk-xxxxxxxx03",
  "RequestId": "c9d0e1f2-a3b4-4567-cdef-901234567890",
  "OrderId": "ORDER-202603150003"
}
```

#### 挂载云硬盘

```bash
ctcli ecs AttachDisk --InstanceId i-xxxxxxxxxxx02 --DiskId disk-xxxxxxxx03
```

**输出示例:**
```json
{
  "RequestId": "d0e1f2a3-b4c5-5678-defa-012345678901",
  "InstanceId": "i-xxxxxxxxxxx02",
  "DiskId": "disk-xxxxxxxx03",
  "Status": "attaching"
}
```

---

## 4. 数据库服务

### MySQL

#### 查询数据库列表

```bash
ctcli rds DescribeDatabases --DBInstanceId rm-xxxxxxxx01
```

**输出示例:**
```json
{
  "Databases": [
    {
      "DatabaseName": "app_production",
      "CharacterSetName": "utf8mb4",
      "Status": "Running",
      "TablesCount": 45,
      "Size": 21474836480
    },
    {
      "DatabaseName": "app_staging",
      "CharacterSetName": "utf8mb4",
      "Status": "Running",
      "TablesCount": 38,
      "Size": 5368709120
    }
  ],
  "TotalCount": 2
}
```

#### 创建数据库

```bash
ctcli rds CreateDatabase \
  --DBInstanceId rm-xxxxxxxx01 \
  --DatabaseName app_new \
  --CharacterSetName utf8mb4 \
  --Description "New application database"
```

**输出示例:**
```json
{
  "RequestId": "e1f2a3b4-c5d6-7890-efab-123456789012",
  "DatabaseName": "app_new",
  "Status": "Creating"
}
```

#### 创建数据库账号

```bash
ctcli rds CreateAccount \
  --DBInstanceId rm-xxxxxxxx01 \
  --AccountName appadmin \
  --AccountPassword P@ssw0rd!2026 \
  --AccountType Normal
```

**输出示例:**
```json
{
  "RequestId": "f2a3b4c5-d6e7-8901-fabc-234567890123",
  "AccountName": "appadmin",
  "AccountStatus": "Creating"
}
```

#### 授权账号数据库权限

```bash
ctcli rds GrantPrivilege \
  --DBInstanceId rm-xxxxxxxx01 \
  --AccountName appadmin \
  --DBName app_production \
  --Privilege Execute,Insert,Update,Delete
```

**输出示例:**
```json
{
  "RequestId": "a3b4c5d6-e7f8-9012-abcd-345678901234",
  "DBPrivileges": [
    {
      "DBName": "app_production",
      "AccountName": "appadmin",
      "Privilege": "Execute,Insert,Update,Delete"
    }
  ]
}
```

#### 创建数据库备份

```bash
ctcli rds CreateBackup \
  --DBInstanceId rm-xxxxxxxx01 \
  --BackupMethod Physical \
  --Description "Manual backup before upgrade"
```

**输出示例:**
```json
{
  "BackupId": "backup-xxxxxxxx01",
  "RequestId": "b4c5d6e7-f8a9-0123-bcde-456789012345",
  "Status": "Preparing"
}
```

### Redis

#### 查询Redis实例列表

```bash
ctcli redis DescribeInstances --RegionId cn-east-1
```

**输出示例:**
```json
{
  "Instances": [
    {
      "InstanceId": "redis-xxxxxxxx01",
      "InstanceName": "cache-production",
      "InstanceType": "redis_master",
      "Capacity": 4096,
      "QPS": 100000,
      "Connections": 10000,
      "Status": "Running",
      "ZoneId": "cn-east-1a",
      "VpcId": "vpc-xxxxxxxx",
      "CreatedTime": "2026-02-15T10:00:00Z",
      "ExpiredTime": "2027-02-15T10:00:00Z"
    }
  ],
  "TotalCount": 1
}
```

#### 创建Redis实例

```bash
ctcli redis CreateInstance \
  --InstanceName cache-cluster \
  --RegionId cn-east-1 \
  --ZoneId cn-east-1a \
  --VpcId vpc-xxxxxxxx \
  --VSwitchId vsw-xxxxxxxx \
  --Capacity 8192 \
  --InstanceType redis_master \
  --Password P@ssw0rd!Redis
```

**输出示例:**
```json
{
  "InstanceId": "redis-xxxxxxxx02",
  "RequestId": "c5d6e7f8-a9b0-1234-cdef-567890123456",
  "OrderId": "ORDER-202603150004",
  "Status": "Creating"
}
```

### MongoDB

#### 查询MongoDB实例列表

```bash
ctcli mongodb DescribeInstances --RegionId cn-east-1
```

**输出示例:**
```json
{
  "Instances": [
    {
      "InstanceId": "mongodb-xxxxxxxx01",
      "InstanceName": "mongo-production",
      "InstanceType": "replicate_set",
      "Capacity": 100,
      "EngineVersion": "6.0",
      "Status": "Running",
      "ZoneId": "cn-east-1a",
      "VpcId": "vpc-xxxxxxxx",
      "ReplicaSetStatus": {
        "Primary": "192.168.1.100:27017",
        "Secondary": ["192.168.1.101:27017", "192.168.1.102:27017"]
      }
    }
  ],
  "TotalCount": 1
}
```

#### 创建MongoDB实例

```bash
ctcli mongodb CreateInstance \
  --InstanceName mongo-cluster \
  --RegionId cn-east-1 \
  --ZoneId cn-east-1a \
  --VpcId vpc-xxxxxxxx \
  --VSwitchId vsw-xxxxxxxx \
  --Capacity 200 \
  --InstanceType replicate_set \
  --EngineVersion 6.0 \
  --Password P@ssw0rd!Mongo
```

**输出示例:**
```json
{
  "InstanceId": "mongodb-xxxxxxxx02",
  "RequestId": "d6e7f8a9-b0c1-2345-defa-678901234567",
  "OrderId": "ORDER-202603150005",
  "Status": "Creating"
}
```

---

## 5. 网络服务

### VPC

#### 查询VPC列表

```bash
ctcli vpc DescribeVpcs --RegionId cn-east-1
```

**输出示例:**
```json
{
  "Vpcs": [
    {
      "VpcId": "vpc-xxxxxxxx01",
      "VpcName": "production-vpc",
      "CidrBlock": "192.168.0.0/16",
      "Status": "Available",
      "CreatedTime": "2026-01-15T09:00:00Z"
    },
    {
      "VpcId": "vpc-xxxxxxxx02",
      "VpcName": "development-vpc",
      "CidrBlock": "10.0.0.0/16",
      "Status": "Available",
      "CreatedTime": "2026-02-20T14:30:00Z"
    }
  ],
  "TotalCount": 2
}
```

#### 创建VPC

```bash
ctcli vpc CreateVpc \
  --VpcName web-vpc \
  --CidrBlock 172.16.0.0/12 \
  --RegionId cn-east-1
```

**输出示例:**
```json
{
  "VpcId": "vpc-xxxxxxxx03",
  "VpcName": "web-vpc",
  "CidrBlock": "172.16.0.0/12",
  "RequestId": "e7f8a9b0-c1d2-3456-efab-789012345678",
  "Status": "Pending"
}
```

#### 查询交换机列表

```bash
ctcli vpc DescribeVSwitches --VpcId vpc-xxxxxxxx01 --RegionId cn-east-1
```

**输出示例:**
```json
{
  "VSwitches": [
    {
      "VSwitchId": "vsw-xxxxxxxx01",
      "VSwitchName": "subnet-web",
      "CidrBlock": "192.168.1.0/24",
      "ZoneId": "cn-east-1a",
      "Status": "Available",
      "AvailableIpAddressCount": 250
    },
    {
      "VSwitchId": "vsw-xxxxxxxx02",
      "VSwitchName": "subnet-db",
      "CidrBlock": "192.168.2.0/24",
      "ZoneId": "cn-east-1b",
      "Status": "Available",
      "AvailableIpAddressCount": 250
    }
  ],
  "TotalCount": 2
}
```

#### 创建交换机

```bash
ctcli vpc CreateVSwitch \
  --VpcId vpc-xxxxxxxx01 \
  --CidrBlock 192.168.3.0/24 \
  --ZoneId cn-east-1c \
  --VSwitchName subnet-app
```

**输出示例:**
```json
{
  "VSwitchId": "vsw-xxxxxxxx03",
  "VSwitchName": "subnet-app",
  "CidrBlock": "192.168.3.0/24",
  "ZoneId": "cn-east-1c",
  "RequestId": "f8a9b0c1-d2e3-4567-fabc-890123456789",
  "Status": "Pending"
}
```

#### 创建路由表

```bash
ctcli vpc CreateRouteTable \
  --VpcId vpc-xxxxxxxx01 \
  --RouteTableName rt-web
```

**输出示例:**
```json
{
  "RouteTableId": "rtb-xxxxxxxx01",
  "RouteTableName": "rt-web",
  "VpcId": "vpc-xxxxxxxx01",
  "RequestId": "a9b0c1d2-e3f4-5678-abcd-901234567890",
  "Status": "Available"
}
```

### 负载均衡

#### 查询负载均衡实例列表

```bash
ctcli slb DescribeLoadBalancers --RegionId cn-east-1
```

**输出示例:**
```json
{
  "LoadBalancers": [
    {
      "LoadBalancerId": "lb-xxxxxxxx01",
      "LoadBalancerName": "web-lb",
      "LoadBalancerSpec": "slb.s2.medium",
      "AddressType": "public",
      "Status": "active",
      "InternetChargeType": "paybybandwidth",
      "Bandwidth": 100,
      "CreatedTime": "2026-02-10T11:00:00Z"
    }
  ],
  "TotalCount": 1
}
```

#### 创建负载均衡实例

```bash
ctcli slb CreateLoadBalancer \
  --LoadBalancerName api-lb \
  --RegionId cn-east-1 \
  --ZoneId.1 cn-east-1a \
  --ZoneId.2 cn-east-1b \
  --LoadBalancerSpec slb.s2.large \
  --AddressType public \
  --InternetChargeType paybytraffic
```

**输出示例:**
```json
{
  "LoadBalancerId": "lb-xxxxxxxx02",
  "RequestId": "b0c1d2e3-f4a5-6789-bcde-f01234567890",
  "OrderId": "ORDER-202603150006",
  "Status": "Creating"
}
```

#### 注册后端服务器

```bash
ctcli slb RegisterTargets \
  --LoadBalancerId lb-xxxxxxxx01 \
  --TargetServer.1.InstanceId i-xxxxxxxxxxx01 \
  --TargetServer.1.Weight 100 \
  --TargetServer.2.InstanceId i-xxxxxxxxxxx02 \
  --TargetServer.2.Weight 100 \
  --BackendPort 80
```

**输出示例:**
```json
{
  "RequestId": "c1d2e3f4-a5b6-7890-cdef-123456789012",
  "Targets": [
    {
      "InstanceId": "i-xxxxxxxxxxx01",
      "Weight": 100,
      "Status": "Adding"
    },
    {
      "InstanceId": "i-xxxxxxxxxxx02",
      "Weight": 100,
      "Status": "Adding"
    }
  ]
}
```

### 弹性IP

#### 查询弹性IP列表

```bash
ctcli eip DescribeEips --RegionId cn-east-1
```

**输出示例:**
```json
{
  "EipAddresses": [
    {
      "AllocationId": "eip-xxxxxxxx01",
      "IpAddress": "180.x.x.x",
      "Bandwidth": 100,
      "InternetChargeType": "paybybandwidth",
      "Status": "InUse",
      "InstanceId": "lb-xxxxxxxx01",
      "InstanceType": "SlbInstance",
      "CreatedTime": "2026-02-10T11:30:00Z"
    },
    {
      "AllocationId": "eip-xxxxxxxx02",
      "IpAddress": "180.x.x.x",
      "Bandwidth": 50,
      "InternetChargeType": "paybytraffic",
      "Status": "Available",
      "InstanceId": null,
      "InstanceType": null,
      "CreatedTime": "2026-03-01T09:00:00Z"
    }
  ],
  "TotalCount": 2
}
```

#### 申请弹性IP

```bash
ctcli eip AllocateEipAddress \
  --RegionId cn-east-1 \
  --Bandwidth 100 \
  --InternetChargeType paybybandwidth \
  --Name web-eip
```

**输出示例:**
```json
{
  "AllocationId": "eip-xxxxxxxx03",
  "IpAddress": "180.x.x.x",
  "RequestId": "d2e3f4a5-b6c7-8901-defa-234567890123",
  "OrderId": "ORDER-202603150007",
  "Status": "Pending"
}
```

#### 绑定弹性IP

```bash
ctcli eip AssociateEipAddress \
  --AllocationId eip-xxxxxxxx02 \
  --InstanceId i-xxxxxxxxxxx01 \
  --InstanceType EcsInstance
```

**输出示例:**
```json
{
  "RequestId": "e3f4a5b6-c7d8-9012-efab-345678901234",
  "AllocationId": "eip-xxxxxxxx02",
  "InstanceId": "i-xxxxxxxxxxx01",
  "Status": "Binding"
}
```

---

## 6. 监控

### 云监控

#### 查询监控指标列表

```bash
ctcli cms ListMetrics --RegionId cn-east-1 --Namespace acs_ecs_dashboard
```

**输出示例:**
```json
{
  "Metrics": [
    {
      "MetricName": "cpu_utilization",
      "Namespace": "acs_ecs_dashboard",
      "Dimensions": [
        {
          "Name": "instanceId",
          "Value": "i-xxxxxxxxxxx01"
        }
      ],
      "Statistics": ["Average", "Minimum", "Maximum"],
      "Period": 60
    },
    {
      "MetricName": "memory_usage",
      "Namespace": "acs_ecs_dashboard",
      "Dimensions": [
        {
          "Name": "instanceId",
          "Value": "i-xxxxxxxxxxx01"
        }
      ],
      "Statistics": ["Average", "Minimum", "Maximum"],
      "Period": 60
    },
    {
      "MetricName": "disk_read_bytes",
      "Namespace": "acs_ecs_dashboard",
      "Dimensions": [
        {
          "Name": "instanceId",
          "Value": "i-xxxxxxxxxxx01"
        }
      ],
      "Statistics": ["Average", "Minimum", "Maximum"],
      "Period": 60
    }
  ],
  "TotalCount": 3
}
```

#### 查询监控数据

```bash
ctcli cms GetMetricData \
  --MetricName cpu_utilization \
  --Namespace acs_ecs_dashboard \
  --Dimension.1.Name instanceId \
  --Dimension.1.Value i-xxxxxxxxxxx01 \
  --StartTime 1749859200 \
  --EndTime 1749862800 \
  --Period 60
```

**输出示例:**
```json
{
  "Datapoints": [
    {
      "Timestamp": 1749859260,
      "Average": 23.45,
      "Minimum": 15.20,
      "Maximum": 45.80
    },
    {
      "Timestamp": 1749859320,
      "Average": 28.12,
      "Minimum": 18.50,
      "Maximum": 52.30
    },
    {
      "Timestamp": 1749859380,
      "Average": 25.67,
      "Minimum": 12.10,
      "Maximum": 48.90
    }
  ],
  "Period": 60,
  "MetricName": "cpu_utilization",
  "Namespace": "acs_ecs_dashboard"
}
```

#### 创建报警规则

```bash
ctcli cms CreateAlarm \
  --AlarmName cpu-high-alarm \
  --MetricName cpu_utilization \
  --Namespace acs_ecs_dashboard \
  --Dimension.1.Name instanceId \
  --Dimension.1.Value i-xxxxxxxxxxx01 \
  --Condition "Average > 80" \
  --Period 300 \
  --EvaluationCount 3 \
  --NotifyType 1
```

**输出示例:**
```json
{
  "RequestId": "f4a5b6c7-d8e9-0123-fabc-456789012345",
  "AlarmId": "alarm-xxxxxxxx01",
  "AlarmName": "cpu-high-alarm",
  "Status": "Enabled"
}
```

---

## 7. 资源管理

### IAM

#### 查询用户列表

```bash
ctcli iam ListUsers --RegionId cn-east-1
```

**输出示例:**
```json
{
  "Users": [
    {
      "UserId": "user-xxxxxxxx01",
      "UserName": "admin",
      "DisplayName": "System Administrator",
      "Email": "admin@example.com",
      "Mobile": "+86.138xxxxxxx",
      "Status": "Active",
      "CreatedTime": "2026-01-01T00:00:00Z",
      "LastLoginTime": "2026-03-15T08:30:00Z"
    },
    {
      "UserId": "user-xxxxxxxx02",
      "UserName": "developer",
      "DisplayName": "Development Team",
      "Email": "dev@example.com",
      "Mobile": "+86.139xxxxxxx",
      "Status": "Active",
      "CreatedTime": "2026-01-15T10:00:00Z",
      "LastLoginTime": "2026-03-14T17:45:00Z"
    }
  ],
  "TotalCount": 2
}
```

#### 创建用户

```bash
ctcli iam CreateUser \
  --UserName app-operator \
  --DisplayName "Application Operator" \
  --Email operator@example.com \
  --Mobile +86.136xxxxxxx \
  --Description "Application deployment and operation user"
```

**输出示例:**
```json
{
  "UserId": "user-xxxxxxxx03",
  "UserName": "app-operator",
  "DisplayName": "Application Operator",
  "Email": "operator@example.com",
  "RequestId": "a5b6c7d8-e9f0-1234-bcde-567890123456",
  "Status": "Active"
}
```

#### 创建访问密钥

```bash
ctcli iam CreateAccessKey --UserName app-operator
```

**输出示例:**
```json
{
  "AccessKey": {
    "AccessKeyId": "AKTP1a2b3c4d5e6f7g8h9i0j",
    "Status": "Active",
    "CreateTime": "2026-03-15T12:00:00Z"
  },
  "SecretAccessKey": "SKTPxxxxxxxxxxxxxxxxxxxxxx",
  "RequestId": "b6c7d8e9-f0a1-2345-cdef-678901234567"
}
```

---

## 8. 附录：产品CLI名称映射表

| 产品类别 | 产品名称 | CLI命令空间 | 官方文档 |
|----------|----------|-------------|----------|
| **计算服务** | 云服务器 ECS | `ctcli ecs` | https://www.ctyun.cn/document/100678 |
| | 容器服务 CCS | `ctcli cs` | https://www.ctyun.cn/document/101234 |
| | 弹性伸缩 ESS | `ctcli ess` | https://www.ctyun.cn/document/100789 |
| | 镜像服务 | `ctcli ecs DescribeImages` | https://www.ctyun.cn/document/100679 |
| **存储服务** | 对象存储 OBS | `ctcli obs` | https://www.ctyun.cn/document/100012 |
| | 云硬盘 | `ctcli ecs CreateDisk/AttachDisk` | https://www.ctyun.cn/document/100023 |
| | 文件存储 | `ctcli nas` | https://www.ctyun.cn/document/100034 |
| **数据库服务** | MySQL | `ctcli rds` | https://www.ctyun.cn/document/100045 |
| | PostgreSQL | `ctcli rds` | https://www.ctyun.cn/document/100045 |
| | Redis | `ctcli redis` | https://www.ctyun.cn/document/100056 |
| | MongoDB | `ctcli mongodb` | https://www.ctyun.cn/document/100067 |
| | 分布式数据库 | `ctcli dds` | https://www.ctyun.cn/document/100078 |
| **网络服务** | 私有网络 VPC | `ctcli vpc` | https://www.ctyun.cn/document/100089 |
| | 负载均衡 SLB | `ctcli slb` | https://www.ctyun.cn/document/100090 |
| | 弹性IP EIP | `ctcli eip` | https://www.ctyun.cn/document/100091 |
| | NAT网关 | `ctcli nat` | https://www.ctyun.cn/document/100092 |
| | 专线接入 | `ctcli phy` | https://www.ctyun.cn/document/100093 |
| **监控服务** | 云监控 CMS | `ctcli cms` | https://www.ctyun.cn/document/100103 |
| **资源管理** | 访问控制 IAM | `ctcli iam` | https://www.ctyun.cn/document/100111 |
| | 标签服务 | `ctcli tag` | https://www.ctyun.cn/document/100112 |
| **安全服务** | 安全组 | `ctcli ecs DescribeSecurityGroups` | https://www.ctyun.cn/document/100120 |
| | DDoS防护 | `ctcli ddos` | https://www.ctyun.cn/document/100121 |
| **应用服务** | API网关 | `ctcli api` | https://www.ctyun.cn/document/100130 |
| | 消息队列 | `ctcli mq` | https://www.ctyun.cn/document/100131 |

---

## 快速参考

### 常用命令速查

```bash
# 查看帮助
ctcli help
ctcli ecs help
ctcli ecs DescribeInstances --help

# 查看账号信息
ctcli account get

# 查看资源概览
ctcli summary

# 切换Region
ctcli configure set --region cn-south-1

# 查看当前配置
ctcli configure list
```

### 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| `InvalidAccessKeyId` | 访问密钥无效 | 检查AccessKey是否正确配置 |
| `InvalidSecretKey` | 密钥Secret无效 | 重新生成访问密钥 |
| `Unauthorized` | 未授权 | 检查IAM权限策略 |
| `ResourceNotFound` | 资源不存在 | 检查资源ID是否正确 |
| `InvalidParameter` | 参数无效 | 检查命令参数格式 |
| `QuotaExceeded` | 配额超限 | 提交工单申请提升配额 |
| `RequestTimeout` | 请求超时 | 重试操作或检查网络连接 |

---

**文档版本**: v1.0
**最后更新**: 2026-03-15
**CLI版本要求**: CT-CLI v3.0.0+