# 移动云CLI命令速查表

> 中国移动移动云命令行工具完整参考手册，覆盖计算、存储、数据库、网络等核心产品线

---

## 1. 安装与配置

### 安装方法

移动云CLI工具可通过以下方式安装：

```bash
# 使用pip安装（Python 3.6+）
pip install cmcc-cli

# 验证安装
cmcc-cli --version
# 输出：cmcc-cli version 1.2.3

# 升级到最新版本
pip install --upgrade cmcc-cli
```

### 配置凭证

使用 `cmcc-cli configure` 命令配置访问凭证：

```bash
# 交互式配置（推荐）
cmcc-cli configure

# 命令行直接配置
cmcc-cli configure set --access-key AKI******* --secret-key SK**************************** --region cn-north-4

# 查看当前配置
cmcc-cli configure list
# 输出：
# [default]
# access-key = AKI*******
# secret-key = ********
# region     = cn-north-4
# output     = json

# 多账号配置
cmcc-cli configure set --profile prod --access-key AKI******* --secret-key SK**************************** --region cn-east-2

# 切换账号
export CMCC_PROFILE=prod
```

### 全局参数

所有命令支持以下全局参数：

```bash
--profile <profile_name>      # 指定配置账号
--region <region_id>          # 指定地域（覆盖配置文件）
--output <json|text|table>    # 指定输出格式
--endpoint <url>              # 指定API端点
--verify-ssl                  # 启用SSL验证（默认开启）
--timeout <seconds>           # 请求超时时间（默认60秒）
--debug                        # 开启调试模式

# 示例：指定地域和输出格式
cmcc-cli ecs DescribeInstances --region cn-north-4 --output table
```

---

## 2. 计算服务

### ECS云服务器

#### 查询实例列表

```bash
cmcc-cli ecs DescribeInstances

# 输出（JSON格式）：
{
  "Instances": [
    {
      "InstanceId": "ecs-2zeb3f3a8a****",
      "InstanceName": "web-server-01",
      "InstanceType": "ecs.s6.xlarge.2",
      "Status": "Running",
      "PublicIpAddress": ["211.****.***.162"],
      "PrivateIpAddress": ["192.168.1.10"],
      "ZoneId": "cn-north-4a",
      "CreatedTime": "2025-03-15T10:30:00Z"
    },
    {
      "InstanceId": "ecs-2zeb3f3a8b****",
      "InstanceName": "db-server-01",
      "InstanceType": "ecs.s6.2xlarge.4",
      "Status": "Running",
      "PublicIpAddress": [],
      "PrivateIpAddress": ["192.168.1.20"],
      "ZoneId": "cn-north-4a",
      "CreatedTime": "2025-03-16T14:20:00Z"
    }
  ],
  "TotalCount": 2,
  "PageNumber": 1,
  "PageSize": 10
}
```

#### 创建实例

```bash
cmcc-cli ecs RunInstances \
  --InstanceName web-server-prod \
  --InstanceType ecs.s6.xlarge.2 \
  --ImageId image-ubuntu22.04 \
  --VSwitchId vsw-2ze3**** \
  --SecurityGroupId sg-2ze4**** \
  --KeyPairName my-keypair \
  --ZoneId cn-north-4a

# 输出：
{
  "InstanceId": "ecs-2zeb3f3a8c****",
  "OrderId": "order-2ze3****",
  "ZoneId": "cn-north-4a"
}
```

#### 停止实例

```bash
cmcc-cli ecs StopInstances --InstanceId ecs-2zeb3f3a8a****

# 输出：
{
  "InstanceId": "ecs-2zeb3f3a8a****",
  "Code": "Success",
  "Message": "stop instance success"
}
```

#### 重启实例

```bash
cmcc-cli ecs RebootInstances --InstanceId ecs-2zeb3f3a8a****

# 输出：
{
  "InstanceId": "ecs-2zeb3f3a8a****",
  "Code": "Success",
  "Message": "reboot instance success"
}
```

#### 删除实例

```bash
cmcc-cli ecs TerminateInstances --InstanceId ecs-2zeb3f3a8a**** --Force true

# 输出：
{
  "InstanceId": "ecs-2zeb3f3a8a****",
  "Code": "Success",
  "Message": "terminate instance success"
}
```

