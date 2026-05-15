# 火山引擎CLI命令速查表

> 火山引擎命令行工具完整参考手册，覆盖计算、存储、数据库、网络、安全等核心产品线

**文档版本**: v1.0 | **更新时间**: 2026/05

---

## 目录

1. [安装与配置](#1-安装与配置)
2. [计算服务](#2-计算服务)
3. [存储服务](#3-存储服务)
4. [数据库服务](#4-数据库服务)
5. [网络服务](#5-网络服务)
6. [安全服务](#6-安全服务)
7. [监控与日志](#7-监控与日志)
8. [中间件服务](#8-中间件服务)
9. [容器服务](#9-容器服务)
10. [资源管理与权限](#10-资源管理与权限)
11. [附录：产品CLI名称映射表](#11-附录产品cli名称映射表)

---

## 1. 安装与配置

### 1.1 安装 CLI

#### Linux/macOS 安装

```bash
# 通过安装脚本自动安装
curl -fsSL https://veutunnel.com/tools/vke/install-cli.sh | bash

# 或者通过包管理器安装 (macOS)
brew install volcengine-cli

# 验证安装
volcengine-cli version
```

**输出示例**:
```
Volcengine CLI version 1.2.3
Build Date: 2026-03-15
Go Version: go1.21.5
```

#### Windows 安装

```powershell
# 通过 PowerShell 安装
irm https://veutunnel.com/tools/vke/install-cli.ps1 | iex

# 或下载 MSI 安装包后双击安装
```

### 1.2 配置凭证

```bash
# 交互式配置 (推荐)
volcengine-cli configure

# 输出示例:
# Configure Guide:
# 1. Access Key ID: AKLT ********  # 输入您的Access Key ID
# 2. Access Key Secret: ********  # 输入您的Access Key Secret
# 3. Default Region [cn-beijing]: # 选择默认区域
# 4. Output Format [json]:        # 选择输出格式 (json/text/table)
# Configure success!
```

#### 非交互式配置

```bash
# 直接通过命令行配置凭证
volcengine-cli configure set-access-key --access-key-id AKLT你的AccessKeyID
volcengine-cli configure set-access-key-secret --access-key-secret 你的SecretKey

# 配置默认区域
volcengine-cli configure set-region --region cn-beijing
```

#### 凭证文件位置

```
~/.volcengine/config.toml
```

**config.toml 示例内容**:
```toml
[default]
access_key_id = "AKLT****************************"
access_key_secret = "****************************"
region = "cn-beijing"
output = "json"

[profile-dev]
access_key_id = "AKLT****************************"
access_key_secret = "****************************"
region = "cn-shanghai"
output = "table"
```

### 1.3 全局参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--region` | 指定目标区域 | `--region cn-beijing` |
| `--output` | 指定输出格式 | `--output json` |
| `--profile` | 指定配置 Profile | `--profile dev` |
| `--endpoint` | 指定自定义端点 | `--endpoint https://ecs.volcengineapi.com` |
| `--version` | 指定 API 版本 | `--version 2022-01-01` |
| `--debug` | 开启调试模式 | `--debug` |
| `--no-params-check` | 跳过参数检查 | `--no-params-check` |

```bash
# 常用组合示例
volcengine-cli ecs DescribeInstances --region cn-beijing --output table
volcengine-cli ecs DescribeInstances --region cn-shanghai --profile dev --output json
```

### 1.4 多账户管理

```bash
# 列出所有 Profile
volcengine-cli configure list-profiles

# 创建新 Profile
volcengine-cli configure add-profile --profile test --access-key-id AKLT*** --access-key-secret ***

# 删除 Profile
volcengine-cli configure delete-profile --profile test

# 切换默认 Profile
volcengine-cli configure set-default-profile --profile dev
```

---

## 2. 计算服务

### 2.1 ECS 云服务器

#### 查询实例列表

```bash
volcengine-cli ecs DescribeInstances --region cn-beijing
```

**输出示例** (JSON 格式):
```json
{
  "Instances": [
    {
      "InstanceId": "i-2zeaf0ls2p7k9****",
      "InstanceName": "web-server-01",
      "InstanceType": "ecs.c3.large",
      "Status": "Running",
      "ZoneId": "cn-beijing-a",
      "VpcId": "vpc-2ze4j7g9****",
      "VSwitchId": "vsw-2ze8f3k6****",
      "PublicIp": ["120.92.168.***"],
      "CreatedAt": "2026-01-15T08:30:00Z",
      "Tags": [
        {"Key": "Environment", "Value": "Production"},
        {"Key": "Project", "Value": "WebApp"}
      ]
    }
  ],
  "TotalCount": 1,
  "PageSize": 10,
  "PageNumber": 1
}
```

#### 筛选条件查询

```bash
# 按状态筛选运行中的实例
volcengine-cli ecs DescribeInstances --RegionId cn-beijing --InstanceType ecs.c3.large --Status Running

# 按标签筛选
volcengine-cli ecs DescribeInstances --TagFilters "[{\"Key\":\"Environment\",\"Values\":[\"Production\"]}]"

# 按 VPC 筛选
volcengine-cli ecs DescribeInstances --VpcId vpc-2zeaf0ls2p7k9****
```

#### 创建实例

```bash
volcengine-cli ecs RunInstances --region cn-beijing \
  --InstanceType ecs.c3.large \
  --ImageId img-2zeaf0ls2p7k9**** \
  --InstanceName web-server-new \
  --VSwitchId vsw-2ze8f3k6**** \
  --SecurityGroupIds '["sg-2ze4j7g9****"]' \
  --DiskMappings '[{"DiskType":"ESSD","DiskSize":50}]' \
  --Password "YourPassWord123!" \
  --Count 1
```

**输出示例**:
```json
{
  "InstanceId": "i-2zeaf0ls2p8k****",
  "TradeHost": "172.20.123.45",
  "RequestId": "8d8f5e28-4e73-41b2-9f1a-4f8c8a9b7c6d"
}
```

#### 停止实例

```bash
# 停止单个实例
volcengine-cli ecs StopInstances --RegionId cn-beijing --InstanceIds '["i-2zeaf0ls2p8k****"]'

# 强制停止
volcengine-cli ecs StopInstances --RegionId cn-beijing --InstanceIds '["i-2zeaf0ls2p8k****"]' --ForceStop true
```

**输出示例**:
```json
{
  "RequestId": "8d8f5e28-4e73-41b2-9f1a-4f8c8a9b7c6d",
  "Results": [
    {"InstanceId": "i-2zeaf0ls2p8k****", "Code": 0, "Message": "stop instance success"}
  ]
}
```

#### 重启实例

```bash
volcengine-cli ecs RebootInstances --RegionId cn-beijing --InstanceIds '["i-2zeaf0ls2p8k****"]'
```

#### 删除实例

```bash
# 按量付费实例直接删除
volcengine-cli ecs TerminateInstances --RegionId cn-beijing --InstanceIds '["i-2zeaf0ls2p8k****"]'

# 包年包月实例需要设置退还方式
volcengine-cli ecs TerminateInstances --RegionId cn-beijing --InstanceIds '["i-2zeaf0ls2p8k****"]' --RenewType None --ReleaseInstanceInHour 1
```

#### 查询可用镜像

```bash
# 查询公共镜像
volcengine-cli ecs DescribeImages --RegionId cn-beijing --ImageType public --ImageName "CentOS 7.9"

# 筛选操作系统类型
volcengine-cli ecs DescribeImages --RegionId cn-beijing --OsType linux --Architecture x86_64
```

**输出示例**:
```json
{
  "Images": [
    {
      "ImageId": "img-2zeaf0ls2p7k9****",
      "ImageName": "CentOS 7.9 x86_64",
      "ImageType": "public",
      "OsType": "linux",
      "Architecture": "x86_64",
      "Size": 40,
      "SystemDisk": {"DiskType": "ESSD", "DiskSize": 40}
    }
  ]
}
```

### 2.2 云硬盘操作

#### 创建云硬盘

```bash
volcengine-cli ecs CreateDisk --RegionId cn-beijing \
  --DiskType ESSD \
  --DiskSize 100 \
  --DiskName data-disk-01 \
  --ZoneId cn-beijing-a
```

**输出示例**:
```json
{
  "DiskId": "vol-2zeaf0ls2p7k9****",
  "RequestId": "9d9f6f39-5f84-43c3-a02b-5g9d9a8c7d7e"
}
```

#### 挂载云硬盘

```bash
volcengine-cli ecs AttachDisk --RegionId cn-beijing \
  --InstanceId i-2zeaf0ls2p8k**** \
  --DiskId vol-2zeaf0ls2p7k9****
```

#### 卸载云硬盘

```bash
volcengine-cli ecs DetachDisk --RegionId cn-beijing \
  --InstanceId i-2zeaf0ls2p8k**** \
  --DiskId vol-2zeaf0ls2p7k9****
```

#### 查询云硬盘

```bash
volcengine-cli ecs DescribeDisks --RegionId cn-beijing --DiskIds '["vol-2zeaf0ls2p7k9****"]'
```

**输出示例**:
```json
{
  "Disks": [
    {
      "DiskId": "vol-2zeaf0ls2p7k9****",
      "DiskName": "data-disk-01",
      "DiskType": "ESSD",
      "DiskSize": 100,
      "Status": "Available",
      "ZoneId": "cn-beijing-a",
      "CreatedAt": "2026-02-20T10:00:00Z"
    }
  ]
}
```

#### 删除云硬盘

```bash
volcengine-cli ecs DeleteDisk --RegionId cn-beijing --DiskId vol-2zeaf0ls2p7k9****
```

### 2.3 容器实例 VCI

#### 查询容器实例

```bash
volcengine-cli vci DescribeContainerInstances --RegionId cn-beijing
```

**输出示例**:
```json
{
  "ContainerInstances": [
    {
      "ContainerId": "vci-2zeaf0ls2p7k9****",
      "ContainerName": "my-app-container",
      "Status": "Running",
      "ZoneId": "cn-beijing-a",
      "Cpu": 2,
      "Memory": 4096,
      "Image": "nginx:latest",
      "CreatedAt": "2026-03-10T14:20:00Z"
    }
  ],
  "TotalCount": 1
}
```

#### 创建容器

```bash
volcengine-cli vci CreateContainer --RegionId cn-beijing \
  --ContainerName my-app \
  --Image nginx:latest \
  --Cpu 2 \
  --Memory 4096 \
  --VSwitchId vsw-2ze8f3k6**** \
  --SecurityGroupId sg-2ze4j7g9****
```

**输出示例**:
```json
{
  "ContainerId": "vci-2zeaf0ls2p8k****",
  "RequestId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

#### 删除容器

```bash
volcengine-cli vci DeleteContainer --RegionId cn-beijing --ContainerId vci-2zeaf0ls2p8k****
```

### 2.4 函数服务

#### 列出函数

```bash
volc function ListFunctions --RegionId cn-beijing --FunctionType Timer
```

**输出示例**:
```json
{
  "Functions": [
    {
      "FunctionId": "func-2zeaf0ls2p7k9****",
      "FunctionName": "image-processor",
      "Runtime": "Python3.9",
      "Timeout": 60,
      "MemorySize": 128,
      "CreatedAt": "2026-01-20T09:00:00Z"
    }
  ],
  "TotalCount": 1
}
```

#### 创建函数

```bash
volc function CreateFunction --RegionId cn-beijing \
  --FunctionName my-handler-function \
  --Runtime Python3.9 \
  --Handler index.handler \
  --CodeZipFile /path/to/code.zip \
  --Timeout 60 \
  --MemorySize 256
```

**输出示例**:
```json
{
  "FunctionId": "func-2zeaf0ls2p8k****",
  "FunctionName": "my-handler-function",
  "CreatedAt": "2026-04-01T12:00:00Z",
  "RequestId": "b2c3d4e5-f6a7-8901-bcde-f23456789012"
}
```

#### 调用函数

```bash
# 同步调用
volc function InvokeFunction --RegionId cn-beijing \
  --FunctionName my-handler-function \
  --Payload '{"key": "value"}'

# 异步调用
volc function InvokeFunction --RegionId cn-beijing \
  --FunctionName my-handler-function \
  --InvocationType Async \
  --Payload '{"key": "value"}'
```

**输出示例** (同步调用):
```json
{
  "StatusCode": 200,
  "Payload": "{\"result\": \"success\", \"data\": {\"processed\": true}}",
  "LogResult": " RequestId: b2c3d4e5-f6a7-8901-bcde-f23456789012\n Duration: 45.32ms\n Billed Duration: 100ms"
}
```

#### 删除函数

```bash
volc function DeleteFunction --RegionId cn-beijing --FunctionId func-2zeaf0ls2p8k****
```

---

## 3. 存储服务

### 3.1 TOS 对象存储

> TOS: Volcano Engine Object Storage

#### 基础命令 (通过 tosutil 工具)

```bash
# 安装 tosutil
curl -fsSL https://veutunnel.com/tools/tos/install-tosutil.sh | bash
```

##### 列出桶

```bash
tosutil ls tos://your-bucket-name/
```

**输出示例**:
```
DateTime            Size      Object
2026-05-01 10:00:00  1.2MB     docs/readme.pdf
2026-05-02 14:30:00  500KB     images/logo.png
2026-05-03 09:15:00  3.4MB     videos/intro.mp4
```

##### 创建桶

```bash
tosutil mb tos://my-project-bucket-2026/
```

**输出示例**:
```
Creating bucket: tos://my-project-bucket-2026/
Bucket created successfully.
```

##### 上传文件

```bash
tosutil cp /local/path/to/file.tar.gz tos://my-project-bucket-2026/backups/
```

**输出示例**:
```
[2026-05-14 10:30:00]
  File: /local/path/to/file.tar.gz
  Size: 1.25GB
  Start: upload
  End: success
  Speed: 15.3MB/s
```

##### 下载文件

```bash
tosutil cp tos://my-project-bucket-2026/backups/file.tar.gz /local/downloads/
```

##### 同步目录

```bash
tosutil sync /local/data/ tos://my-project-bucket-2026/data/ --force
```

**输出示例**:
```
[2026-05-14 10:35:00]
  Sync Mode: force
  Total Files: 128
  Success: 128
  Failed: 0
  Duration: 45.23s
```

##### 删除对象

```bash
tosutil rm tos://my-project-bucket-2026/backups/old-file.tar.gz
```

##### 递归删除

```bash
tosutil rm -r tos://my-project-bucket-2026/temp/
```

#### 权限管理

##### 设置 ACL

```bash
tosutil set-acl tos://my-project-bucket-2026/ --acl private
tosutil set-acl tos://my-project-bucket-2026/readme.pdf --acl public-read
```

##### 查看 ACL

```bash
tosutil get-acl tos://my-project-bucket-2026/readme.pdf
```

**输出示例**:
```
Owner: AKLT****************************
Grantee: (id: *)
Permission: READ
```

#### 跨域资源共享 (CORS)

##### 配置 CORS

```bash
tosutil cors tos://my-project-bucket-2026/ --cors-rules '[
  {
    "AllowedOrigins": ["https://example.com"],
    "AllowedMethods": ["GET", "PUT", "POST"],
    "AllowedHeaders": ["*"],
    "MaxAgeSeconds": 3600
  }
]'
```

##### 查看 CORS 配置

```bash
tosutil cors tos://my-project-bucket-2026/ --get
```

#### 生命周期管理

##### 配置生命周期规则

```bash
tosutil lifecycle tos://my-project-bucket-2026/ --rules '[
  {
    "ID": "log-expiration",
    "Prefix": "logs/",
    "Expiration": {"Days": 30},
    "Status": "Enabled"
  },
  {
    "ID": "archive-transition",
    "Prefix": "archives/",
    "Transitions": [{"Days": 90, "StorageClass": "Archive"}],
    "Status": "Enabled"
  }
]'
```

##### 查看生命周期规则

```bash
tosutil lifecycle tos://my-project-bucket-2026/ --get
```

### 3.2 云硬盘

> 同 2.2 节 ECS 云硬盘操作，使用 `ecs` 服务命令

---

## 4. 数据库服务

### 4.1 MySQL/PostgreSQL (ByteDance 数据库)

#### 查询数据库

```bash
volcengine-cli rds DescribeDatabases --RegionId cn-beijing --DBInstanceId dbinst-2zeaf0ls2p7k9****
```

**输出示例**:
```json
{
  "Databases": [
    {
      "DBName": "app_production",
      "CharacterSetName": "utf8mb4",
      "DBDescription": "Production application database",
      "Status": "Running",
      "CreatedAt": "2026-01-10T08:00:00Z"
    },
    {
      "DBName": "app_staging",
      "CharacterSetName": "utf8mb4",
      "DBDescription": "Staging environment database",
      "Status": "Running",
      "CreatedAt": "2026-02-15T10:30:00Z"
    }
  ]
}
```

#### 创建数据库

```bash
volcengine-cli rds CreateDatabase --RegionId cn-beijing \
  --DBInstanceId dbinst-2zeaf0ls2p7k9**** \
  --DBName app_new_database \
  --CharacterSetName utf8mb4 \
  --DBDescription "New project database"
```

**输出示例**:
```json
{
  "DBName": "app_new_database",
  "RequestId": "c3d4e5f6-a7b8-9012-cdef-345678901234",
  "TaskId": "task-2zeaf0ls2p8k****"
}
```

#### 创建账户

```bash
volcengine-cli rds CreateAccount --RegionId cn-beijing \
  --DBInstanceId dbinst-2zeaf0ls2p7k9**** \
  --AccountName app_admin \
  --Password "Str0ngPass!23" \
  --AccountType Normal
```

**输出示例**:
```json
{
  "AccountName": "app_admin",
  "RequestId": "d4e5f6a7-b8c9-0123-defa-456789012345"
}
```

#### 授予账户权限

```bash
volcengine-cli rds GrantAccountPrivilege --RegionId cn-beijing \
  --DBInstanceId dbinst-2zeaf0ls2p7k9**** \
  --AccountName app_admin \
  --DBName app_new_database \
  --PrivilegeType DynamicAccount
```

**输出示例**:
```json
{
  "RequestId": "e5f6a7b8-c9d0-1234-efab-567890123456"
}
```

#### 查询实例列表

```bash
volcengine-cli rds DescribeDBInstances --RegionId cn-beijing --DBInstanceType MySQL
```

**输出示例**:
```json
{
  "DBInstances": [
    {
      "DBInstanceId": "dbinst-2zeaf0ls2p7k9****",
      "DBInstanceName": "production-mysql",
      "DBInstanceType": "MySQL",
      "DBInstanceVersion": "8.0",
      "DBEngine": "MySQL",
      "Status": "Running",
      "ZoneId": "cn-beijing-a",
      "VpcId": "vpc-2ze4j7g9****",
      "VSwitchId": "vsw-2ze8f3k6****",
      "SpecCode": "rds.mysql.slave.s1.large",
      "StorageSize": 200,
      "PrimaryInstanceId": "",
      "CreatedAt": "2026-01-05T12:00:00Z"
    }
  ],
  "TotalCount": 1
}
```

#### 重启实例

```bash
volcengine-cli rds RebootDBInstance --RegionId cn-beijing --DBInstanceId dbinst-2zeaf0ls2p7k9****
```

### 4.2 Redis 数据库

#### 查询 Redis 实例

```bash
volcengine-cli redis DescribeInstances --RegionId cn-beijing
```

**输出示例**:
```json
{
  "Instances": [
    {
      "InstanceId": "redis-2zeaf0ls2p7k9****",
      "InstanceName": "cache-prod",
      "RegionId": "cn-beijing",
      "ZoneId": "cn-beijing-a",
      "Status": "Running",
      "EngineVersion": "6.0",
      "SpecCode": "redis.sh.standard.a1.2g",
      "StorageSize": 2048,
      "VpcId": "vpc-2ze4j7g9****",
      "Port": 6379,
      "CreatedAt": "2026-02-01T09:00:00Z"
    }
  ],
  "TotalCount": 1
}
```

#### 创建 Redis 实例

```bash
volcengine-cli redis CreateInstance --RegionId cn-beijing \
  --InstanceName cache-dev \
  --ZoneIds '["cn-beijing-a"]' \
  --SpecCode redis.sh.standard.a1.2g \
  --StorageSize 2048 \
  --VpcId vpc-2ze4j7g9**** \
  --VSwitchId vsw-2ze8f3k6**** \
  --Password "Str0ngRedis!45"
```

**输出示例**:
```json
{
  "InstanceId": "redis-2zeaf0ls2p8k****",
  "OrderId": "order-2zeaf0ls2p8k****",
  "RequestId": "f6a7b8c9-d0e1-2345-fabc-678901234567"
}
```

#### 创建账户

```bash
volcengine-cli redis CreateAccount --RegionId cn-beijing \
  --InstanceId redis-2zeaf0ls2p8k**** \
  --AccountName app_cache_user \
  --Password "Str0ngPass!67"
```

#### 连接实例

```bash
# 查看连接信息
volcengine-cli redis DescribeInstanceAttribute --RegionId cn-beijing --InstanceId redis-2zeaf0ls2p7k9****

# 通过内网连接
redis-cli -h redis-2zeaf0ls2p7k9****.redis.cn-beijing.ivolces.com -p 6379 -a Str0ngPass!45
```

### 4.3 MongoDB 数据库

#### 查询 MongoDB 实例

```bash
volcengine-cli mongo DescribeInstances --RegionId cn-beijing
```

**输出示例**:
```json
{
  "Instances": [
    {
      "InstanceId": "mongo-2zeaf0ls2p7k9****",
      "InstanceName": "mongodb-prod",
      "Status": "Running",
      "EngineVersion": "5.0",
      "SpecCode": "mongo.sh.standard.e2.4g",
      "StorageSize": 50,
      "ReplicaSets": [
        {"ReplicaSetName": "mgset-2zeaf0ls2p7k9****", "Role": "Primary"}
      ],
      "VpcId": "vpc-2ze4j7g9****",
      "Port": 27017,
      "CreatedAt": "2026-01-25T11:00:00Z"
    }
  ],
  "TotalCount": 1
}
```

#### 创建 MongoDB 实例

```bash
volcengine-cli mongo CreateInstance --RegionId cn-beijing \
  --InstanceName mongodb-dev \
  --ZoneIds '["cn-beijing-a"]' \
  --SpecCode mongo.sh.standard.e2.4g \
  --StorageSize 50 \
  --VpcId vpc-2ze4j7g9**** \
  --VSwitchId vsw-2ze8f3k6**** \
  --Password "Str0ngMongo!89"
```

**输出示例**:
```json
{
  "InstanceId": "mongo-2zeaf0ls2p8k****",
  "OrderId": "order-2zeaf0ls2p8k****",
  "RequestId": "a7b8c9d0-e1f2-3456-abcd-789012345678"
}
```

#### 创建账户

```bash
volcengine-cli mongo CreateAccount --RegionId cn-beijing \
  --InstanceId mongo-2zeaf0ls2p8k**** \
  --AccountName app_mongo_user \
  --Password "Str0ngPass!91"
```

#### 连接实例

```bash
# 通过 mongo shell 连接
mongo "mongodb://app_mongo_user:Str0ngPass!91@mongo-2zeaf0ls2p8k****.mongo.cn-beijing.ivolces.com:27017/app_database?authSource=admin"
```

---

## 5. 网络服务

### 5.1 VPC 私有网络

#### 查询 VPC

```bash
volcengine-cli vpc DescribeVpcs --RegionId cn-beijing
```

**输出示例**:
```json
{
  "Vpcs": [
    {
      "VpcId": "vpc-2zeaf0ls2p7k9****",
      "VpcName": "production-vpc",
      "CidrBlock": "192.168.0.0/16",
      "Status": "Available",
      "Description": "Production environment VPC",
      "CreatedAt": "2026-01-01T00:00:00Z",
      "Tags": [
        {"Key": "Environment", "Value": "Production"}
      ]
    }
  ],
  "TotalCount": 1
}
```

#### 创建 VPC

```bash
volcengine-cli vpc CreateVpc --RegionId cn-beijing \
  --VpcName production-vpc-new \
  --CidrBlock 10.0.0.0/8 \
  --Description "New production VPC"
```

**输出示例**:
```json
{
  "VpcId": "vpc-2zeaf0ls2p8k****",
  "RequestId": "b8c9d0e1-f2a3-4567-bcde-890123456789"
}
```

#### 查询虚拟交换机

```bash
volcengine-cli vpc DescribeVSwitches --RegionId cn-beijing --VpcId vpc-2zeaf0ls2p7k9****
```

**输出示例**:
```json
{
  "VSwitches": [
    {
      "VSwitchId": "vsw-2ze8f3k6****",
      "VSwitchName": "web-subnet",
      "VpcId": "vpc-2zeaf0ls2p7k9****",
      "CidrBlock": "192.168.1.0/24",
      "ZoneId": "cn-beijing-a",
      "Status": "Available"
    },
    {
      "VSwitchId": "vsw-2ze8f3k7****",
      "VSwitchName": "db-subnet",
      "VpcId": "vpc-2zeaf0ls2p7k9****",
      "CidrBlock": "192.168.2.0/24",
      "ZoneId": "cn-beijing-a",
      "Status": "Available"
    }
  ]
}
```

#### 创建虚拟交换机

```bash
volcengine-cli vpc CreateVSwitch --RegionId cn-beijing \
  --VpcId vpc-2zeaf0ls2p7k9**** \
  --VSwitchName app-subnet \
  --CidrBlock 192.168.3.0/24 \
  --ZoneId cn-beijing-a
```

**输出示例**:
```json
{
  "VSwitchId": "vsw-2ze8f3k8****",
  "RequestId": "c9d0e1f2-a3b4-5678-cdef-901234567890"
}
```

#### 查询路由表

```bash
volcengine-cli vpc DescribeRouteTables --RegionId cn-beijing --VpcId vpc-2zeaf0ls2p7k9****
```

**输出示例**:
```json
{
  "RouteTables": [
    {
      "RouteTableId": "rtb-2zeaf0ls2p7k9****",
      "RouteTableName": "default-route-table",
      "VpcId": "vpc-2zeaf0ls2p7k9****",
      "Type": "System",
      "Routes": [
        {
          "DestinationCidrBlock": "192.168.0.0/16",
          "NexthopType": "Local",
          "NexthopId": ""
        }
      ]
    }
  ]
}
```

#### 创建路由表

```bash
volcengine-cli vpc CreateRouteTable --RegionId cn-beijing \
  --VpcId vpc-2zeaf0ls2p7k9**** \
  --RouteTableName custom-route-table
```

**输出示例**:
```json
{
  "RouteTableId": "rtb-2zeaf0ls2p8k****",
  "RequestId": "d0e1f2a3-b4c5-6789-defa-012345678901"
}
```

#### 添加路由条目

```bash
volcengine-cli vpc AssociateRouteTable --RegionId cn-beijing \
  --VSwitchId vsw-2ze8f3k8**** \
  --RouteTableId rtb-2zeaf0ls2p8k****
```

#### 创建 NAT 网关

```bash
volcengine-cli vpc CreateNatGateway --RegionId cn-beijing \
  --NatGatewayName prod-nat \
  --VpcId vpc-2zeaf0ls2p7k9**** \
  --SubnetId vsw-2ze8f3k6**** \
  --SpecCode Small
```

**输出示例**:
```json
{
  "NatGatewayId": "nat-2zeaf0ls2p7k9****",
  "RequestId": "e1f2a3b4-c5d6-7890-efab-123456789012"
}
```

### 5.2 CLB 负载均衡

#### 查询负载均衡器

```bash
volcengine-cli clb DescribeLoadBalancers --RegionId cn-beijing
```

**输出示例**:
```json
{
  "LoadBalancers": [
    {
      "LoadBalancerId": "lb-2zeaf0ls2p7k9****",
      "LoadBalancerName": "web-lb",
      "LoadBalancerType": "public",
      "Status": "active",
      "VpcId": "vpc-2zeaf0ls2p7k9****",
      "Address": "120.92.168.***",
      "CreatedAt": "2026-02-01T10:00:00Z"
    }
  ],
  "TotalCount": 1
}
```

#### 创建负载均衡器

```bash
# 公网负载均衡器
volcengine-cli clb CreateLoadBalancer --RegionId cn-beijing \
  --LoadBalancerName web-lb-new \
  --VpcId vpc-2zeaf0ls2p7k9**** \
  --SubnetId vsw-2ze8f3k6**** \
  --LoadBalancerType public \
  --BandwidthPackegeId ""

# 私网负载均衡器
volcengine-cli clb CreateLoadBalancer --RegionId cn-beijing \
  --LoadBalancerName internal-lb \
  --VpcId vpc-2zeaf0ls2p7k9**** \
  --SubnetId vsw-2ze8f3k6**** \
  --LoadBalancerType internal
```

**输出示例**:
```json
{
  "LoadBalancerId": "lb-2zeaf0ls2p8k****",
  "RequestId": "f2a3b4c5-d6e7-8901-fabc-234567890123"
}
```

#### 注册目标

```bash
volcengine-cli clb RegisterTargets --RegionId cn-beijing \
  --ServerGroupId sg-2zeaf0ls2p7k9**** \
  --Targets '[{"InstanceId": "i-2zeaf0ls2p8k****", "Port": 80}]'
```

**输出示例**:
```json
{
  "RequestId": "a3b4c5d6-e7f8-9012-abcd-345678901234"
}
```

#### 创建监听器

```bash
# 创建 HTTP 监听器
volcengine-cli clb CreateListener --RegionId cn-beijing \
  --LoadBalancerId lb-2zeaf0ls2p7k9**** \
  --ListenerName http-listener \
  --Protocol HTTP \
  --Port 80 \
  --ServerGroupId sg-2zeaf0ls2p7k9****

# 创建 HTTPS 监听器
volcengine-cli clb CreateListener --RegionId cn-beijing \
  --LoadBalancerId lb-2zeaf0ls2p7k9**** \
  --ListenerName https-listener \
  --Protocol HTTPS \
  --Port 443 \
  --ServerGroupId sg-2zeaf0ls2p7k9**** \
  --CertificateId cert-2zeaf0ls2p7k9****
```

**输出示例**:
```json
{
  "ListenerId": "lsn-2zeaf0ls2p7k9****",
  "RequestId": "b4c5d6e7-f8a9-0123-bcde-456789012345"
}
```

### 5.3 弹性 IP

#### 查询弹性 IP

```bash
volcengine-cli eip DescribeEips --RegionId cn-beijing
```

**输出示例**:
```json
{
  "Eips": [
    {
      "EipId": "eip-2zeaf0ls2p7k9****",
      "EipAddress": "120.92.168.***",
      "Bandwidth": 200,
      "Status": "Available",
      "InstanceType": "",
      "BilingType": "PostPaid",
      "CreatedAt": "2026-03-01T08:00:00Z"
    }
  ],
  "TotalCount": 1
}
```

#### 申请弹性 IP

```bash
volcengine-cli eip AllocateEipAddress --RegionId cn-beijing \
  --Bandwidth 100 \
  --BilingType PostPaid \
  --ISP ChinaTelecom
```

**输出示例**:
```json
{
  "EipId": "eip-2zeaf0ls2p8k****",
  "EipAddress": "120.92.169.***",
  "OrderId": "order-2zeaf0ls2p8k****",
  "RequestId": "c5d6e7f8-a9b0-1234-cdef-567890123456"
}
```

#### 绑定弹性 IP

```bash
volcengine-cli eip AssociateEipAddress --RegionId cn-beijing \
  --EipId eip-2zeaf0ls2p8k**** \
  --InstanceId i-2zeaf0ls2p8k**** \
  --InstanceType EcsInstance
```

**输出示例**:
```json
{
  "RequestId": "d6e7f8a9-b0c1-2345-defa-678901234567"
}
```

#### 解绑弹性 IP

```bash
volcengine-cli eip DisassociateEipAddress --RegionId cn-beijing \
  --EipId eip-2zeaf0ls2p8k****
```

#### 释放弹性 IP

```bash
volcengine-cli eip ReleaseEipAddress --RegionId cn-beijing --EipId eip-2zeaf0ls2p8k****
```

---

## 6. 安全服务

### 6.1 密钥管理 KMS

#### 查询密钥列表

```bash
volcengine-cli kms ListKeys --RegionId cn-beijing --KeyType AliyunManaged
```

**输出示例**:
```json
{
  "Keys": [
    {
      "KeyId": "kms-2zeaf0ls2p7k9****",
      "KeyArn": "acs:kms:cn-beijing:123456789012:key/kms-2zeaf0ls2p7k9****",
      "KeyState": "Enabled",
      "KeySpec": "AliyunManaged",
      "CreateTime": "2026-01-15T10:00:00Z"
    }
  ],
  "TotalCount": 1
}
```

#### 创建密钥

```bash
volcengine-cli kms CreateKey --RegionId cn-beijing \
  --KeyUsage ENCRYPT_DECRYPT \
  --KeyDescription "Production encryption key" \
  --ProtectionLevel Software
```

**输出示例**:
```json
{
  "KeyId": "kms-2zeaf0ls2p8k****",
  "KeyArn": "acs:kms:cn-beijing:123456789012:key/kms-2zeaf0ls2p8k****",
  "KeyState": "Enabled",
  "CreateTime": "2026-05-10T14:30:00Z"
}
```

#### 加密数据

```bash
# 加密小数据 (直接加密)
volcengine-cli kms Encrypt --RegionId cn-beijing \
  --KeyId kms-2zeaf0ls2p8k**** \
  --Plaintext "SGVsbG8gV29ybGQ=" \
  --PlaintextType Plain
```

**输出示例**:
```json
{
  "KeyId": "kms-2zeaf0ls2p8k****",
  "CiphertextBlob": "VAiICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg",
  "RequestId": "e7f8a9b0-c1d2-3456-efab-789012345678"
}
```

#### 解密数据

```bash
volcengine-cli kms Decrypt --RegionId cn-beijing \
  --KeyId kms-2zeaf0ls2p8k**** \
  --CiphertextBlob "VAiICAgICAgICAgICAg..."
```

**输出示例**:
```json
{
  "KeyId": "kms-2zeaf0ls2p8k****",
  "Plaintext": "SGVsbG8gV29ybGQ=",
  "RequestId": "f8a9b0c1-d2e3-4567-fabc-890123456789"
}
```

### 6.2 安全组

#### 查询安全组

```bash
volcengine-cli ecs DescribeSecurityGroups --RegionId cn-beijing --VpcId vpc-2zeaf0ls2p7k9****
```

**输出示例**:
```json
{
  "SecurityGroups": [
    {
      "SecurityGroupId": "sg-2ze4j7g9****",
      "SecurityGroupName": "web-sg",
      "VpcId": "vpc-2zeaf0ls2p7k9****",
      "Description": "Security group for web servers",
      "SecurityGroupType": "security_group",
      "CreatedAt": "2026-01-10T09:00:00Z"
    }
  ]
}
```

#### 创建安全组

```bash
volcengine-cli ecs CreateSecurityGroup --RegionId cn-beijing \
  --SecurityGroupName my-security-group \
  --VpcId vpc-2zeaf0ls2p7k9**** \
  --Description "My security group"
```

**输出示例**:
```json
{
  "SecurityGroupId": "sg-2ze4j7g0****",
  "RequestId": "a9b0c1d2-e3f4-5678-abcd-901234567890"
}
```

#### 安全组入方向规则授权

```bash
# 允许 HTTP 访问
volcengine-cli ecs AuthorizeSecurityGroup --RegionId cn-beijing \
  --SecurityGroupId sg-2ze4j7g9**** \
  --IpProtocol tcp \
  --PortStart 80 \
  --PortEnd 80 \
  --SourceCidrBlock 0.0.0.0/0 \
  --Policy accept

# 允许 HTTPS 访问
volcengine-cli ecs AuthorizeSecurityGroup --RegionId cn-beijing \
  --SecurityGroupId sg-2ze4j7g9**** \
  --IpProtocol tcp \
  --PortStart 443 \
  --PortEnd 443 \
  --SourceCidrBlock 0.0.0.0/0 \
  --Policy accept

# 允许 MySQL 3306 端口 (仅内网)
volcengine-cli ecs AuthorizeSecurityGroup --RegionId cn-beijing \
  --SecurityGroupId sg-2ze4j7g9**** \
  --IpProtocol tcp \
  --PortStart 3306 \
  --PortEnd 3306 \
  --SourceCidrBlock 192.168.0.0/16 \
  --Policy accept
```

**输出示例**:
```json
{
  "RequestId": "b0c1d2e3-f4a5-6789-bcde-012345678901"
}
```

#### 安全组出方向规则授权

```bash
# 允许所有出站
volcengine-cli ecs AuthorizeSecurityGroup --RegionId cn-beijing \
  --SecurityGroupId sg-2ze4j7g9**** \
  --IpProtocol tcp \
  --PortStart -1 \
  --PortEnd -1 \
  --DestCidrBlock 0.0.0.0/0 \
  --Policy accept \
  --Direction egress
```

#### 撤销安全组规则

```bash
volcengine-cli ecs RevokeSecurityGroup --RegionId cn-beijing \
  --SecurityGroupId sg-2ze4j7g9**** \
  --IpProtocol tcp \
  --PortStart 80 \
  --PortEnd 80 \
  --SourceCidrBlock 0.0.0.0/0
```

---

## 7. 监控与日志

### 7.1 云监控

#### 查询指标列表

```bash
volcengine-cli cms ListMetrics --RegionId cn-beijing --Namespace acs_ecs_dashboard
```

**输出示例**:
```json
{
  "Metrics": [
    {
      "Namespace": "acs_ecs_dashboard",
      "MetricName": "cpu_total",
      "Dimensions": [
        {"Name": "instanceId", "Value": "i-2zeaf0ls2p8k****"}
      ],
      "Statistics": ["Average", "Minimum", "Maximum"]
    },
    {
      "Namespace": "acs_ecs_dashboard",
      "MetricName": "memory_used",
      "Dimensions": [
        {"Name": "instanceId", "Value": "i-2zeaf0ls2p8k****"}
      ],
      "Statistics": ["Average", "Minimum", "Maximum"]
    },
    {
      "Namespace": "acs_ecs_dashboard",
      "MetricName": "disk_read_bytes",
      "Dimensions": [
        {"Name": "instanceId", "Value": "i-2zeaf0ls2p8k****"}
      ],
      "Statistics": ["Average", "Minimum", "Maximum"]
    }
  ],
  "TotalCount": 3
}
```

#### 查询监控数据

```bash
volcengine-cli cms GetMetricData --RegionId cn-beijing \
  --MetricData.1.Namespace acs_ecs_dashboard \
  --MetricData.1.MetricName cpu_total \
  --MetricData.1.Period 60 \
  --MetricData.1.StartTime 1747200000 \
  --MetricData.1.EndTime 1747203600 \
  --MetricData.1.Dimensions '[{"instanceId": "i-2zeaf0ls2p8k****"}]'
```

**输出示例**:
```json
{
  "Datapoints": [
    {
      "Timestamp": 1747200000,
      "Average": 45.2,
      "Minimum": 30.1,
      "Maximum": 78.5
    },
    {
      "Timestamp": 1747200060,
      "Average": 52.3,
      "Minimum": 35.6,
      "Maximum": 82.1
    }
  ],
  "RequestId": "c1d2e3f4-a5b6-7890-cdef-123456789012"
}
```

#### 创建报警规则

```bash
volcengine-cli cms CreateAlarm --RegionId cn-beijing \
  --AlarmName cpu-high-alarm \
  --MetricNamespace acs_ecs_dashboard \
  --MetricName cpu_total \
  --AlarmStatistics Average \
  --AlarmPeriod 300 \
  --AlarmThreshold 80 \
  --ComparisonOperator ">=" \
  --AlarmActions '[{"Type": "Callback", "Url": "https://your-webhook.com/alarm"}]' \
  --Dimensions '[{"instanceId": "i-2zeaf0ls2p8k****"}]'
```

**输出示例**:
```json
{
  "AlarmId": "alarm-2zeaf0ls2p8k****",
  "RequestId": "d2e3f4a5-b6c7-8901-defa-234567890123"
}
```

#### 查询报警规则

```bash
volcengine-cli cms DescribeAlarms --RegionId cn-beijing --AlarmName cpu-high-alarm
```

### 7.2 日志服务

#### 查询日志项目

```bash
volcengine-cli log DescribeProjects --RegionId cn-beijing
```

**输出示例**:
```json
{
  "Projects": [
    {
      "ProjectName": "app-production-logs",
      "ProjectId": "e70f8a9b-1234-5678-abcd-ef1234567890",
      "RegionId": "cn-beijing",
      "Description": "Production application logs",
      "CreatedAt": "2026-01-20T10:00:00Z"
    }
  ],
  "TotalCount": 1
}
```

#### 创建日志项目

```bash
volcengine-cli log CreateProject --RegionId cn-beijing \
  --ProjectName app-staging-logs \
  --RegionId cn-beijing \
  --Description "Staging environment logs"
```

**输出示例**:
```json
{
  "ProjectName": "app-staging-logs",
  "RequestId": "e3f4a5b6-c7d8-8901-efab-345678901234"
}
```

#### 创建日志库

```bash
volcengine-cli log CreateLogstore --RegionId cn-beijing \
  --ProjectName app-production-logs \
  --LogStoreName nginx-logs \
  --TTLInDays 30 \
  --ShardCount 2
```

**输出示例**:
```json
{
  "LogStoreName": "nginx-logs",
  "Shards": [
    {"ShardId": 0, "Status": "readwrite"},
    {"ShardId": 1, "Status": "readwrite"}
  ],
  "RequestId": "f4a5b6c7-d8e9-9012-fabc-456789012345"
}
```

#### 写入日志

```bash
volcengine-cli log PushLog --RegionId cn-beijing \
  --ProjectName app-production-logs \
  --LogStoreName nginx-logs \
  --Topic "access-log" \
  --LogStreams '["logstream-001"]' \
  --Logs '[{"timestamp": 1747203600, "content": {"ip": "192.168.1.100", "status": 200, "path": "/api/users"}}]'
```

**输出示例**:
```json
{
  "RequestId": "a5b6c7d8-e9f0-1234-abcd-567890123456",
  "RejectedLogGroups": 0
}
```

#### 查询日志

```bash
volcengine-cli log QueryLogs --RegionId cn-beijing \
  --ProjectName app-production-logs \
  --LogStoreName nginx-logs \
  --Query "status >= 400" \
  --From 1747196400 \
  --To 1747203600 \
  --Limit 100
```

**输出示例**:
```json
{
  "Logs": [
    {
      "Time": "2026-05-14 10:00:00",
      "Contents": [
        {"Key": "ip", "Value": "203.0.113.42"},
        {"Key": "status", "Value": "404"},
        {"Key": "path", "Value": "/api/missing"}
      ]
    },
    {
      "Time": "2026-05-14 10:05:00",
      "Contents": [
        {"Key": "ip", "Value": "198.51.100.15"},
        {"Key": "status", "Value": "500"},
        {"Key": "path", "Value": "/api/error"}
      ]
    }
  ],
  "TotalCount": 2,
  "RequestId": "b6c7d8e9-f0a1-2345-bcde-678901234567"
}
```

## 8. 中间件服务 (Middleware)

### Kafka消息队列
```bash
# 查询Kafka实例
 volc kafka ListInstance --Region cn-east-1

# 创建Kafka实例
 volc kafka CreateInstance --Region cn-east-1 \
  --InstanceName my-kafka \
  --ZoneId cn-east-1a \
  --EngineVersion 2.7.0 \
  --Partitions 6

# 查询Topic列表
 volc kafka ListTopic --Region cn-east-1 --InstanceId kafka-xxxxxxxx

# 创建Topic
 volc kafka CreateTopic --Region cn-east-1 \
  --InstanceId kafka-xxxxxxxx \
  --Topic my-topic \
  --PartitionCount 6 \
  --ReplicationFactor 3

# 创建Consumer Group
 volc kafka CreateConsumerGroup --Region cn-east-1 \
  --InstanceId kafka-xxxxxxxx \
  --GroupId my-group
```

### RocketMQ消息队列
```bash
# 查询RocketMQ实例
 volc rocketmq ListInstance --Region cn-east-1

# 创建RocketMQ实例
 volc rocketmq CreateInstance --Region cn-east-1 \
  --InstanceName my-rmq \
  --ZoneId cn-east-1a

# 创建Topic
 volc rocketmq ListTopic --Region cn-east-1 --InstanceId rmq-xxxxxxxx

# 创建Consumer Group
 volc rocketmq CreateSubscription --Region cn-east-1 \
  --InstanceId rmq-xxxxxxxx \
  --GroupId my-consumer-group
```

---

## 9. 容器服务

### 9.1 容器引擎 VKE

#### 查询集群列表

```bash
volcengine-cli vke ListClusters --RegionId cn-beijing
```

**输出示例**:
```json
{
  "Clusters": [
    {
      "ClusterId": "cc-2zeaf0ls2p7k9****",
      "Name": "production-cluster",
      "KubernetesVersion": "1.28.4",
      "Status": "Running",
      "RegionId": "cn-beijing",
      "ZoneId": "cn-beijing-a",
      "VpcId": "vpc-2zeaf0ls2p7k9****",
      "VSwitchIds": ["vsw-2ze8f3k6****"],
      "CreatedAt": "2026-01-15T08:00:00Z",
      "Tags": [
        {"Key": "Environment", "Value": "Production"}
      ]
    }
  ],
  "TotalCount": 1
}
```

#### 创建集群

```bash
volcengine-cli vke CreateCluster --RegionId cn-beijing \
  --Name production-cluster-new \
  --KubernetesVersion 1.28.4 \
  --VpcId vpc-2zeaf0ls2p7k9**** \
  --VSwitchIds '["vsw-2ze8f3k6****", "vsw-2ze8f3k7****"]' \
  --ContainerNetworkCidr 172.20.0.0/16 \
  --ServiceCidr 172.21.0.0/16 \
  --Password "Str0ngK8s!23" \
  --NodePoolType ManagedNodes
```

**输出示例**:
```json
{
  "ClusterId": "cc-2zeaf0ls2p8k****",
  "RequestId": "c7d8e9f0-a1b2-3456-cdef-789012345678",
  "TaskId": "task-2zeaf0ls2p8k****"
}
```

#### 查询集群详情

```bash
volcengine-cli vke DescribeCluster --RegionId cn-beijing --ClusterId cc-2zeaf0ls2p8k****
```

**输出示例**:
```json
{
  "ClusterId": "cc-2zeaf0ls2p8k****",
  "Name": "production-cluster-new",
  "KubernetesVersion": "1.28.4",
  "Status": "Running",
  "RegionId": "cn-beijing",
  "VpcId": "vpc-2zeaf0ls2p7k9****",
  "ContainerNetworkCidr": "172.20.0.0/16",
  "ServiceCidr": "172.21.0.0/16",
  "Endpoints": {
    "Private": "https://172.20.100.10:6443",
    "Public": "https://cc-2zeaf0ls2p8k****.k8s.cn-beijing.ivolces.com:6443"
  },
  "CreatedAt": "2026-05-01T12:00:00Z"
}
```

#### 删除集群

```bash
volcengine-cli vke DeleteCluster --RegionId cn-beijing --ClusterId cc-2zeaf0ls2p8k****
```

**输出示例**:
```json
{
  "RequestId": "d8e9f0a1-b2c3-4567-defa-890123456789"
}
```

#### 集群认证

```bash
# 获取集群 kubeconfig
volcengine-cli vke DescribeClusterKubeconfig --RegionId cn-beijing --ClusterId cc-2zeaf0ls2p8k****

# 保存 kubeconfig
volcengine-cli vke DescribeClusterKubeconfig --RegionId cn-beijing --ClusterId cc-2zeaf0ls2p8k**** --FilePath /Users/username/.kube/config
```

### 9.2 镜像仓库

#### 查询仓库列表

```bash
volcengine-cli vke ListRepositories --RegionId cn-beijing
```

**输出示例**:
```json
{
  "Repositories": [
    {
      "RepositoryId": "repo-2zeaf0ls2p7k9****",
      "RepositoryName": "nginx",
      "Registry": "registry.cn-beijing.ivolces.com",
      "Description": "Nginx base images",
      "CreatedAt": "2026-02-01T10:00:00Z"
    },
    {
      "RepositoryId": "repo-2zeaf0ls2p7k0****",
      "RepositoryName": "app-backend",
      "Registry": "registry.cn-beijing.ivolces.com",
      "Description": "Backend application images",
      "CreatedAt": "2026-02-15T14:30:00Z"
    }
  ],
  "TotalCount": 2
}
```

#### 创建仓库

```bash
volcengine-cli vke CreateRepository --RegionId cn-beijing \
  --RepositoryName my-app \
  --RepositoryType Private \
  --Description "My application repository"
```

**输出示例**:
```json
{
  "RepositoryId": "repo-2zeaf0ls2p8k****",
  "RepositoryName": "my-app",
  "Registry": "registry.cn-beijing.ivolces.com/my-app",
  "RequestId": "e9f0a1b2-c3d4-5678-efab-901234567890"
}
```

#### 推送镜像

```bash
# 登录镜像仓库
docker login registry.cn-beijing.ivolces.com -u your-username

# 打标签
docker tag my-app:latest registry.cn-beijing.ivolces.com/my-app:v1.0.0

# 推送
docker push registry.cn-beijing.ivolces.com/my-app:v1.0.0
```

**输出示例**:
```
The push refers to repository [registry.cn-beijing.ivolces.com/my-app]
v1.0.0: digest: sha256:a1b2c3d4e5f6...
Size: 1572.5kB
```

#### 拉取镜像

```bash
docker pull registry.cn-beijing.ivolces.com/my-app:v1.0.0
```

---

## 10. 资源管理与权限

### 10.1 IAM 访问控制

#### 查询用户

```bash
volcengine-cli iam ListUsers --RegionId cn-beijing
```

**输出示例**:
```json
{
  "Users": [
    {
      "UserId": "100000000001",
      "UserName": "admin",
      "DisplayName": "Administrator",
      "Email": "admin@example.com",
      "UserType": "IRMUser",
      "Status": "Active",
      "CreatedAt": "2025-01-01T00:00:00Z"
    },
    {
      "UserId": "100000000002",
      "UserName": "developer",
      "DisplayName": "Developer Account",
      "Email": "dev@example.com",
      "UserType": "IRMUser",
      "Status": "Active",
      "CreatedAt": "2026-01-10T09:00:00Z"
    }
  ],
  "TotalCount": 2
}
```

#### 创建用户

```bash
volcengine-cli iam CreateUser --RegionId cn-beijing \
  --UserName app-service-account \
  --DisplayName "Application Service Account" \
  --Email "app-service@example.com" \
  --Password "Str0ngPass!99"
```

**输出示例**:
```json
{
  "UserId": "100000000003",
  "UserName": "app-service-account",
  "RequestId": "f0a1b2c3-d4e5-6789-abcd-012345678901"
}
```

#### 创建访问密钥

```bash
volcengine-cli iam CreateAccessKey --RegionId cn-beijing \
  --UserName app-service-account
```

**输出示例**:
```json
{
  "AccessKeyId": "AKLT****************************",
  "AccessKeySecret": "****************************",
  "Status": "Active",
  "CreateTime": "2026-05-14T10:00:00Z"
}
```

**注意**: AccessKeySecret 仅在创建时返回，请妥善保存

#### 绑定策略

```bash
# 绑定系统策略
volcengine-cli iam AttachPolicy --RegionId cn-beijing \
  --UserName app-service-account \
  --PolicyType System \
  --PolicyName ReadOnlyAccess

# 绑定自定义策略
volcengine-cli iam AttachPolicy --RegionId cn-beijing \
  --UserName app-service-account \
  --PolicyType Custom \
  --PolicyName MyCustomPolicy \
  --PolicyScope All
```

**输出示例**:
```json
{
  "RequestId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

#### 绑定标签

```bash
volcengine-cli iam TagUser --RegionId cn-beijing \
  --UserName app-service-account \
  --TagKeys '[{"Key": "Environment", "Value": "Production"}]'
```

### 10.2 资源目录

#### 查询资源组

```bash
volcengine-cli resourcemanager ListResourceGroups --RegionId cn-beijing
```

**输出示例**:
```json
{
  "ResourceGroups": [
    {
      "ResourceGroupId": "rg-2zeaf0ls2p7k9****",
      "ResourceGroupName": "default",
      "DisplayName": "默认资源组",
      "Type": "System",
      "CreatedAt": "2025-01-01T00:00:00Z"
    },
    {
      "ResourceGroupId": "rg-2zeaf0ls2p8k****",
      "ResourceGroupName": "production",
      "DisplayName": "生产环境",
      "Type": "Custom",
      "CreatedAt": "2026-01-15T08:00:00Z"
    }
  ],
  "TotalCount": 2
}
```

#### 创建资源组

```bash
volcengine-cli resourcemanager CreateResourceGroup --RegionId cn-beijing \
  --ResourceGroupName staging \
  --DisplayName "预发布环境"
```

**输出示例**:
```json
{
  "ResourceGroupId": "rg-2zeaf0ls2p0k****",
  "ResourceGroupName": "staging",
  "RequestId": "b2c3d4e5-f6a7-8901-bcde-f23456789012"
}
```

#### 移动资源

```bash
# 将 ECS 实例移动到指定资源组
volcengine-cli resourcemanager MoveResources --RegionId cn-beijing \
  --SourceResourceGroupId rg-2zeaf0ls2p7k9**** \
  --TargetResourceGroupId rg-2zeaf0ls2p8k**** \
  --ResourceTypes '["EcsInstance"]' \
  --ResourceIds '["i-2zeaf0ls2p8k****"]'
```

**输出示例**:
```json
{
  "RequestId": "c3d4e5f6-a7b8-9012-cdef-345678901234"
}
```

---

## 11. 附录：产品CLI名称映射表

### 11.1 服务与 CLI 服务名对照

| 产品名称 | CLI 服务名 | 说明 |
|---------|-----------|------|
| 云服务器 ECS | `ecs` | Elastic Compute Service |
| 容器实例 VCI | `vci` | Volcano Container Instance |
| 函数服务 | `function` | Serverless Function |
| 对象存储 TOS | `tos` | 通过 tosutil 工具操作 |
| 云硬盘 | `ecs` | 与 ECS 统一管理 |
| RDS MySQL/PostgreSQL | `rds` | Relational Database Service |
| Redis 数据库 | `redis` | Volcano Engine Redis |
| MongoDB | `mongo` | Volcano Engine MongoDB |
| 私有网络 VPC | `vpc` | Virtual Private Cloud |
| 负载均衡 CLB | `clb` | Cloud Load Balancer |
| 弹性 IP | `eip` | Elastic IP Address |
| 密钥管理 KMS | `kms` | Key Management Service |
| 安全组 | `ecs` | 与 ECS 统一管理 |
| 云监控 | `cms` | Cloud Monitor Service |
| 日志服务 | `log` | Log Service |
| 容器引擎 VKE | `vke` | Volcano Kubernetes Engine |
| 镜像仓库 | `vke` | Container Registry |
| IAM 访问控制 | `iam` | Identity and Access Management |
| 资源目录 | `resourcemanager` | Resource Management |
| Kafka 消息队列 | `kafka` | Managed Kafka Service |
| RocketMQ 消息队列 | `rocketmq` | Managed RocketMQ Service |

### 11.2 常用 API 端点

| 服务 | 端点 |
|------|------|
| ECS | `https://ecs.volcengineapi.com` |
| VPC | `https://vpc.volcengineapi.com` |
| CLB | `https://clb.volcengineapi.com` |
| RDS | `https://rds.volcengineapi.com` |
| Redis | `https://redis.volcengineapi.com` |
| TOS | `https://tos.volcengineapi.com` |
| KMS | `https://kms.volcengineapi.com` |
| VKE | `https://vke.volcengineapi.com` |
| CMS | `https://cms.volcengineapi.com` |
| Log | `https://log.volcengineapi.com` |

### 11.3 区域 ID 映射

| 区域名 | Region ID |
|--------|-----------|
| 北京 | `cn-beijing` |
| 上海 | `cn-shanghai` |
| 广州 | `cn-guangzhou` |
| 新加坡 | `ap-singapore` |
| 印度尼西亚 | `ap-jakarta` |
| 日本 | `ap-tokyo` |
| 美国东部 | `us-east-1` |
| 美国西部 | `us-west-1` |

### 11.4 输出格式说明

```bash
# JSON 格式 (默认)
volcengine-cli ecs DescribeInstances --output json

# Table 表格格式 (适合人类阅读)
volcengine-cli ecs DescribeInstances --output table

# Text 文本格式 (适合脚本解析)
volcengine-cli ecs DescribeInstances --output text
```

**Table 格式输出示例**:
```
+---------------+------------------+-------------+--------+
| InstanceId    | InstanceName     | InstanceType| Status |
+---------------+------------------+-------------+--------+
| i-2zeaf...    | web-server-01    | ecs.c3.large| Running|
+---------------+------------------+-------------+--------+
```

### 11.5 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| `InvalidAccessKeyId` | Access Key 无效 | 检查 Access Key ID 是否正确 |
| `SignatureDoesNotMatch` | 签名不匹配 | 检查 Access Key Secret 是否正确 |
| `InvalidRegion` | Region 无效 | 使用正确的 Region ID |
| `ResourceNotFound` | 资源不存在 | 检查资源 ID 是否正确 |
| `InsufficientBalance` | 余额不足 | 充值后重试 |
| `Unauthorized` | 未授权 | 检查是否具有相应权限 |
| `RequestLimitExceeded` | 请求超限 | 降低请求频率或申请提升配额 |

### 11.6 配额限制

| 资源 | 默认配额 | 可申请提升 |
|------|---------|----------|
| ECS 实例 (按量) | 100 台/区域 | 是 |
| ECS 实例 (包年包月) | 50 台/区域 | 是 |
| 安全组 | 100 个/VPC | 是 |
| 安全组规则 | 100 条/安全组 | 是 |
| VPC | 20 个/区域 | 是 |
| 虚拟交换机 | 50 个/VPC | 是 |
| 弹性 IP | 20 个/账户 | 是 |
| RDS 实例 | 50 个/区域 | 是 |
| Redis 实例 | 50 个/区域 | 是 |

---

## 相关链接

- [火山引擎官网](https://www.volcengine.com)
- [火山引擎 CLI 文档](https://www.volcengine.com/docs/cli)
- [火山引擎 API 文档](https://www.volcengine.com/docs/api)
- [火山引擎开发者社区](https://www.volcengine.com/community)

---

*本文档由 OpenDemo 项目整理，如有问题请提交 Issue。*