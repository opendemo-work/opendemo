# 腾讯云CLI命令速查表

> 腾讯云命令行工具完整参考手册，覆盖计算、存储、数据库、网络、安全等核心产品线

---

## 目录索引

- [安装与配置](#安装与配置)
- [计算服务](#计算服务)
  - [CVM云服务器](#cvm云服务器)
  - [容器服务TKE](#容器服务tke)
  - [无服务器云函数SCF](#无服务器云函数scf)
- [存储服务](#存储服务)
  - [COS对象存储](#cos对象存储)
  - [CBS云硬盘](#cbs云硬盘)
  - [CFS文件存储](#cfs文件存储)
- [数据库服务](#数据库服务)
  - [MySQL/PostgreSQL](#mysqlpostgresql)
  - [Redis数据库](#redis数据库)
  - [MongoDB数据库](#mongodb数据库)
- [网络服务](#网络服务)
  - [VPC私有网络](#vpc私有网络)
  - [CLB负载均衡](#clb负载均衡)
  - [专线连接](#专线连接)
  - [VPN网关](#vpn网关)
- [内容分发CDN](#内容分发cdn)
- [安全服务](#安全服务)
  - [密钥管理KMS](#密钥管理kms)
  - [云防火墙CFW](#云防火墙cfw)
  - [WAFWeb应用防火墙](#wafweb应用防火墙)
- [中间件服务](#中间件服务)
  - [CMQ消息队列](#cmq消息队列)
  - [CKafka消息队列](#ckafka消息队列)
  - [TDMQ分布式消息](#tdmq分布式消息)
- [监控运维](#监控运维)
  - [云监控CM](#云监控cm)
  - [运维编排](#运维编排)
- [访问控制CAM](#访问控制cam)
- [附录：产品CLI名称映射表](#附录产品cli名称映射表)

---

## 安装与配置

### 安装

```bash
# Linux/macOS/Windows 下载安装
# 下载地址: https://github.com/TencentCloud/tencentcloud-cli-intl/releases

# Linux/macOS 安装
curl -sSL https://raw.githubusercontent.com/TencentCloud/tencentcloud-cli-intl-bin/master/install.sh | sh

# macOS Homebrew 安装
brew install tccli

# Windows 安装 (PowerShell)
iwr https://raw.githubusercontent.com/TencentCloud/tencentcloud-cli-intl-bin/master/install.ps1 -OutFile install.ps1; .\install.ps1

# 验证安装
tccli cli version
# 输出: cvm v3.0.136 2024-12-01
```

### 配置凭证

```bash
# 交互式配置（推荐）
tccli configure
# 提示输入 SecretId、SecretKey、Region、Output format

# 非交互式配置
tccli configure set secretId AKIDxxxxxxxxxxxxxxxxxxxxx
tccli configure set secretKey your-secret-key-here
tccli configure set region ap-guangzhou
tccli configure set output json

# 环境变量配置
export TENCENTCLOUD_SECRET_ID=AKIDxxxxxxxxxxxxxxxxxxxxx
export TENCENTCLOUD_SECRET_KEY=your-secret-key-here
export TENCENTCLOUD_REGION=ap-guangzhou

# 多账户Profile配置
tccli configure --profile admin
tccli configure --profile dev --secretId AKIDyyyyyyyyyyyyyyyyyyyy

# 使用指定Profile
tccli cvm DescribeInstances --profile dev

# 查看配置列表
tccli configure list
# 输出:
# [default]
# secretId = AKIDxxxxxxxxxxxxxxxxxxxxx
# secretKey = ****************
# region = ap-guangzhou
# output = json

# [dev]
# secretId = AKIDyyyyyyyyyyyyyyyyyyyy
# secretKey = ****************
# region = ap-shanghai
# output = json
```

### 常用全局参数

```bash
--region          # 地域ID，如 ap-guangzhou, ap-shanghai, ap-beijing
--profile        # 配置文件名，如 --profile default
--secret-id      # 访问密钥ID（临时覆盖配置）
--secret-key     # 访问密钥Key（临时覆盖配置）
--output         # 输出格式，支持 json/table/text，默认为 json
--version        # API版本号，格式如 2022-03-03
--endpoint       # API endpoint，覆盖默认端点
--debug          # 开启调试模式，显示完整请求响应
--page-number    # 分页查询页码
--page-size      # 分页查询每页数量
```

---

## 计算服务

### CVM云服务器

```bash
# 查询可用区资源
tccli cvm DescribeZoneConfig --region ap-guangzhou

# 查询实例列表
tccli cvm DescribeInstances --region ap-guangzhou --output table
# 输出:
# ------------------------------------------------------------
# |                     DescribeInstances                      |
# +-----------------+-----------------+--------+--------------+
# |    InstanceId   |   InstanceName  | Status |  PublicIp   |
# +-----------------+-----------------+--------+--------------+
# | ins-xxxxxxxxx   | web-server-01   | RUNNING| 43.123.45.67 |
# | ins-yyyyyyyyy   | db-server-01    | RUNNING| 43.123.45.68 |
# +-----------------+-----------------+--------+--------------+

# 查询单个实例详情
tccli cvm DescribeInstances --region ap-guangzhou --InstanceIds '["ins-xxxxxxxxx"]'

# 创建按量付费实例
tccli cvm RunInstances --region ap-guangzhou \
  --InstanceType CVM.S2.small \
  --ImageId img-xxxxxxxx \
  --SubnetId subnet-xxxxxxxx \
  --SecurityGroupIds '["sg-xxxxxxxx"]' \
  --InstanceChargeType POSTPAID_BY_HOUR \
  --InstanceName my-web-server

# 创建包年包月实例
tccli cvm RunInstances --region ap-guangzhou \
  --InstanceType CVM.S2.small \
  --ImageId img-xxxxxxxx \
  --SubnetId subnet-xxxxxxxx \
  --SecurityGroupIds '["sg-xxxxxxxx"]' \
  --InstanceChargeType PREPAID \
  --Period 12 \
  --InstanceChargePrepaid '{"Period":12,"RenewFlag":"NOTIFY_AND_AUTO_RENEW"}'

# 启动实例
tccli cvm StartInstances --region ap-guangzhou --InstanceIds '["ins-xxxxxxxxx"]'

# 停止实例
tccli cvm StopInstances --region ap-guangzhou --InstanceIds '["ins-xxxxxxxxx"]'
# 输出:
# {
#   "InstanceIdSet": ["ins-xxxxxxxxx"],
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 重启实例
tccli cvm RebootInstances --region ap-guangzhou --InstanceIds '["ins-xxxxxxxxx"]'

# 删除/退还实例
tccli cvm TerminateInstances --region ap-guangzhou --InstanceIds '["ins-xxxxxxxxx"]'

# 重装系统
tccli cvm ResetInstance --region ap-guangzhou \
  --InstanceId ins-xxxxxxxxx \
  --ImageId img-yyyyyyyy

# 修改实例属性
tccli cvm ModifyInstanceAttribute --region ap-guangzhou \
  --InstanceId ins-xxxxxxxxx \
  --InstanceName new-server-name

# 查询镜像列表
tccli cvm DescribeImages --region ap-guangzhou \
  --ImageIds '["img-xxxxxxxx"]'
# 输出:
# {
#   "ImageSet": [
#     {
#       "ImageId": "img-xxxxxxxx",
#       "ImageName": "Ubuntu 22.04 LTS 64bit",
#       "ImageState": "NORMAL",
#       "OSName": "Ubuntu 22.04 LTS"
#     }
#   ],
#   "TotalCount": 1
# }

# 查询实例规格
tccli cvm DescribeInstanceTypeConfigs --region ap-guangzhou

# 创建云盘
tccli cbs CreateDisks --region ap-guangzhou \
  --DiskType CLOUD_BSSD \
  --DiskSize 100 \
  --Zone ap-guangzhou-3

# 查询云盘列表
tccli cbs DescribeDisks --region ap-guangzhou \
  --DiskIds '["disk-xxxxxxxx"]'

# 挂载云盘
tccli cbs AttachDisks --region ap-guangzhou \
  --DiskIds '["disk-xxxxxxxx"]' \
  --InstanceId ins-xxxxxxxxx

# 解绑云盘
tccli cbs DetachDisks --region ap-guangzhou \
  --DiskIds '["disk-xxxxxxxx"]' \
  --InstanceId ins-xxxxxxxxx

# 云盘续费
tccli cbs RenewDisks --region ap-guangzhou \
  --DiskIds '["disk-xxxxxxxx"]' \
  --RenewChargePrepaid '{"RenewPercent":100}'
```

---

### 容器服务TKE

```bash
# 查询集群列表
tccli tke DescribeClusters --region ap-guangzhou
# 输出:
# {
#   "ClusterSet": [
#     {
#       "ClusterId": "cls-xxxxxxxx",
#       "ClusterName": "my-k8s-cluster",
#       "ClusterVersion": "1.28.4",
#       "ClusterStatus": "Running",
#       "ClusterType": "Managed"
#     }
#   ],
#   "TotalCount": 1
# }

# 查询集群信息
tccli tke DescribeCluster --region ap-guangzhou --ClusterId cls-xxxxxxxx

# 创建集群
tccli tke CreateCluster --region ap-guangzhou \
  --ClusterName my-tke-cluster \
  --ClusterType managed \
  --KubernetesVersion 1.28.4 \
  --VpcId vpc-xxxxxxxx \
  --SubnetIds '["subnet-xxxxxxxx"]' \
  --ManagedClusterExtraArgs '{"KubeProxy":{"kube-proxy-ipvs":{"mode":"stub"}}}' \
  --NodePoolExtraArgs '{"mounter":""}'

# 创建节点池
tccli tke CreateNodePool --region ap-guangzhou \
  --ClusterId cls-xxxxxxxx \
  --AutoScalingGroupDesiredSize 2 \
  --NodePoolName my-nodepool

# 扩容节点池
tccli tke ScaleCluster --region ap-guangzhou \
  --ClusterId cls-xxxxxxxx \
  --NodePoolId np-xxxxxxxx \
  --DesiredSize 5

# 删除集群
tccli tke DeleteCluster --region ap-guangzhou --ClusterId cls-xxxxxxxx

# 获取集群凭证
tccli tke DescribeClusterCredentials --region ap-guangzhou --ClusterId cls-xxxxxxxx
# 输出:
# {
#   "Credentials": {
#     "Kubeconfig": "YXBwbGU6Ly9jbHVzdGVyLWlkOjEuMjguNC4uLi4="
#   }
# }

# 查询节点列表
tccli tke DescribeClusterInstances --region ap-guangzhou \
  --ClusterId cls-xxxxxxxx

# 添加已有节点
tccli tke AddExistedInstances --region ap-guangzhou \
  --ClusterId cls-xxxxxxxx \
  --InstanceIds '["ins-xxxxxxxxx"]' \
  --NodePoolId np-xxxxxxxx

# 查询节点池
tccli tke DescribeNodePools --region ap-guangzhou --ClusterId cls-xxxxxxxx

# 修改节点池
tccli tke ModifyNodePool --region ap-guangzhou \
  --ClusterId cls-xxxxxxxx \
  --NodePoolId np-xxxxxxxx \
  --DesiredSize 3
```

---

### 无服务器云函数SCF

```bash
# 查询函数列表
tccli scf ListFunctions --region ap-guangzhou --namespace default
# 输出:
# {
#   "Functions": [
#     {
#       "FunctionId": "f-xxxxxxxxx",
#       "FunctionName": "my-handler",
#       "Runtime": "Python3.11",
#       "ModTime": "2024-06-15 10:30:00",
#       "Status": "Active"
#     }
#   ],
#   "TotalCount": 1
# }

# 创建函数
tccli scf CreateFunction --region ap-guangzhou \
  --FunctionName my-python-function \
  --Runtime Python3.11 \
  --Code '{"ZipFile":"base64-encoded-code.zip"}' \
  --Handler index.handler \
  --Namespace default \
  --MemorySize 128 \
  --Timeout 30

# 获取函数配置
tccli scf GetFunction --region ap-guangzhou \
  --FunctionName my-python-function \
  --Namespace default
# 输出:
# {
#   "FunctionId": "f-xxxxxxxxx",
#   "FunctionName": "my-python-function",
#   "Runtime": "Python3.11",
#   "MemorySize": 128,
#   "Timeout": 30,
#   "Environment": {"Variables": {}},
#   "Status": "Active"
# }

# 调用函数
tccli scf InvokeFunction --region ap-guangzhou \
  --FunctionName my-python-function \
  --Namespace default \
  --InvocationType RequestResponse \
  --Payload '{"key":"value"}'
# 输出:
# {
#   "Result": {
#     "Duration": 12.34,
#     "BillDuration": 13,
#     "FunctionRequestId": "req-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
#     "LogResult": "AAABBBCCCDDDEEE...",
#     "RetMsg": "\"Hello from serverless\"",
#     "ErrMsg": "",
#     "InvokeResult": 0
#   }
# }

# 同步调用函数
tccli scf InvokeFunction --region ap-guangzhou \
  --FunctionName my-python-function \
  --InvocationType Synchronous

# 更新函数代码
tccli scf UpdateFunctionCode --region ap-guangzhou \
  --FunctionName my-python-function \
  --Code '{"ZipFile":"base64-encoded-new-code.zip"}'

# 更新函数配置
tccli scf UpdateFunctionConfiguration --region ap-guangzhou \
  --FunctionName my-python-function \
  --MemorySize 256 \
  --Timeout 60

# 删除函数
tccli scf DeleteFunction --region ap-guangzhou \
  --FunctionName my-python-function \
  --Namespace default

# 查询触发器
tccli scf ListTriggers --region ap-guangzhou \
  --FunctionName my-python-function \
  --Namespace default

# 创建触发器
tccli scf CreateTrigger --region ap-guangzhou \
  --FunctionName my-python-function \
  --TriggerName my-trigger \
  --TriggerType cos \
  --TriggerDesc '{"bucket":"my-bucket-123456789","filter":{"prefix":"","sufix":".jpg"}}'
```

---

## 存储服务

### COS对象存储

```bash
# COS使用专用工具coscli，需要先安装
# 安装: brew install tencentcloud-cli-tccli

# 配置COS CLI
coscli configure set -a AKIDxxxxxxxx -k your-secret-key -b my-bucket-123456789 -r ap-guangzhou

# 查询Bucket列表
coscli ls
# 输出:
#   BucketNumber: 2
#   BucketList:
#     - my-bucket-123456789
#     - another-bucket-987654321

# 创建Bucket
coscli mb cos://new-bucket-123456789

# 上传文件
coscli cp ./file.txt cos://my-bucket-123456789/prefix/
# 输出:
#   [2024-06-15 10:30:00] [100%] [40.00B/40.00B] - 1/1 files uploaded successfully

# 下载文件
coscli cp cos://my-bucket-123456789/file.txt ./download.txt

# 列出Bucket内文件
coscli ls cos://my-bucket-123456789/
# 输出:
#   Object Number: 3
#   ObjectList:
#     - file.txt
#     - images/logo.png
#     - documents/readme.md

# 同步目录（增量）
coscli sync /local/dir/ cos://my-bucket-123456789/prefix/

# 删除文件
coscli rm cos://my-bucket-123456789/file.txt

# 生成签名URL（临时访问）
coscli sign-url cos://my-bucket-123456789/file.txt --expires 3600
# 输出:
#   https://my-bucket-123456789.cos.ap-guangzhou.myqcloud.com/file.txt?sign=xxxxxx

# 设置静态网站托管
coscli website set cos://my-bucket-123456789 --index index.html --error error.html

# 配置CORS跨域规则
coscli cors set cos://my-bucket-123456789 --rules '[{"allowedOrigin":"*","allowedMethod":["GET"],"allowedHeader":"*","maxAgeSeconds":3600}]'

# 配置生命周期规则
coscli lifecycle set cos://my-bucket-123456789 \
  --rule-id aging-rule \
  --prefix "logs/" \
  --expire-days 30
# 输出:
#   Successfully set lifecycle rule: aging-rule

# 查看存储类型
coscli stat cos://my-bucket-123456789/file.txt
# 输出:
#   Key: file.txt
#   Size: 40 B
#   StorageClass: STANDARD
#   LastModified: 2024-06-15T10:30:00Z

# 修改存储类型
coscli object restore cos://my-bucket-123456789/archive.txt --days 3
```

---

### CBS云硬盘

```bash
# 查询云盘列表
tccli cbs DescribeDisks --region ap-guangzhou \
  --Filters '[{"Name":"zone","Values":["ap-guangzhou-3"]}]'
# 输出:
# {
#   "DiskSet": [
#     {
#       "DiskId": "disk-xxxxxxxx",
#       "DiskName": "data-disk",
#       "DiskType": "CLOUD_BSSD",
#       "DiskSize": 100,
#       "DiskState": "AVAILABLE",
#       "InstanceId": "",
#       "CreateTime": "2024-06-15 10:30:00"
#     }
#   ],
#   "TotalCount": 1
# }

# 创建云盘
tccli cbs CreateDisks --region ap-guangzhou \
  --DiskType CLOUD_BSSD \
  --DiskSize 200 \
  --Zone ap-guangzhou-3 \
  --DiskName my-data-disk
# 输出:
# {
#   "DiskIdSet": ["disk-yyyyyyyy"],
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 创建加密云盘
tccli cbs CreateDisks --region ap-guangzhou \
  --DiskType CLOUD_BSSD \
  --DiskSize 100 \
  --Zone ap-guangzhou-3 \
  --Encrypted true

# 查询云盘操作日志
tccli cbs DescribeDiskOperationLogs --region ap-guangzhou \
  --DiskIds '["disk-xxxxxxxx"]'

# 挂载云盘
tccli cbs AttachDisks --region ap-guangzhou \
  --DiskIds '["disk-xxxxxxxx"]' \
  --InstanceId ins-xxxxxxxxx

# 解绑云盘
tccli cbs DetachDisks --region ap-guangzhou \
  --DiskIds '["disk-xxxxxxxx"]' \
  --InstanceId ins-xxxxxxxxx

# 删除云盘
tccli cbs DeleteDisks --region ap-guangzhou \
  --DiskIds '["disk-xxxxxxxx"]'

# 云盘续费
tccli cbs RenewDisks --region ap-guangzhou \
  --DiskIds '["disk-xxxxxxxx"]' \
  --RenewChargePrepaid '{"RenewPercent":100}'

# 查询快照列表
tccli cbs DescribeSnapshots --region ap-guangzhou \
  --DiskId disk-xxxxxxxx
# 输出:
# {
#   "SnapshotSet": [
#     {
#       "SnapshotId": "snap-xxxxxxxx",
#       "SnapshotName": "snap-20240615",
#       "DiskId": "disk-xxxxxxxx",
#       "SnapshotState": "NORMAL",
#       "Percent": 100
#     }
#   ]
# }

# 创建快照
tccli cbs CreateSnapshot --region ap-guangzhou --DiskId disk-xxxxxxxx

# 回滚云盘
tccli cbs ApplyDisk --region ap-guangzhou --DiskId disk-xxxxxxxx --SnapshotId snap-xxxxxxxx
```

---

### CFS文件存储

```bash
# 查询文件系统列表
tccli cfs DescribeFileSystems --region ap-guangzhou
# 输出:
# {
#   "FileSystemSet": [
#     {
#       "FileSystemId": "cfs-xxxxxxxx",
#       "FsName": "my-cfs",
#       "Region": "ap-guangzhou",
#       "Zone": "ap-guangzhou-3",
#       "Protocol": "NFS",
#       "StorageType": "SD",
#       "MountTargetSet": [
#         {
#           "MountTargetId": "mt-xxxxxxxx",
#           "VpcId": "vpc-xxxxxxxx",
#           "SubnetId": "subnet-xxxxxxxx",
#           "MountTargetDomain": "cfs-xxxxxxxx.ap-guangzhou.gz6.fs.local"
#         }
#       ]
#     }
#   ]
# }

# 创建文件系统
tccli cfs CreateFileSystem --region ap-guangzhou \
  --FsName my-cfs \
  --Zone ap-guangzhou-3 \
  --Protocol NFS \
  --StorageType SD

# 查询挂载点
tccli cfs DescribeMountTargets --region ap-guangzhou --FileSystemId cfs-xxxxxxxx

# 创建挂载点
tccli cfs CreateMountTarget --region ap-guangzhou \
  --FileSystemId cfs-xxxxxxxx \
  --VpcId vpc-xxxxxxxx \
  --SubnetId subnet-xxxxxxxx

# 删除挂载点
tccli cfs DeleteMountTarget --region ap-guangzhou \
  --FileSystemId cfs-xxxxxxxx \
  --MountTargetId mt-xxxxxxxx

# 查询权限组
tccli cfs DescribeUserGroups --region ap-guangzhou

# 创建权限组
tccli cfs CreateUserGroup --region ap-guangzhou \
  --Name my-permission-group

# 添加权限组规则
tccli cfs AddUserGroupRules --region ap-guangzhou \
  --UserGroupId ug-xxxxxxxx \
  --Rules '[{"AuthClient": "10.0.0.0/8", "Priority": 1, "RWPermission": "rw", "UserPermission": "all_squash"}]'

# 查询文件系统配额
tccli cfs DescribeCfsFileSystemClients --region ap-guangzhou --FileSystemId cfs-xxxxxxxx
```

---

## 数据库服务

### MySQL/PostgreSQL

```bash
# 查询CDB实例列表
tccli cdb DescribeDBInstances --region ap-guangzhou
# 输出:
# {
#   "Items": [
#     {
#       "UniInstanceId": "cdb-xxxxxxxx",
#       "InstanceName": "my-mysql",
#       "InstanceType": 2,
#       "EngineVersion": "8.0",
#       "Status": 1,
#       "Vip": "10.0.1.10",
#       "Vport": 3306
#     }
#   ],
#   "TotalCount": 1
# }

# 创建MySQL实例
tccli cdb CreateDBInstance --region ap-guangzhou \
  --InstanceName my-mysql \
  --EngineType mysql \
  --EngineVersion 8.0 \
  --InstanceType S2.small \
  --Storage 50 \
  --Zone "ap-guangzhou-3" \
  --SubnetId subnet-xxxxxxxx \
  --SecurityGroupIds '["sg-xxxxxxxx"]'

# 创建只读实例
tccli cdb CreateDBInstance --region ap-guangzhou \
  --InstanceName my-mysql-ro \
  --EngineType mysql \
  --EngineVersion 8.0 \
  --InstanceType S2.small \
  --Storage 50 \
  --Zone "ap-guangzhou-3" \
  --MasterInstanceId cdb-xxxxxxxx \
  --VpcId vpc-xxxxxxxx \
  --SubnetId subnet-xxxxxxxx

# 查询数据库列表
tccli cdb DescribeDatabases --region ap-guangzhou --InstanceId cdb-xxxxxxxx

# 创建数据库
tccli cdb CreateDatabase --region ap-guangzhou \
  --InstanceId cdb-xxxxxxxx \
  --DBName myappdb \
  --Charset utf8mb4

# 查询账号列表
tccli cdb DescribeAccounts --region ap-guangzhou --InstanceId cdb-xxxxxxxx

# 创建账号
tccli cdb CreateAccount --region ap-guangzhou \
  --InstanceId cdb-xxxxxxxx \
  --AccountName appuser \
  --AccountPassword MyP@ssw0rd! \
  --Host '%'

# 授权账号数据库权限
tccli cdb GrantAccountPrivileges --region ap-guangzhou \
  --InstanceId cdb-xxxxxxxx \
  --AccountName appuser \
  --Host '%' \
  --DBPrivileges '[{"DBName":"myappdb","Privileges":["SELECT","INSERT"]}]'

# 设置白名单
tccli cdb ModifyDBInstanceSecurityGroup --region ap-guangzhou \
  --InstanceId cdb-xxxxxxxx \
  --SecurityGroupIds '["sg-xxxxxxxx"]'

# 查询备份列表
tccli cdb DescribeBackups --region ap-guangzhou --InstanceId cdb-xxxxxxxx
# 输出:
# {
#   "Items": [
#     {
#       "BackupId": 1234567890,
#       "BackupName": "backup-20240615",
#       "BackupTime": "2024-06-15 02:00:00",
#       "BackupType": " logical",
#       "BackupSize": 52428800,
#       "Status": "SUCCESS"
#     }
#   ]
# }

# 创建备份
tccli cdb CreateBackup --region ap-guangzhou \
  --InstanceId cdb-xxxxxxxx \
  --BackupMethod Logical \
  --BackupName "manual-backup-001"

# 恢复数据库
tccli cdb RestoreInstance --region ap-guangzhou \
  --InstanceId cdb-xxxxxxxx \
  --BackupId 1234567890

# 变配实例规格
tccli cdb ModifyDBInstanceSpec --region ap-guangzhou \
  --InstanceId cdb-xxxxxxxx \
  --InstanceType S2.large

# 设置备份策略
tccli cdb ModifyBackupPolicy --region ap-guangzhou \
  --InstanceId cdb-xxxxxxxx \
  --BinaryBackupEnabled 0 \
  --BackupPeriod '["Monday","Wednesday","Friday"]' \
  --BackupTime "02:00-04:00" \
  --SaveDays 7

# 开启SSL加密
tccli cdb ModifyDBInstanceSSL --region ap-guangzhou \
  --InstanceId cdb-xxxxxxxx \
  --SSLEnabled 1

# 开启TDE加密
tccli cdb ModifyDBInstanceTDE --region ap-guangzhou \
  --InstanceId cdb-xxxxxxxx \
  --TDEStatus enabled
```

---

### Redis数据库

```bash
# 查询Redis实例列表
tccli redis DescribeInstances --region ap-guangzhou --TypeId 1
# 输出:
# {
#   "InstanceSet": [
#     {
#       "InstanceId": "crs-xxxxxxxx",
#       "InstanceName": "my-redis",
#       "Status": 2,
#       "Type": 1,
#       "Engine": "Redis",
#       "EngineVersion": "6.2.7",
#       "Size": 1024,
#       "BillingMode": 1,
#       "Vip": "10.0.1.20",
#       "Port": 6379
#     }
#   ],
#   "TotalCount": 1
# }

# 创建Redis实例
tccli redis CreateInstance --region ap-guangzhou \
  --InstanceName my-redis \
  --TypeId 1 \
  --MemSize 1024 \
  --ZoneId ap-guangzhou-3 \
  --SubnetId subnet-xxxxxxxx \
  --SecurityGroupIds '["sg-xxxxxxxx"]'

# 创建集群版Redis
tccli redis CreateInstance --region ap-guangzhou \
  --InstanceName my-redis-cluster \
  --TypeId 1 \
  --MemSize 4096 \
  --ZoneId ap-guangzhou-3 \
  --VpcId vpc-xxxxxxxx \
  --SubnetId subnet-xxxxxxxx \
  --RedisReplicateNum 2 \
  --ShardNum 3

# 查询实例配置
tccli redis DescribeInstanceConfig --region ap-guangzhou --InstanceId crs-xxxxxxxx

# 修改实例配置
tccli redis ModifyInstanceParams --region ap-guangzhou \
  --InstanceId crs-xxxxxxxx \
  --InstanceParams '{"maxmemory-policy":"volatile-lru"}'

# 创建账号
tccli redis CreateAccount --region ap-guangzhou \
  --InstanceId crs-xxxxxxxx \
  --AccountName myuser \
  --AccountPassword MyP@ssw0rd! \
  --Privilege ReadOnly \
  --Host '%'

# 开启SSL加密
tccli redis ModifySSL --region ap-guangzhou \
  --InstanceId crs-xxxxxxxx \
  --SSLEnabled 1

# 备份实例
tccli redis CreateBackUp --region ap-guangzhou --InstanceId crs-xxxxxxxx
# 输出:
# {
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
#   "BackupId": "xxxxxx"
# }

# 变配
tccli redis RenewInstance --region ap-guangzhou \
  --InstanceId crs-xxxxxxxx \
  --Period 12

# 查询备份文件
tccli redis DescribeInstanceBackUp --region ap-guangzhou --InstanceId crs-xxxxxxxx

# 禁用命令
tccli redis DisableDelayNode --region ap-guangzhou --InstanceId crs-xxxxxxxx --Command FLUSHDB,FLUSHALL
```

---

### MongoDB数据库

```bash
# 查询MongoDB实例列表
tccli mongo DescribeInstances --region ap-guangzhou
# 输出:
# {
#   "InstanceSet": [
#     {
#       "InstanceId": "cmongo-xxxxxxxx",
#       "InstanceName": "my-mongo",
#       "Status": 1,
#       "EngineVersion": "5.0",
#       "Shard": 0,
#       "ReplicateSet": 1,
#       "Vip": "10.0.1.30",
#       "Vport": 27017
#     }
#   ]
# }

# 创建副本集实例
tccli mongo CreateDBInstance --region ap-guangzhou \
  --InstanceName my-mongo \
  --SpecCode mongo.d.mseries.medium \
  --Capacity 20 \
  --Zone ap-guangzhou-3 \
  --VpcId vpc-xxxxxxxx \
  --SubnetId subnet-xxxxxxxx

# 创建分片集群
tccli mongo CreateDBInstance --region ap-guangzhou \
  --InstanceName my-mongo-shard \
  --SpecCode mongo.d.mseries.medium \
  --Capacity 20 \
  --Zone ap-guangzhou-3 \
  --VpcId vpc-xxxxxxxx \
  --SubnetId subnet-xxxxxxxx \
  --ClusterType 1 \
  --MongosNodeCount 2 \
  --ReplicateSetNum 1

# 创建数据库账号
tccli mongo CreateAccount --region ap-guangzhou \
  --InstanceId cmongo-xxxxxxxx \
  --AccountName myuser \
  --AccountPassword MyP@ssw0rd! \
  --AuthFlag 1

# 设置密码
tccli mongo SetPassword --region ap-guangzhou \
  --InstanceId cmongo-xxxxxxxx \
  --AccountName myuser \
  --AccountPassword NewP@ssw0rd!

# 设置白名单
tccli mongo ModifyDBInstanceSecurityGroup --region ap-guangzhou \
  --InstanceId cmongo-xxxxxxxx \
  --SecurityGroupIds '["sg-xxxxxxxx"]'

# 设置备份策略
tccli mongo ModifyBackupPolicy --region ap-guangzhou \
  --InstanceId cmongo-xxxxxxxx \
  --BackupMethod Logical \
  --BackupTime "02:00" \
  --KeepDays 7

# 创建备份
tccli mongo CreateBackup --region ap-guangzhou \
  --InstanceId cmongo-xxxxxxxx \
  --BackupMethod Logical

# 变配
tccli redis.RenewInstance --region ap-guangzhou \
  --InstanceId cmongo-xxxxxxxx \
  --InstanceType mongo.d.mseries.large

# 查询慢日志
tccli mongo DescribeSlowLog --region ap-guangzhou \
  --InstanceId cmongo-xxxxxxxx

# 查询性能数据
tccli mongo.DescribePerformance --region ap-guangzhou \
  --InstanceId cmongo-xxxxxxxx
```

---

## 网络服务

### VPC私有网络

```bash
# 查询VPC列表
tccli vpc DescribeVpcs --region ap-guangzhou
# 输出:
# {
#   "VpcSet": [
#     {
#       "VpcId": "vpc-xxxxxxxx",
#       "VpcName": "my-vpc",
#       "CidrBlock": "10.0.0.0/16",
#       "IsDefault": false,
#       "CreateTime": "2024-06-15 10:30:00"
#     }
#   ],
#   "TotalCount": 1
# }

# 创建VPC
tccli vpc CreateVpc --region ap-guangzhou \
  --VpcName my-vpc \
  --CidrBlock 10.0.0.0/16
# 输出:
# {
#   "Vpc": {
#     "VpcId": "vpc-xxxxxxxx",
#     "VpcName": "my-vpc",
#     "CidrBlock": "10.0.0.0/16"
#   },
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 删除VPC
tccli vpc DeleteVpc --region ap-guangzhou --VpcId vpc-xxxxxxxx

# 查询交换机列表
tccli vpc DescribeVSwitches --region ap-guangzhou --VpcId vpc-xxxxxxxx
# 输出:
# {
#   "VSwitchSet": [
#     {
#       "VSwitchId": "subnet-xxxxxxxx",
#       "VSwitchName": "my-subnet",
#       "VpcId": "vpc-xxxxxxxx",
#       "CidrBlock": "10.0.1.0/24",
#       "Zone": "ap-guangzhou-3",
#       "AvailableIpAddressCount": 250
#     }
#   ]
# }

# 创建交换机
tccli vpc CreateVSwitch --region ap-guangzhou \
  --VpcId vpc-xxxxxxxx \
  --VSwitchName my-subnet \
  --CidrBlock 10.0.1.0/24 \
  --Zone ap-guangzhou-3

# 删除交换机
tccli vpc DeleteVSwitch --region ap-guangzhou --VSwitchId subnet-xxxxxxxx

# 查询路由表
tccli vpc DescribeRouteTables --region ap-guangzhou --VpcId vpc-xxxxxxxx
# 输出:
# {
#   "RouteTableSet": [
#     {
#       "RouteTableId": "rtb-xxxxxxxx",
#       "RouteTableName": "default",
#       "VpcId": "vpc-xxxxxxxx",
#       "RouteTableSet": [
#         {
#           "DestinationCidrBlock": "0.0.0.0/0",
#           "GatewayType": "NAT",
#           "GatewayId": "ngw-xxxxxxxx"
#         }
#       ]
#     }
#   ]
# }

# 创建自定义路由表
tccli vpc CreateRouteTable --region ap-guangzhou \
  --VpcId vpc-xxxxxxxx \
  --RouteTableName my-routetable

# 添加路由策略
tccli vpc AddRouteEntry --region ap-guangzhou \
  --RouteTableId rtb-xxxxxxxx \
  --RouteTableEntry '{"DestinationCidrBlock":"192.168.0.0/16","GatewayType":"NETWORK","GatewayId":"lgw-xxxxxxxx"}'

# 删除路由策略
tccli vpc DeleteRouteEntry --region ap-guangzhou \
  --RouteTableId rtb-xxxxxxxx \
  --RouteTableEntry '{"DestinationCidrBlock":"192.168.0.0/16"}'

# 创建NAT网关
tccli vpc CreateNatGateway --region ap-guangzhou \
  --VpcId vpc-xxxxxxxx \
  --NatGatewayName my-natgw \
  --InternetServiceProvider BGP \
  --MaxConcurrentConnection 1000000
# 输出:
# {
#   "NatGateway": {
#     "NatGatewayId": "ngw-xxxxxxxx",
#     "NatGatewayName": "my-natgw"
#   }
# }

# 查询EIP列表
tccli vpc DescribeAddresses --region ap-guangzhou --AddressIds '["eip-xxxxxxxx"]'

# 分配弹性公网IP
tccli vpc AllocateAddresses --region ap-guangzhou \
  --AddressType EIP \
  --InternetChargeType BANDWIDTH_POSTPAID \
  --InternetMaxBandwidth 100
# 输出:
# {
#   "AddressSet": ["eip-xxxxxxxx"],
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 绑定EIP到NAT网关
tccli vpc AssociateNatGatewayAddress --region ap-guangzhou \
  --NatGatewayId ngw-xxxxxxxx \
  --PublicIpAddress eip-xxxxxxxx

# 创建对等连接
tccli vpc CreateVpcPeeringConnection --region ap-guangzhou \
  --VpcId vpc-xxxxxxxx \
  --PeerVpcId vpc-yyyyyyyy \
  --PeerRegion ap-beijing \
  --Name my-peering

# 查询网络ACL
tccli vpc DescribeNetworkAcls --region ap-guangzhou --VpcId vpc-xxxxxxxx

# 创建网络ACL
tccli vpc CreateNetworkAcl --region ap-guangzhou \
  --VpcId vpc-xxxxxxxx \
  --AclName my-acl

# 添加网络ACL规则
tccli vpc AddNetworkAclEntries --region ap-guangzhou \
  --NetworkAclId acl-xxxxxxxx \
  --IngressEntries '[{"Protocol":"TCP","Port":"22","Action":"ACCEPT","CidrBlock":"0.0.0.0/0","Description":"SSH"}]'
```

---

### CLB负载均衡

```bash
# 查询CLB实例列表
tccli clb DescribeLoadBalancers --region ap-guangzhou
# 输出:
# {
#   "LoadBalancerSet": [
#     {
#       "LoadBalancerId": "lb-xxxxxxxx",
#       "LoadBalancerName": "my-clb",
#       "LoadBalancerType": "public",
#       "Vip": "43.123.45.67",
#       "Status": "active"
#     }
#   ],
#   "TotalCount": 1
# }

# 创建公网CLB
tccli clb CreateLoadBalancers --region ap-guangzhou \
  --LoadBalancerType open \
  --InternetChargeType BANDWIDTH_POSTPAID \
  --InternetMaxBandwidth 100 \
  --LoadBalancerName my-clb
# 输出:
# {
#   "LoadBalancerIds": ["lb-xxxxxxxx"],
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 创建内网CLB
tccli clb CreateLoadBalancers --region ap-guangzhou \
  --LoadBalancerType internal \
  --VpcId vpc-xxxxxxxx \
  --SubnetId subnet-xxxxxxxx \
  --LoadBalancerName my-internal-clb

# 查询CLB后端服务器
tccli clb DescribeTargets --region ap-guangzhou --LoadBalancerId lb-xxxxxxxx
# 输出:
# {
#   "Listeners": [
#     {
#       "ListenerId": "lbl-xxxxxxxx",
#       "Protocol": "TCP",
#       "Port": 80,
#       "Rules": []
#     }
#   ]
# }

# 绑定后端服务器
tccli clb RegisterTargets --region ap-guangzhou \
  --LoadBalancerId lb-xxxxxxxx \
  --TargetList '[{"InstanceId":"ins-xxxxxxxxx","Port":80,"Weight":100}]' \
  --ListenerUids '["lbl-xxxxxxxx"]' \
  --Protocol TCP \
  --Port 80

# 解绑后端服务器
tccli clb DeregisterTargets --region ap-guangzhou \
  --LoadBalancerId lb-xxxxxxxx \
  --TargetList '[{"InstanceId":"ins-xxxxxxxxx","Port":80}]' \
  --ListenerUids '["lbl-xxxxxxxx"]' \
  --Protocol TCP \
  --Port 80

# 创建TCP监听器
tccli clb CreateListeners --region ap-guangzhou \
  --LoadBalancerId lb-xxxxxxxx \
  --Listeners '[{"Protocol":"TCP","ListenerPort":80,"HealthCheckSwitch":true,"HealthCheckTimeOut":2}]'
# 输出:
# {
#   "ListenerIds": ["lbl-xxxxxxxx"],
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 创建HTTP监听器
tccli clb CreateListeners --region ap-guangzhou \
  --LoadBalancerId lb-xxxxxxxx \
  --Listeners '[{"Protocol":"HTTP","ListenerPort":80,"Scheduler":"roundrobin","KeepaliveEnable":true}]'

# 创建HTTPS监听器
tccli clb CreateListeners --region ap-guangzhou \
  --LoadBalancerId lb-xxxxxxxx \
  --Listeners '[{"Protocol":"HTTPS","ListenerPort":443,"CertificateSSLId":"a1b2c3d4"}]'

# 修改CLB属性
tccli clb ModifyLoadBalancerAttributes --region ap-guangzhou \
  --LoadBalancerId lb-xxxxxxxx \
  --LoadBalancerName new-clb-name

# 设置权重
tccli clb ModifyTargetWeight --region ap-guangzhou \
  --LoadBalancerId lb-xxxxxxxx \
  --TargetList '[{"InstanceId":"ins-xxxxxxxxx","Port":80,"Weight":50}]' \
  --ListenerUids '["lbl-xxxxxxxx"]' \
  --Protocol TCP \
  --Port 80

# 查询健康检查状态
tccli clb DescribeTargetHealth --region ap-guangzhou --LoadBalancerId lb-xxxxxxxx

# 删除监听器
tccli clb DeleteListeners --region ap-guangzhou \
  --LoadBalancerId lb-xxxxxxxx \
  --ListenerIds '["lbl-xxxxxxxx"]'
```

---

### 专线连接

```bash
# 查询专线网关列表
tccli vpc DescribeDirectConnectGateways --region ap-guangzhou
# 输出:
# {
#   "DirectConnectGatewaySet": [
#     {
#       "DirectConnectGatewayId": "dcg-xxxxxxxx",
#       "DirectConnectGatewayName": "my-dcg",
#       "DirectConnectGatewayType": "NORMAL",
#       "VpcId": "vpc-xxxxxxxx",
#       "CreateTime": "2024-06-15 10:30:00"
#     }
#   ]
# }

# 创建专线网关
tccli vpc CreateDirectConnectGateway --region ap-guangzhou \
  --DirectConnectGatewayName my-dcg \
  --VpcId vpc-xxxxxxxx \
  --DirectConnectGatewayType NORMAL

# 删除专线网关
tccli vpc DeleteDirectConnectGateway --region ap-guangzhou --DirectConnectGatewayId dcg-xxxxxxxx

# 创建专线通道
tccli vpc CreateDirectConnectTunnel --region ap-guangzhou \
  --DirectConnectGatewayId dcg-xxxxxxxx \
  --DirectConnectTunnelName my-tunnel \
  --TencentAddress 10.0.0.1/30 \
  --CustomerAddress 10.0.0.2/30 \
  --Bandwidth 1000

# 查询专线通道
tccli vpc DescribeDirectConnectTunnels --region ap-guangzhou --DirectConnectTunnelId dct-xxxxxxxx

# 修改专线通道
tccli vpc ModifyDirectConnectTunnelAttribute --region ap-guangzhou \
  --DirectConnectTunnelId dct-xxxxxxxx \
  --Bandwidth 2000
```

---

### VPN网关

```bash
# 查询VPN网关列表
tccli vpc DescribeVpnGateways --region ap-guangzhou
# 输出:
# {
#   "VPNGatewaySet": [
#     {
#       "VPNGatewayId": "vpngw-xxxxxxxx",
#       "VPNGatewayName": "my-vpngw",
#       "VpcId": "vpc-xxxxxxxx",
#       "PublicIp": "43.123.45.67",
#       "State": "available",
#       "Bandwidth": 100
#     }
#   ]
# }

# 创建VPN网关
tccli vpc CreateVpnGateway --region ap-guangzhou \
  --VPNGatewayName my-vpngw \
  --VpcId vpc-xxxxxxxx \
  --Bandwidth 100 \
  --PreShareKey MySecureKey

# 删除VPN网关
tccli vpc DeleteVpnGateway --region ap-guangzhou --VPNGatewayId vpngw-xxxxxxxx

# 查询SSL-VPN网关
tccli vpc DescribeSSLVPNGateways --region ap-guangzhou --VPNGatewayId vpngw-xxxxxxxx

# 创建SSL-VPN网关
tccli vpc CreateSSLVPNGateway --region ap-guangzhou \
  --VPNGatewayId vpngw-xxxxxxxx \
  --SSLVPNServerName my-ssl-server \
  --LocalCidr '["10.0.1.0/24"]'

# 查询VPN通道
tccli vpc DescribeVpnConnections --region ap-guangzhou --VPNGatewayId vpngw-xxxxxxxx

# 创建VPN通道
tccli vpc CreateVpnConnection --region ap-guangzhou \
  --VPNGatewayId vpngw-xxxxxxxx \
  --VpnConnectionName my-vpn \
  --PreShareKey MySecureKey \
  --RemoteCidr '["192.168.0.0/16"]' \
  --LocalCidr '["10.0.1.0/24"]' \
  --encryptProtocol AES-256-CBC
```

---

## 内容分发CDN

```bash
# 添加加速域名
tccli cdn AddCdnDomain --region ap-guangzhou \
  --Domain example.com \
  --ServiceType web \
  --Origin '{"Origins":["oss.example.com"],"OriginType":"cos"}' \
  --Area mainland
# 输出:
# {
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
#   "Domain": "example.com"
# }

# 查询加速域名列表
tccli cdn DescribeCdnDomains --region ap-guangzhou
# 输出:
# {
#   "Domains": [
#     {
#       "ResourceId": "example.com",
#       "Domain": "example.com",
#       "ServiceType": "web",
#       "Status": "online",
#       "Cname": "example.com.cdn.dnsv1.com",
#       "CreateTime": "2024-06-15 10:30:00"
#     }
#   ],
#   "TotalCount": 1
# }

# 启用加速域名
tccli cdn StartCdnDomain --region ap-guangzhou --Domain example.com

# 停用加速域名
tccli cdn StopCdnDomain --region ap-guangzhou --Domain example.com

# 刷新缓存
tccli cdn PurgeCdnCache --region ap-guangzhou \
  --Urls '["http://example.com/index.html","http://example.com/css/*.css"]'
# 输出:
# {
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
#   "TaskId": "purge-xxxxxxxx"
# }

# 预热缓存
tccli cdn PushCdnCache --region ap-guangzhou \
  --Urls '["http://example.com/images/banner.jpg"]'
# 输出:
# {
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
#   "TaskId": "preload-xxxxxxxx"
# }

# 查询CDN访问日志
tccli cdn DescribeCdnLogs --region ap-guangzhou \
  --Domain example.com \
  --StartTime "2024-06-15 00:00:00" \
  --EndTime "2024-06-15 23:59:59"

# 查询CDN数据统计
tccli cdn DescribeCdnData --region ap-guangzhou \
  --Metric traffic \
  --StartTime "2024-06-15 00:00:00" \
  --EndTime "2024-06-15 23:59:59" \
  --Domains '["example.com"]'
# 输出:
# {
#   "Data": [
#     {
#       "Value": 1024000,
#       "Time": "2024-06-15T00:00:00Z"
#     }
#   ]
# }

# 配置缓存规则
tccli cdn SetCdnConfig --region ap-guangzhou \
  --Domain example.com \
  --Cache rules '[{"RuleType":"suffix","RulePaths":[".jpg",".png"],"TTL":31536000,"Weight":1}]'

# 设置防盗链
tccli cdn SetCdnDomainReferer --region ap-guangzhou \
  --Domain example.com \
  --RefererType whitelist \
  --Referers '["*.example.com","example.com"]'

# 修改回源配置
tccli cdn UpdateDomainConfig --region ap-guangzhou \
  --Domain example.com \
  --Origin '{"Origins":["new-origin.example.com"],"OriginType":"cos"}'

# 查询HTTPS证书
tccli cdn DescribeCdnCertificates --region ap-guangzhou --Domain example.com
```

---

## 安全服务

### 密钥管理KMS

```bash
# 查询密钥列表
tccli kms ListKey --region ap-guangzhou
# 输出:
# {
#   "Keys": [
#     {
#       "KeyId": "key-xxxxxxxx",
#       "KeyAlias": "my-key",
#       "KeyState": "Enabled",
#       "KeyUsage": "ENCRYPT_DECRYPT",
#       "CreateTime": "2024-06-15 10:30:00"
#     }
#   ],
#   "TotalCount": 1
# }

# 创建密钥
tccli kms CreateKey --region ap-guangzhou \
  --KeyAlias my-key \
  --KeyUsage ENCRYPT_DECRYPT \
  --KeyType DEFAULT \
  --Description "My encryption key"
# 输出:
# {
#   "Key": {
#     "KeyId": "key-xxxxxxxx",
#     "KeyAlias": "my-key"
#   },
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 查询密钥信息
tccli kms DescribeKey --region ap-guangzhou --KeyId key-xxxxxxxx
# 输出:
# {
#   "Key": {
#     "KeyId": "key-xxxxxxxx",
#     "KeyAlias": "my-key",
#     "KeyState": "Enabled",
#     "KeyUsage": "ENCRYPT_DECRYPT",
#     "CreateTime": "2024-06-15T10:30:00Z"
#   }
# }

# 加密数据
tccli kms Encrypt --region ap-guangzhou \
  --KeyId key-xxxxxxxx \
  --PlainText "SGVsbG8gV29ybGQ="
# 输出:
# {
#   "CiphertextBlob": "CiC7V2xp...",
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 解密数据
tccli kms Decrypt --region ap-guangzhou \
  --CiphertextBlob "CiC7V2xp..."
# 输出:
# {
#   "PlainText": "SGVsbG8gV29ybGQ=",
#   "KeyId": "key-xxxxxxxx"
# }

# 生成数据密钥
tccli kms GenerateDataKey --region ap-guangzhou \
  --KeyId key-xxxxxxxx \
  --KeySpec 1 \
  --NumberOfBytes 32
# 输出:
# {
#   "PlainText": "YWFhYmNjZGVmZ2hpamtsbW5vcA==",
#   "CiphertextBlob": "CiC7...",
#   "KeyId": "key-xxxxxxxx"
# }

# 计划删除密钥
tccli kms ScheduleKeyDeletion --region ap-guangzhou \
  --KeyId key-xxxxxxxx \
  --PendingWindowInDays 7

# 取消密钥删除计划
tccli kms CancelKeyDeletion --region ap-guangzhou --KeyId key-xxxxxxxx

# 禁用密钥
tccli kms DisableKey --region ap-guangzhou --KeyId key-xxxxxxxx

# 启用密钥
tccli kms EnableKey --region ap-guangzhou --KeyId key-xxxxxxxx
```

---

### 云防火墙CFW

```bash
# 查询安全组列表
tccli cvm DescribeSecurityGroups --region ap-guangzhou
# 输出:
# {
#   "SecurityGroupSet": [
#     {
#       "SecurityGroupId": "sg-xxxxxxxx",
#       "SecurityGroupName": "my-sg",
#       "ProjectId": 0,
#       "CreateTime": "2024-06-15 10:30:00"
#     }
#   ],
#   "TotalCount": 1
# }

# 创建安全组
tccli cvm CreateSecurityGroup --region ap-guangzhou \
  --SecurityGroupName my-sg \
  --Description "My security group"
# 输出:
# {
#   "SecurityGroupId": "sg-yyyyyyyy",
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 安全组授权
tccli cvm AuthorizeSecurityGroup --region ap-guangzhou \
  --SecurityGroupId sg-xxxxxxxx \
  --Permission '{"Direction":"ingress","Protocol":"TCP","PortRange":"22","CidrBlock":"0.0.0.0/0","Action":"accept"}'

# 安全组删除授权
tccli cvm RevokeSecurityGroup --region ap-guangzhou \
  --SecurityGroupId sg-xxxxxxxx \
  --Permission '{"Direction":"ingress","Protocol":"TCP","PortRange":"22","CidrBlock":"0.0.0.0/0"}'

# 查询安全组规则
tccli cvm DescribeSecurityGroupPolicy --region ap-guangzhou --SecurityGroupId sg-xxxxxxxx
# 输出:
# {
#   "SecurityGroupPolicySet": {
#     "Ingress": [
#       {
#         "Direction": "ingress",
#         "Protocol": "TCP",
#         "Port": "22",
#         "CidrBlock": "0.0.0.0/0",
#         "Action": "accept"
#       }
#     ]
#   }
# }

# 修改安全组属性
tccli cvm ModifySecurityGroupAttribute --region ap-guangzhou \
  --SecurityGroupId sg-xxxxxxxx \
  --SecurityGroupName new-sg-name

# 绑定安全组到实例
tccli cvm AssociateSecurityGroups --region ap-guangzhou \
  --SecurityGroupIds '["sg-xxxxxxxx"]' \
  --InstanceIds '["ins-xxxxxxxxx"]'
```

---

### WAFWeb应用防火墙

```bash
# 查询WAF实例
tccli waf DescribeDomain --region ap-guangzhou --Domain example.com
# 输出:
# {
#   "DomainList": [
#     {
#       "Domain": "example.com",
#       "Status": "1",
#       "Mode": "proxy"
#     }
#   ]
# }

# 添加防护域名
tccli waf CreateHost --region ap-guangzhou \
  --Domain example.com \
  --InstanceID waf-xxxxxxxx \
  --LoadBalanceStation "http://127.0.0.1:8080" \
  --ProxySetup

# 开启防护
tccli waf ModifyHostDomain --region ap-guangzhou \
  --Domain example.com \
  --DomainSet

# 关闭防护
tccli waf ModifyHostDomain --region ap-guangzhou \
  --Domain example.com \
  --DomainSet

# 查询攻击日志
tccli waf DescribeAttackLog --region ap-guangzhou \
  --StartTime "2024-06-15 00:00:00" \
  --EndTime "2024-06-15 23:59:59"

# 查询防护配置
tccli waf DescribeDomainConfig --region ap-guangzhou --Domain example.com \
  --Clspw

# 设置CC防护
tccli waf ModifyAreaHostConfig --region ap-guangzhou \
  --Domain example.com \
  --HostType clspw/cc_mode

# 设置IP封禁
tccli waf CreateIpAccessControl --region ap-guangzhou \
  --IpList "1.2.3.4" \
  --IpType 0

# 查询爬虫日志
tccli waf DescribeBotLog --region ap-guangzhou --Domain example.com
```

---

## 中间件服务

### CMQ消息队列

```bash
# 查询队列列表
tccli cmq DescribeQueue --region ap-guangzhou --QueueName my-queue
# 输出:
# {
#   "QueueSet": [
#     {
#       "QueueId": "queue-xxxxxxxx",
#       "QueueName": "my-queue",
#       "MaxMsgHeapNum": 100000,
#       "PollingWaitSeconds": 0,
#       "VisibilityTimeout": 30,
#       "CreateTime": 1718436600
#     }
#   ],
#   "TotalCount": 1
# }

# 创建队列
tccli cmq CreateQueue --region ap-guangzhou \
  --QueueName my-queue \
  --MaxMsgHeapNum 100000 \
  --PollingWaitSeconds 5 \
  --VisibilityTimeout 30 \
  --MsgRetentionSeconds 345600
# 输出:
# {
#   "QueueId": "queue-xxxxxxxx",
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 列出队列
tccli cmq ListQueue --region ap-guangzhou
# 输出:
# {
#   "QueueList": ["my-queue", "another-queue"],
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 发送消息
tccli cmq SendMessage --region ap-guangzhou \
  --QueueName my-queue \
  --MsgBody "Hello World" \
  --DelaySeconds 0
# 输出:
# {
#   "MsgId": "msg-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 接收消息
tccli cmq ReceiveMessage --region ap-guangzhou \
  --QueueName my-queue \
  --PoleWaitTime 5
# 输出:
# {
#   "MsgBody": "Hello World",
#   "MsgId": "msg-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
#   "ReceiptHandle": "xxxxxx",
#   "DequeueCount": 1
# }

# 删除消息
tccli cmq DeleteMessage --region ap-guangzhou \
  --QueueName my-queue \
  --ReceiptHandle xxxxxx

# 删除队列
tccli cmq DeleteQueue --region ap-guangzhou --QueueName my-queue

# 发送批量消息
tccli cmq BatchSendMessage --region ap-guangzhou \
  --QueueName my-queue \
  --MsgBody.n '["msg1","msg2","msg3"]'
```

---

### CKafka消息队列

```bash
# 查询CKafka实例列表
tccli ckafka DescribeInstances --region ap-guangzhou
# 输出:
# {
#   "InstanceList": [
#     {
#       "InstanceId": "ckafka-xxxxx",
#       "InstanceName": "my-kafka",
#       "Status": 1,
#       "Version": "2.7.0"
#     }
#   ],
#   "TotalCount": 1
# }

# 创建CKafka实例
tccli ckafka CreateInstance --region ap-guangzhou \
  --InstanceName my-kafka \
  --ZoneId "ap-guangzhou-3" \
  --Bandwidth 100 \
  --DiskSize 300 \
  --DiskType CLOUD_BSSD \
  --KafkaVersion 2.7.0

# 创建Topic
tccli ckafka CreateTopic --region ap-guangzhou \
  --InstanceId ckafka-xxxxx \
  --TopicName my-topic \
  --PartitionNum 6 \
  --ReplicaNum 3
# 输出:
# {
#   "TopicId": "topic-xxxxxxxx",
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 查询Topic列表
tccli ckafka DescribeTopic --region ap-guangzhou --InstanceId ckafka-xxxxx
# 输出:
# {
#   "TopicList": [
#     {
#       "TopicId": "topic-xxxxxxxx",
#       "TopicName": "my-topic",
#       "PartitionNum": 6,
#       "ReplicaNum": 3
#     }
#   ]
# }

# 查询Consumer Group列表
tccli ckafka ListConsumerGroup --region ap-guangzhou \
  --InstanceId ckafka-xxxxx

# 创建Consumer Group
tccli ckafka CreateConsumerGroup --region ap-guangzhou \
  --InstanceId ckafka-xxxxx \
  --GroupName my-consumer-group \
  --ConsumeRule 1
# 输出:
# {
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 生产消息
tccli ckafka ProduceMessage --region ap-guangzhou \
  --InstanceId ckafka-xxxxx \
  --TopicName my-topic \
  --Messages '[{"Body":"test message"}]'

# 删除Topic
tccli ckafka DeleteTopic --region ap-guangzhou \
  --InstanceId ckafka-xxxxx \
  --TopicName my-topic

# 变配实例
tccli ckafka ModifyInstanceAttributes --region ap-guangzhou \
  --InstanceId ckafka-xxxxx \
  --Bandwidth 200
```

---

### TDMQ分布式消息

```bash
# 查询TDMQ命名空间
tccli tdmq DescribeEnvironments --region ap-guangzhou
# 输出:
# {
#   "EnvironmentSet": [
#     {
#       "EnvironmentId": "namespace-xxxxx",
#       "EnvironmentName": "my-namespace",
#       "Remark": "",
#       "CreateTime": 1718436600
#     }
#   ]
# }

# 创建命名空间
tccli tdmq CreateEnvironment --region ap-guangzhou \
  --EnvironmentId my-namespace \
  --EnvironmentName "My Namespace" \
  --RetentionMinutes 10080

# 创建Topic
tccli tdmq CreateTopic --region ap-guangzhou \
  --EnvironmentId my-namespace \
  --TopicName my-topic \
  --Partitions 6 \
  --RetentionMinutes 10080
# 输出:
# {
#   "TopicId": "topic-xxxxxxxx",
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 查询Subscription
tccli tdmq DescribeSubscriptions --region ap-guangzhou \
  --EnvironmentId my-namespace \
  --TopicName my-topic
# 输出:
# {
#   "SubscriptionSet": [
#     {
#       "SubscriptionId": "sub-xxxxxxxx",
#       "TopicName": "my-topic",
#       "ConsumerGroup": "my-group"
#     }
#   ]
# }

# 创建Subscription
tccli tdmq CreateSubscription --region ap-guangzhou \
  --EnvironmentId my-namespace \
  --TopicName my-topic \
  --SubscriptionName my-subscription \
  --ConsumerGroup my-group

# 发送消息
tccli tdmq ProduceMessage --region ap-guangzhou \
  --EnvironmentId my-namespace \
  --TopicName my-topic \
  --Body "Hello TDMQ"

# 重置消费位点
tccli tdmq ResetMsgSubOffset --region ap-guangzhou \
  --EnvironmentId my-namespace \
  --TopicName my-topic \
  --SubscriptionName my-subscription \
  --OffsetTimestamp 1718436600
```

---

## 监控运维

### 云监控CM

```bash
# 查询告警列表
tccli monitor DescribeBasicAlarmList --region ap-guangzhou \
  --StartTime 1718436600 \
  --EndTime 1718523000
# 输出:
# {
#   "Alarms": [
#     {
#       "EventObj": {
#         "AlarmId": "alarm-xxxxxxxx",
#         "MetricName": "CPU",
#         "Value": 95,
#         "InstanceId": "ins-xxxxxxxxx"
#       }
#     }
#   ],
#   "TotalCount": 1
# }

# 创建告警策略
tccli monitor CreatePolicy --region ap-guangzhou \
  --PolicyName "High CPU Alert" \
  --MetricNamespace acs_ecs_dashboard \
  --MetricName cpu_idle \
  --Period 300 \
  --Statistics Average \
  --Condition '{"ComparisonOperator":"LessThan","Threshold":30}'
# 输出:
# {
#   "PolicyId": "policy-xxxxxxxx",
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 绑定告警对象
tccli monitor BindPolicy --region ap-guangzhou \
  --PolicyId policy-xxxxxxxx \
  --BindingDimensions '{"InstanceId":"ins-xxxxxxxxx"}' \
  --Enable 1

# 上报自定义指标
tccli monitor PutMetricData --region ap-guangzhou \
  --Metrics '[{"MetricName":"sales","Value":100,"Unit":"count","Dimensions":{"instance":"i-001"}}]'
# 输出:
# {
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 查询监控数据
tccli monitor GetMonitorData --region ap-guangzhou \
  --Namespace acs_ecs_dashboard \
  --MetricName cpu_idle \
  --StartTime 1718436600 \
  --EndTime 1718523000 \
  --Period 300 \
  --Instances '[{"InstanceId":"ins-xxxxxxxxx"}]'
# 输出:
# {
#   "DataPoints": [
#     {
#       "Timestamps": [1718436600, 1718436900],
#       "Values": [95.5, 92.3]
#     }
#   ]
# }

# 查询指标列表
tccli monitor DescribeMonitorProducts --region ap-guangzhou

# 删除告警策略
tccli monitor DeletePolicy --region ap-guangzhou --PolicyId policy-xxxxxxxx

# 查询告警历史
tccli monitor DescribeAlarmHistory --region ap-guangzhou \
  --StartTime 1718436600 \
  --EndTime 1718523000

# 创建服务发现
tccli monitor CreateServiceDiscovery --region ap-guangzhou \
  --Name "my-discovery" \
  --CollectMetrics '[{"MetricName":"custom_metric","CollectInterval":60}]'
```

---

### 运维编排

```bash
# 查询执行任务列表
tccli.tat DescribeExecutionTasks --region ap-guangzhou
# 输出:
# {
#   "ExecutionTasks": [
#     {
#       "ExecutionTaskId": "task-xxxxxxxx",
#       "Status": "Success",
#       "StartTime": "2024-06-15 10:30:00",
#       "EndTime": "2024-06-15 10:35:00"
#     }
#   ]
# }

# 创建模板
tccli.tat CreateTemplate --region ap-guangzhou \
  --TemplateName my-template \
  --Content '{"format":"cloudformat","version":"1.0","tasks":[]}'
# 输出:
# {
#   "TemplateId": "template-xxxxxxxx",
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 执行模板
tccli.tat InvokeCommand --region ap-guangzhou \
  --CommandId cmd-xxxxxxxx \
  --InstanceIds '["ins-xxxxxxxxx"]'

# 查询命令执行结果
tccli.tat DescribeInvocations --region ap-guangzhou \
  --InvocationId inv-xxxxxxxx

# 创建定时任务
tccli.tat CreateSchedule --region ap-guangzhou \
  --ScheduleName my-schedule \
  --CronExpression "0 0 * * *" \
  --CommandId cmd-xxxxxxxx \
  --InstanceIds '["ins-xxxxxxxxx"]'
```

---

## 访问控制CAM

```bash
# 查询用户列表
tccli cam ListUser --region ap-guangzhou
# 输出:
# {
#   "UserList": [
#     {
#       "Uin": 123456789,
#       "Name": "alice",
#       "Uid": 1000000001,
#       "CreateTime": "2024-06-15 10:30:00",
#       "Remark": "",
#       "ConsoleLogin": "enable"
#     }
#   ],
#   "TotalNum": 1
# }

# 创建子用户
tccli cam CreateUser --region ap-guangzhou \
  --Name alice \
  --Remark "Alice from engineering team" \
  --ConsoleLogin enable \
  --Password MyP@ssw0rd!
# 输出:
# {
#   "Uin": 123456789,
#   "Name": "alice",
#   "SecretId": "AKIDxxxxxxxxxxxxxxxxxxxxx",
#   "SecretKey": "****************",
#   "Uid": 1000000001
# }

# 创建访问密钥
tccli cam CreateAccessKey --region ap-guangzhou --SecretId
# 输出:
# {
#   "AccessKey": {
#     "SecretId": "AKIDyyyyyyyyyyyyyyyyyyyy",
#     "SecretKey": "****************"
#   },
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 创建自定义策略
tccli cam CreatePolicy --region ap-guangzhou \
  --PolicyName my-policy \
  --PolicyDocument '{"version":"2.0","statement":[{"action":["cvm:Describe*"],"resource":["*"],"effect":"allow"}]}'
# 输出:
# {
#   "PolicyId": "p-xxxxxxxx",
#   "RequestId": "3c140006-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# 绑定策略到用户
tccli cam AttachUserPolicy --region ap-guangzhou \
  --PolicyId p-xxxxxxxx \
  --AttachUin 123456789

# 解绑策略
tccli cam DetachUserPolicy --region ap-guangzhou \
  --PolicyId p-xxxxxxxx \
  --AttachUin 123456789

# 查询用户权限
tccli cam ListAttachedUserPolicies --region ap-guangzhou --Uin 123456789

# 创建角色
tccli cam CreateRole --region ap-guangzhou \
  --RoleName my-role \
  --RoleStatement '[{"Effect":"allow","Action":["cvm:DescribeInstances"],"Resource":["qcs::cvm:::*:instance/*"]}]'
# 输出:
# {
#   "RoleId": "461574538",
#   "RoleName": "my-role"
# }

# 绑定策略到角色
tccli cam AttachRolePolicy --region ap-guangzhou \
  --PolicyId p-xxxxxxxx \
  --RoleId 461574538

# 查询角色列表
tccli cam ListRole --region ap-guangzhou
# 输出:
# {
#   "List": [
#     {
#       "RoleId": "461574538",
#       "RoleName": "my-role",
#       "CreateTime": "2024-06-15T10:30:00Z"
#     }
#   ]
# }

# 创建用户组
tccli cam AddUserToGroup --region ap-guangzhou \
  --GroupId 12345 \
  --Uins '["123456789"]'

# 查询用户组
tccli cam ListGroup --region ap-guangzhou

# 列出策略
tccli cam ListPolicy --region ap-guangzhou
# 输出:
# {
#   "List": [
#     {
#       "PolicyId": "p-xxxxxxxx",
#       "PolicyName": "my-policy",
#       "CreateMode": "CUSTOM"
#     }
#   ]
# }
```

---

## 附录产品CLI名称映射表

| 产品类别 | CLI服务名 | 控制台名称 | API前缀 | 地域示例 |
|:---|:---|:---|:---|:---|
| 云服务器 | `cvm` | CVM | CVM | ap-guangzhou |
| 容器服务 | `tke` | TKE | TKE | ap-guangzhou |
| 云函数 | `scf` | SCF | SCF | ap-guangzhou |
| 对象存储 | `cos` | COS | COS | - |
| 云硬盘 | `cbs` | CBS | CBS | ap-guangzhou |
| 文件存储 | `cfs` | CFS | CFS | ap-guangzhou |
| MySQL/PostgreSQL | `cdb` | CDB | CDB | ap-guangzhou |
| Redis | `redis` | Redis | CRS | ap-guangzhou |
| MongoDB | `mongo` | MongoDB | MongoDB | ap-guangzhou |
| 私有网络 | `vpc` | VPC | VPC | ap-guangzhou |
| 负载均衡 | `clb` | CLB | LB | ap-guangzhou |
| 内容分发 | `cdn` | CDN | CDN | - |
| 密钥管理 | `kms` | KMS | KMS | ap-guangzhou |
| 访问控制 | `cam` | CAM | CAM | - |
| 消息队列CMQ | `cmq` | CMQ | CMQ | ap-guangzhou |
| Kafka | `ckafka` | CKafka | CKafka | ap-guangzhou |
| TDMQ | `tdmq` | TDMQ | TDMQ | ap-guangzhou |
| 云监控 | `monitor` | 云监控 | Monitor | ap-guangzhou |
| 运维编排 | `tat` | 运维编排 | TAS | ap-guangzhou |
| WAF | `waf` | WAF | WAF | ap-guangzhou |

---

## 常用命令速查

```bash
# 查看帮助
tccli help

# 查看具体服务帮助
tccli cvm help
tccli vpc help

# 查询可用地域
tccli cvm DescribeRegions --endpoint cvm.tencentcloudapi.com

# 查询可用AZ
tccli cvm DescribeZoneConfig --region ap-guangzhou

# 快速查看账户信息
tccli cam GetUserAppIdInfo
```

---

> 文档版本: v1.0
> 更新时间: 2024/06
> 腾讯云CLI版本: tccli >= 3.0.136
> 官方文档: https://cloud.tencent.com/document/product/1270