#### 查询镜像

```bash
cmcc-cli ecs DescribeImages --ImageName "Ubuntu 22.04"

# 输出：
{
  "Images": [
    {
      "ImageId": "image-ubuntu22.04",
      "ImageName": "Ubuntu 22.04 64bit",
      "OSName": "Ubuntu 22.04 LTS 64bit",
      "Platform": "Ubuntu",
      "Status": "Available",
      "Size": 40
    }
  ]
}
```

#### 创建云硬盘

```bash
cmcc-cli ecs CreateDisk \
  --DiskName data-disk-01 \
  --DiskType SSD \
  --Size 100 \
  --ZoneId cn-north-4a

# 输出：
{
  "DiskId": "disk-2ze3****",
  "OrderId": "order-2ze4****",
  "ZoneId": "cn-north-4a"
}
```

#### 挂载云硬盘

```bash
cmcc-cli ecs AttachDisk \
  --InstanceId ecs-2zeb3f3a8a**** \
  --DiskId disk-2ze3****

# 输出：
{
  "InstanceId": "ecs-2zeb3f3a8a****",
  "DiskId": "disk-2ze3****",
  "Code": "Success"
}
```

### 容器服务

#### 查询容器集群

```bash
cmcc-cli cs DescribeClusters

# 输出：
{
  "Clusters": [
    {
      "ClusterId": "cls-2ze3a8b****",
      "ClusterName": "production-cluster",
      "ClusterType": "ManagedKubernetes",
      "Version": "1.26.3",
      "Status": "Running",
      "NodeCount": 5,
      "ZoneId": "cn-north-4a",
      "CreatedTime": "2025-01-10T08:00:00Z"
    }
  ]
}
```

#### 创建容器集群

```bash
cmcc-cli cs CreateCluster \
  --ClusterName test-cluster \
  --ClusterType ManagedKubernetes \
  --KubernetesVersion 1.26.3 \
  --VSwitchId vsw-2ze3**** \
  --ZoneId cn-north-4a \
  --NodeCount 3

# 输出：
{
  "ClusterId": "cls-2ze4b8c****",
  "ClusterName": "test-cluster",
  "Status": "Creating",
  "TaskId": "task-2ze4****"
}
```

#### 扩容容器集群

```bash
cmcc-cli cs ScaleCluster \
  --ClusterId cls-2ze4b8c**** \
  --NodeCount 5

# 输出：
{
  "ClusterId": "cls-2ze4b8c****",
  "NodeCount": 5,
  "Code": "Success",
  "Message": "scale cluster success"
}
```

#### 删除容器集群

```bash
cmcc-cli cs DeleteCluster --ClusterId cls-2ze4b8c****

# 输出：
{
  "ClusterId": "cls-2ze4b8c****",
  "Code": "Success",
  "Message": "delete cluster success"
}
```

---

## 3. 存储服务

### OBS对象存储

移动云OBS兼容S3风格命令：

```bash
# 配置OBS凭证
cmcc-cli obs configure \
  --access-key AKI******* \
  --secret-key SK**************************** \
  --endpoint obs.cn-north-4.mycloud.com

# 列出所有桶
cmcc-cli obs ls

# 输出：
# 2025-04-01 10:00:00  obs://app-backups        (default)
# 2025-04-15 14:30:00  obs://web-static-assets
# 2025-05-01 09:00:00  obs://logs-archive

# 创建桶
cmcc-cli obs mb obs://my-bucket-2025

# 输出：
# make_bucket: obs://my-bucket-2025 was created successfully

# 上传文件
cmcc-cli obs cp ./app.tar.gz obs://app-backups/app-v2.0.tar.gz

# 输出：
# upload: ./app.tar.gz to obs://app-backups/app-v2.0.tar.gz
# progress: 100%|██████████████████████████████| 1.2GB/1.2GB
# success: uploaded to obs://app-backups/app-v2.0.tar.gz

# 下载文件
cmcc-cli obs cp obs://app-backups/app-v2.0.tar.gz ./downloads/

# 输出：
# download: obs://app-backups/app-v2.0.tar.gz to ./downloads/app-v2.0.tar.gz
# success: downloaded to ./downloads/app-v2.0.tar.gz

# 删除对象
cmcc-cli obs rm obs://app-backups/old-backup.tar.gz

# 输出：
# delete: obs://app-backups/old-backup.tar.gz
# success: deleted

# 同步目录
cmcc-cli obs sync ./dist obs://web-static-assets/ \
  --exclude "*.map" \
  --delete

# 输出：
# sync: ./dist to obs://web-static-assets/
# Added:    125 objects (45.2MB)
# Updated:   12 objects (8.1MB)
# Deleted:    3 objects (1.2MB)
# sync finished in 12.5s
```

### 云硬盘

#### 查询云硬盘

```bash
cmcc-cli ecs DescribeDisks

# 输出：
{
  "Disks": [
    {
      "DiskId": "disk-2ze3****",
      "DiskName": "data-disk-01",
      "DiskType": "SSD",
      "Size": 100,
      "Status": "In_Use",
      "InstanceId": "ecs-2zeb3f3a8a****",
      "ZoneId": "cn-north-4a",
      "CreatedTime": "2025-03-15T12:00:00Z"
    },
    {
      "DiskId": "disk-2ze4****",
      "DiskName": "backup-disk-01",
      "DiskType": "EHDD",
      "Size": 500,
      "Status": "Available",
      "ZoneId": "cn-north-4a",
      "CreatedTime": "2025-04-01T09:00:00Z"
    }
  ],
  "TotalCount": 2
}
```

#### 创建云硬盘

```bash
cmcc-cli ecs CreateDisk \
  --DiskName my-data-disk \
  --DiskType SSD \
  --Size 200 \
  --ZoneId cn-north-4a \
  --Count 1

# 输出：
{
  "DiskId": "disk-2ze5****",
  "DiskName": "my-data-disk",
  "DiskType": "SSD",
  "Size": 200,
  "ZoneId": "cn-north-4a",
  "Status": "Creating"
}
```

#### 挂载云硬盘

```bash
cmcc-cli ecs AttachDisk \
  --InstanceId ecs-2zeb3f3a8b**** \
  --DiskId disk-2ze5****

# 输出：
{
  "InstanceId": "ecs-2zeb3f3a8b****",
  "DiskId": "disk-2ze5****",
  "Code": "Success",
  "Message": "attach disk success"
}
```

---

## 4. 数据库服务

### MySQL

#### 查询数据库列表

```bash
cmcc-cli rds DescribeDatabases --InstanceId mysql-2ze3****

# 输出：
{
  "Databases": [
    {
      "DatabaseName": "app_production",
      "CharacterSet": "utf8mb4",
      "Status": "Running",
      "CreatedTime": "2025-02-01T10:00:00Z"
    },
    {
      "DatabaseName": "app_staging",
      "CharacterSet": "utf8mb4",
      "Status": "Running",
      "CreatedTime": "2025-03-15T14:30:00Z"
    }
  ]
}
```

#### 创建数据库

```bash
cmcc-cli rds CreateDatabase \
  --InstanceId mysql-2ze3**** \
  --DatabaseName app_newdb \
  --CharacterSet utf8mb4

# 输出：
{
  "DatabaseName": "app_newdb",
  "InstanceId": "mysql-2ze3****",
  "CharacterSet": "utf8mb4",
  "Status": "Creating"
}
```

#### 创建数据库账号

```bash
cmcc-cli rds CreateAccount \
  --InstanceId mysql-2ze3**** \
  --AccountName appadmin \
  --AccountPassword P@ssw0rd!**** \
  --DBName app_production

# 输出：
{
  "AccountName": "appadmin",
  "InstanceId": "mysql-2ze3****",
  "Status": "Creating"
}
```

#### 授权账号

```bash
cmcc-cli rds GrantPrivilege \
  --InstanceId mysql-2ze3**** \
  --AccountName appadmin \
  --DBName app_production \
  --Privilege ReadWrite

# 输出：
{
  "AccountName": "appadmin",
  "DBName": "app_production",
  "Privilege": "ReadWrite",
  "Code": "Success"
}
```

#### 创建备份

```bash
cmcc-cli rds CreateBackup \
  --InstanceId mysql-2ze3**** \
  --BackupType Auto \
  --RetentionDays 7

# 输出：
{
  "BackupId": "backup-2ze4****",
  "InstanceId": "mysql-2ze3****",
  "BackupType": "Auto",
  "Status": "Running",
  "EstimatedDuration": 600
}
```

### Redis

#### 查询Redis实例

```bash
cmcc-cli redis DescribeInstances

# 输出：
{
  "Instances": [
    {
      "InstanceId": "redis-2ze3****",
      "InstanceName": "cache-prod",
      "InstanceType": "Redis5.0_Standard",
      "Capacity": 1024,
      "Status": "Running",
      "ZoneId": "cn-north-4a",
      "VpcId": "vpc-2ze3****",
      "CreatedTime": "2025-01-20T08:00:00Z"
    }
  ]
}
```

#### 创建Redis实例

```bash
cmcc-cli redis CreateInstance \
  --InstanceName cache-test \
  --InstanceType Redis5.0_Standard \
  --Capacity 1024 \
  --VpcId vpc-2ze3**** \
  --VSwitchId vsw-2ze4**** \
  --ZoneId cn-north-4a \
  --Password "P@ssw0rd!****"

# 输出：
{
  "InstanceId": "redis-2ze5****",
  "InstanceName": "cache-test",
  "Status": "Creating",
  "OrderId": "order-2ze5****"
}
```

### MongoDB

#### 查询MongoDB实例

```bash
cmcc-cli mongodb DescribeInstances

# 输出：
{
  "Instances": [
    {
      "InstanceId": "mongodb-2ze3****",
      "InstanceName": "mongo-prod",
      "InstanceType": "MongoDB4.0_Standard",
      "Storage": 50,
      "Status": "Running",
      "ReplicaNum": 3,
      "ZoneId": "cn-north-4a",
      "CreatedTime": "2025-02-15T10:00:00Z"
    }
  ]
}
```

#### 创建MongoDB实例

```bash
cmcc-cli mongodb CreateInstance \
  --InstanceName mongo-test \
  --InstanceType MongoDB4.0_Standard \
  --Storage 100 \
  --ReplicaNum 3 \
  --VpcId vpc-2ze3**** \
  --VSwitchId vsw-2ze4**** \
  --ZoneId cn-north-4a \
  --Password "P@ssw0rd!****"

# 输出：
{
  "InstanceId": "mongodb-2ze5****",
  "InstanceName": "mongo-test",
  "Status": "Creating",
  "OrderId": "order-2ze5****"
}
```

---

## 5. 网络服务

### VPC

#### 查询VPC列表

```bash
cmcc-cli vpc DescribeVpcs

# 输出：
{
  "Vpcs": [
    {
      "VpcId": "vpc-2ze3****",
      "VpcName": "production-vpc",
      "CidrBlock": "192.168.0.0/16",
      "Status": "Available",
      "CreatedTime": "2024-12-01T08:00:00Z"
    },
    {
      "VpcId": "vpc-2ze4****",
      "VpcName": "development-vpc",
      "CidrBlock": "10.0.0.0/8",
      "Status": "Available",
      "CreatedTime": "2025-01-15T10:00:00Z"
    }
  ]
}
```

#### 创建VPC

```bash
cmcc-cli vpc CreateVpc \
  --VpcName web-vpc \
  --CidrBlock 172.16.0.0/24

# 输出：
{
  "VpcId": "vpc-2ze5****",
  "VpcName": "web-vpc",
  "CidrBlock": "172.16.0.0/24",
  "Status": "Creating"
}
```

#### 查询交换机

```bash
cmcc-cli vpc DescribeVSwitches --VpcId vpc-2ze3****

# 输出：
{
  "VSwitches": [
    {
      "VSwitchId": "vsw-2ze3****",
      "VSwitchName": "web-subnet",
      "CidrBlock": "192.168.1.0/24",
      "ZoneId": "cn-north-4a",
      "Status": "Available"
    },
    {
      "VSwitchId": "vsw-2ze4****",
      "VSwitchName": "db-subnet",
      "CidrBlock": "192.168.2.0/24",
      "ZoneId": "cn-north-4b",
      "Status": "Available"
    }
  ]
}
```

#### 创建交换机

```bash
cmcc-cli vpc CreateVSwitch \
  --VSwitchName app-subnet \
  --VpcId vpc-2ze3**** \
  --CidrBlock 192.168.3.0/24 \
  --ZoneId cn-north-4a

# 输出：
{
  "VSwitchId": "vsw-2ze5****",
  "VSwitchName": "app-subnet",
  "VpcId": "vpc-2ze3****",
  "CidrBlock": "192.168.3.0/24",
  "ZoneId": "cn-north-4a",
  "Status": "Creating"
}
```

#### 创建路由表

```bash
cmcc-cli vpc CreateRouteTable \
  --RouteTableName web-routes \
  --VpcId vpc-2ze3****

# 输出：
{
  "RouteTableId": "rt-2ze5****",
  "RouteTableName": "web-routes",
  "VpcId": "vpc-2ze3****",
  "Routes": []
}
```

### 负载均衡

#### 查询负载均衡器

```bash
cmcc-cli elb DescribeLoadBalancers

# 输出：
{
  "LoadBalancers": [
    {
      "LoadBalancerId": "lb-2ze3****",
      "LoadBalancerName": "web-lb",
      "LoadBalancerType": "public",
      "Status": "active",
      "Address": "211.****.***.58",
      "ZoneMappings": [
        {"ZoneId": "cn-north-4a", "EipId": "eip-2ze3****"}
      ],
      "CreatedTime": "2025-03-01T10:00:00Z"
    }
  ]
}
```

#### 创建负载均衡器

```bash
cmcc-cli elb CreateLoadBalancer \
  --LoadBalancerName api-lb \
  --LoadBalancerType public \
  --VpcId vpc-2ze3**** \
  --ZoneMappings '[{"ZoneId":"cn-north-4a","EipId":"eip-2ze3****"}]' \
  --ChargeType PostPaid

# 输出：
{
  "LoadBalancerId": "lb-2ze4****",
  "LoadBalancerName": "api-lb",
  "Status": "Creating",
  "Address": "211.****.***.91"
}
```

#### 注册后端目标

```bash
cmcc-cli elb RegisterTargets \
  --LoadBalancerId lb-2ze3**** \
  --TargetServerInfos '[{"ServerId":"ecs-2zeb3f3a8a****","Port":80},{"ServerId":"ecs-2zeb3f3a8b****","Port":80}]'

# 输出：
{
  "LoadBalancerId": "lb-2ze3****",
  "TargetServerInfos": [
    {"ServerId": "ecs-2zeb3f3a8a****", "Port": 80, "Status": "adding"},
    {"ServerId": "ecs-2zeb3f3a8b****", "Port": 80, "Status": "adding"}
  ],
  "Code": "Success"
}
```

### 弹性IP

#### 查询弹性IP

```bash
cmcc-cli eip DescribeEips

# 输出：
{
  "Eips": [
    {
      "EipId": "eip-2ze3****",
      "IpAddress": "211.****.***.58",
      "Status": "InUse",
      "InstanceType": "LoadBalancer",
      "InstanceId": "lb-2ze3****",
      "Bandwidth": 200,
      "ChargeMode": "bandwidth",
      "CreatedTime": "2025-03-01T10:00:00Z"
    },
    {
      "EipId": "eip-2ze4****",
      "IpAddress": "211.****.***.102",
      "Status": "Available",
      "Bandwidth": 5,
      "ChargeMode": "bandwidth",
      "CreatedTime": "2025-04-10T14:00:00Z"
    }
  ]
}
```

#### 申请弹性IP

```bash
cmcc-cli eip AllocateEipAddress \
  --Bandwidth 100 \
  --ChargeMode bandwidth \
  --InternetChargeType payByBandwidth

# 输出：
{
  "EipId": "eip-2ze5****",
  "IpAddress": "211.****.***.215",
  "Status": "Available",
  "Bandwidth": 100
}
```

#### 绑定弹性IP

```bash
cmcc-cli eip AssociateEipAddress \
  --EipId eip-2ze4**** \
  --InstanceId ecs-2zeb3f3a8a**** \
  --InstanceType Ecs

# 输出：
{
  "EipId": "eip-2ze4****",
  "InstanceId": "ecs-2zeb3f3a8a****",
  "InstanceType": "Ecs",
  "Code": "Success",
  "Message": "associate eip success"
}
```

---

## 6. 监控

### 云监控

#### 查询监控指标

```bash
cmcc-cli monitor ListMetrics \
  --Namespace "ACS/ECS" \
  --Dimensions '[{"InstanceId":"ecs-2zeb3f3a8a****"}]'

# 输出：
{
  "Metrics": [
    {
      "MetricName": "CPUUtilization",
      "Namespace": "ACS/ECS",
      "Dimensions": [
        {"InstanceId": "ecs-2zeb3f3a8a****"}
      ],
      "Unit": "Percent",
      "Statistics": ["Average", "Maximum", "Minimum"]
    },
    {
      "MetricName": "IntranetInRate",
      "Namespace": "ACS/ECS",
      "Dimensions": [
        {"InstanceId": "ecs-2zeb3f3a8a****"}
      ],
      "Unit": "Bps",
      "Statistics": ["Average", "Maximum"]
    },
    {
      "MetricName": "IntranetOutRate",
      "Namespace": "ACS/ECS",
      "Dimensions": [
        {"InstanceId": "ecs-2zeb3f3a8a****"}
      ],
      "Unit": "Bps",
      "Statistics": ["Average", "Maximum"]
    }
  ]
}
```

#### 查询监控数据

```bash
cmcc-cli monitor GetMetricData \
  --Namespace ACS/ECS \
  --MetricName CPUUtilization \
  --Dimensions '[{"InstanceId":"ecs-2zeb3f3a8a****"}]' \
  --StartTime 1747200000 \
  --EndTime 1747286400 \
  --Period 300

# 输出：
{
  "Datapoints": [
    {
      "Timestamp": 1747200300,
      "Average": 23.5,
      "Maximum": 45.2,
      "Minimum": 12.1
    },
    {
      "Timestamp": 1747200600,
      "Average": 25.8,
      "Maximum": 48.7,
      "Minimum": 14.3
    }
  ],
  "Period": 300,
  "Code": "Success"
}
```

#### 创建告警规则

```bash
cmcc-cli monitor CreateAlarm \
  --AlarmName high-cpu-alert \
  --Namespace ACS/ECS \
  --MetricName CPUUtilization \
  --Dimensions '[{"InstanceId":"ecs-2zeb3f3a8a****"}]' \
  --Condition "Average > 80" \
  --Period 300 \
  --EvaluationPeriods 3 \
  --NotificationType "SMS,Email" \
  --AlarmActions '[{"NotificationArn":"acs:rmc:cn-north-4:123456789:contacts/test-user"}]'

# 输出：
{
  "AlarmGuid": "alarm-2ze5****",
  "AlarmName": "high-cpu-alert",
  "Status": "Enabled",
  "Code": "Success"
}
```

---

## 7. 资源管理

### IAM

#### 查询用户列表

```bash
cmcc-cli iam ListUsers

# 输出：
{
  "Users": [
    {
      "UserId": "user-2ze3****",
      "UserName": "admin",
      "DisplayName": "Administrator",
      "Email": "admin@example.com",
      "Status": "Active",
      "CreatedTime": "2024-01-01T00:00:00Z"
    },
    {
      "UserId": "user-2ze4****",
      "UserName": "developer",
      "DisplayName": "Developer Account",
      "Email": "dev@example.com",
      "Status": "Active",
      "CreatedTime": "2025-02-01T10:00:00Z"
    }
  ]
}
```

#### 创建用户

```bash
cmcc-cli iam CreateUser \
  --UserName deploy-bot \
  --DisplayName "Deployment Bot" \
  --Email deploy-bot@example.com \
  --Phone "13800138000"

# 输出：
{
  "UserId": "user-2ze5****",
  "UserName": "deploy-bot",
  "DisplayName": "Deployment Bot",
  "Status": "Active",
  "SecretStatus": "Active"
}
```

#### 创建访问密钥

```bash
cmcc-cli iam CreateAccessKey --UserName deploy-bot

# 输出：
{
  "AccessKey": {
    "AccessKeyId": "AKI*******",
    "SecretKey": "SK****************************",
    "Status": "Active",
    "CreateTime": "2025-05-14T10:00:00Z"
  },
  "Warning": "SecretKey will only be shown once. Please save it securely."
}
```

---

## 8. 安全服务

### 密钥管理KMS

#### 查询密钥列表

```bash
cmcc-cli kms ListKeys --RegionId cn-east-1

# 输出：
{
  "Keys": [
    {
      "KeyId": "key-2ze3****",
      "KeyUsage": "ENCRYPT/DECRYPT",
      "KeyStatus": "Enabled",
      "CreatedTime": "2025-04-01T10:00:00Z"
    }
  ]
}
```

#### 创建密钥

```bash
cmcc-cli kms CreateKey --RegionId cn-east-1 --KeyUsage ENCRYPT/DECRYPT

# 输出：
{
  "KeyId": "key-2ze4****",
  "KeyUsage": "ENCRYPT/DECRYPT",
  "KeyStatus": "Enabled",
  "CreateTime": "2025-05-14T10:00:00Z"
}
```

#### 加密数据

```bash
cmcc-cli kms Encrypt \
  --RegionId cn-east-1 \
  --KeyId key-2ze3**** \
  --Plaintext "SGVsbG8gV29ybGQ="

# 输出：
{
  "KeyId": "key-2ze3****",
  "CiphertextBlob": "...",
  "Code": "Success"
}
```

#### 解密数据

```bash
cmcc-cli kms Decrypt \
  --RegionId cn-east-1 \
  --KeyId key-2ze3**** \
  --CiphertextBlob "..."

# 输出：
{
  "KeyId": "key-2ze3****",
  "Plaintext": "SGVsbG8gV29ybGQ=",
  "Code": "Success"
}
```

### 安全组

#### 查询安全组

```bash
cmcc-cli ecs DescribeSecurityGroups --RegionId cn-east-1

# 输出：
{
  "SecurityGroups": [
    {
      "SecurityGroupId": "sg-2ze3****",
      "SecurityGroupName": "my-sg",
      "VpcId": "vpc-2ze3****",
      "Status": "Available",
      "CreatedTime": "2025-03-01T10:00:00Z"
    }
  ]
}
```

#### 创建安全组

```bash
cmcc-cli ecs CreateSecurityGroup \
  --RegionId cn-east-1 \
  --SecurityGroupName my-sg

# 输出：
{
  "SecurityGroupId": "sg-2ze4****",
  "SecurityGroupName": "my-sg",
  "Status": "Created"
}
```

#### 添加安全组规则

```bash
cmcc-cli ecs AuthorizeSecurityGroup \
  --RegionId cn-east-1 \
  --SecurityGroupId sg-2ze3**** \
  --IpProtocol tcp \
  --PortRange 22/22 \
  --SourceCidrIp 0.0.0.0/0

# 输出：
{
  "SecurityGroupId": "sg-2ze3****",
  "Code": "Success",
  "Message": "authorize security group success"
}
```

---

## 9. 中间件服务

### Kafka消息队列

#### 查询实例

```bash
cmcc-cli kafka DescribeInstances --RegionId cn-east-1

# 输出：
{
  "Instances": [
    {
      "InstanceId": "kafka-2ze3****",
      "InstanceName": "kafka-prod",
      "Status": "Running",
      "ZoneId": "cn-east-1",
      "Spec": "kafka.2xlarge",
      "CreatedTime": "2025-02-15T10:00:00Z"
    }
  ]
}
```

#### 创建Topic

```bash
cmcc-cli kafka CreateTopic \
  --RegionId cn-east-1 \
  --InstanceId kafka-2ze3**** \
  --Topic my-topic \
  --Partitions 6

# 输出：
{
  "Topic": "my-topic",
  "InstanceId": "kafka-2ze3****",
  "Partitions": 6,
  "Code": "Success"
}
```

### RabbitMQ消息队列

#### 查询实例

```bash
cmcc-cli rabbitmq DescribeInstances --RegionId cn-east-1

# 输出：
{
  "Instances": [
    {
      "InstanceId": "rabbitmq-2ze3****",
      "InstanceName": "rabbitmq-prod",
      "Status": "Running",
      "ZoneId": "cn-east-1",
      "Spec": "rabbitmq.2xlarge",
      "CreatedTime": "2025-03-01T10:00:00Z"
    }
  ]
}
```

#### 创建队列

```bash
cmcc-cli rabbitmq CreateQueue \
  --RegionId cn-east-1 \
  --InstanceId rabbitmq-2ze3**** \
  --QueueName my-queue

# 输出：
{
  "QueueName": "my-queue",
  "InstanceId": "rabbitmq-2ze3****",
  "Code": "Success"
}
```

---

## 10. 附录：产品CLI名称映射表

| 产品分类 | 云产品 | CLI命令前缀 | 示例命令 |
|---------|-------|------------|---------|
| **计算** | 云服务器ECS | `ecs` | `cmcc-cli ecs DescribeInstances` |
| | 容器服务CCS | `cs` | `cmcc-cli cs DescribeClusters` |
| **存储** | 对象存储OBS | `obs` | `cmcc-cli obs ls` |
| | 云硬盘EVS | `ecs` | `cmcc-cli ecs DescribeDisks` |
| **数据库** | 云数据库RDS | `rds` | `cmcc-cli rds DescribeDatabases` |
| | 分布式缓存Redis | `redis` | `cmcc-cli redis DescribeInstances` |
| | MongoDB | `mongodb` | `cmcc-cli mongodb DescribeInstances` |
| **网络** | 虚拟私有云VPC | `vpc` | `cmcc-cli vpc DescribeVpcs` |
| | 负载均衡ELB | `elb` | `cmcc-cli elb DescribeLoadBalancers` |
| | 弹性IP EIP | `eip` | `cmcc-cli eip DescribeEips` |
| **监控** | 云监控CMS | `monitor` | `cmcc-cli monitor ListMetrics` |
| **安全** | 身份认证IAM | `iam` | `cmcc-cli iam ListUsers` |
| | 密钥管理KMS | `kms` | `cmcc-cli kms ListKeys` |
| | 安全组SG | `ecs` | `cmcc-cli ecs DescribeSecurityGroups` |
| **中间件** | Kafka消息队列 | `kafka` | `cmcc-cli kafka DescribeInstances` |
| | RabbitMQ消息队列 | `rabbitmq` | `cmcc-cli rabbitmq DescribeInstances` |
| **CDN** | CDN加速 | `cdn` | `cmcc-cli cdn DescribeDomains` |

### 常用地域映射

| 地域ID | 地域名称 | 可用区 |
|-------|---------|-------|
| `cn-north-4` | 华北-北京 | cn-north-4a, cn-north-4b, cn-north-4c |
| `cn-east-2` | 华东-上海 | cn-east-2a, cn-east-2b |
| `cn-south-1` | 华南-广州 | cn-south-1a, cn-south-1b |
| `cn-southwest-2` | 西南-贵阳 | cn-southwest-2a |
| `cn-north-5` | 华北-呼和浩特 | cn-north-5a, cn-north-5b |

### 常用实例类型

| 类型 | 规格 | 适用场景 |
|-----|------|---------|
| `ecs.s6.small.1` | 1核1G | 轻量测试 |
| `ecs.s6.xlarge.2` | 4核8G | 通用Web应用 |
| `ecs.s6.2xlarge.4` | 8核16G | 中型数据库 |
| `ecs.g6.2xlarge.4` | 8核32G | 大数据处理 |
| `ecs.c6.4xlarge.8` | 16核32G | 高性能计算 |

### 常用API端点

| 服务 | 端点地址 |
|-----|---------|
| ECS | `ecs.cn-north-4.mycloud.com` |
| OBS | `obs.cn-north-4.mycloud.com` |
| RDS | `rds.cn-north-4.mycloud.com` |
| VPC | `vpc.cn-north-4.mycloud.com` |
| ELB | `elb.cn-north-4.mycloud.com` |
| IAM | `iam.mycloud.com` |

---

*文档版本：1.0.0*
*最后更新：2025年5月*
*移动云CLI工具官方文档：https://www.movcloud.com/doc/cli*