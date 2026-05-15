# 阿里云CLI命令速查表

> 阿里云命令行工具(Alibaba Cloud CLI)完整参考手册，覆盖计算、存储、数据库、网络、安全等核心产品线

---

## 📋 目录索引

- [安装与配置](#安装与配置)
- [计算服务](#计算服务)
  - [ECS云服务器](#ecs云服务器)
  - [容器服务ACK](#容器服务ack)
  - [函数计算FC](#函数计算fc)
  - [弹性容器实例ECI](#弹性容器实例eci)
- [存储服务](#存储服务)
  - [OSS对象存储](#oss对象存储)
  - [NAS文件存储](#nas文件存储)
  - [云盘与快照](#云盘与快照)
- [数据库服务](#数据库服务)
  - [RDS关系型数据库](#rds关系型数据库)
  - [Redis数据库](#redis数据库)
  - [MongoDB数据库](#mongodb数据库)
- [网络服务](#网络服务)
  - [VPC专有网络](#vpc专有网络)
  - [SLB负载均衡](#slb负载均衡)
  - [NAT网关](#nat网关)
  - [CDN内容分发](#cdn内容分发)
- [安全服务](#安全服务)
  - [安骑士Security](#安骑士security)
  - [云防火墙CloudFirewall](#云防火墙cloudfirewall)
  - [密钥管理KMS](#密钥管理kms)
- [中间件服务](#中间件服务)
  - [消息队列MQ](#消息队列mq)
  - [Kafka消息队列](#kafka消息队列)
  - [分布式协调Nacos](#分布式协调nacos)
- [日志与监控](#日志与监控)
  - [日志服务SLS](#日志服务sls)
  - [云监控CMS](#云监控cms)
- [容器与编排](#容器与编排)
  - [容器镜像服务ACR](#容器镜像服务acr)
  - [企业级分布式应用EDAS](#企业级分布式应用edas)
- [运维与权限](#运维与权限)
  - [资源管理RAM](#资源管理ram)
  - [配置审计Config](#配置审计config)
  - [操作审计ActionTrail](#操作审计actiontrail)

---

## 安装与配置

### 安装

```bash
# Linux/macOS 安装
curl -sSL https://get.cli.aliyun.com | sh

# macOS Homebrew 安装
brew install aliyun-cli

# 验证安装
aliyun --version
```

### 配置凭证

```bash
# 交互式配置（推荐）
aliyun configure --mode AK --access-key-id <Your-AK-ID> --access-key-secret <Your-AK-Secret> --region cn-hangzhou

# 环境变量配置
export ALIBABA_CLOUD_ACCESS_KEY_ID=<Your-AK-ID>
export ALIBABA_CLOUD_ACCESS_KEY_SECRET=<Your-AK-Secret>
export ALIBABA_CLOUD_REGION=cn-hangzhou

# 查看当前配置
aliyun configure list
```

### 常用全局参数

```bash
--region        # 地域ID
--profile       # 配置文件名
--mode          # 凭证模式 (AK/StsToken/RamRoleArn/EcsMetaData)
--output        # 输出格式 (json/table/yaml)
--verbose       # 显示详细调试信息
```

---

## 计算服务

### ECS云服务器

```bash
# 查询可用区实例规格
aliyun ecs DescribeAvailableResource --RegionId cn-hangzhou --DestinationResource InstanceType --InstanceTypeFamily ecs.g7

# 查询实例列表
aliyun ecs DescribeInstances --RegionId cn-hangzhou --output cols=InstanceId,InstanceName,Status,PublicIpAddress

# 查询单个实例详情
aliyun ecs DescribeInstances --RegionId cn-hangzhou --InstanceIds '["i-xxxxxxxxx"]'

# 创建按量付费实例
aliyun ecs CreateInstance --RegionId cn-hangzhou \
  --ImageId ubuntu_22_04_64_20G_alibaba_20231220.vhd \
  --InstanceType ecs.g7.large \
  --SecurityGroupId sg-xxxxxxxx \
  --VSwitchId vsw-xxxxxxxx

# 创建包年包月实例
aliyun ecs CreateInstance --RegionId cn-hangzhou \
  --ImageId ubuntu_22_04_64_20G_alibaba_20231220.vhd \
  --InstanceType ecs.g7.large \
  --SecurityGroupId sg-xxxxxxxx \
  --InstanceChargeType Prepaid \
  --Period 1 --PeriodUnit Month

# 启动实例
aliyun ecs StartInstance --RegionId cn-hangzhou --InstanceId i-xxxxxxxx

# 停止实例
aliyun ecs StopInstance --RegionId cn-hangzhou --InstanceId i-xxxxxxxx

# 重启实例
aliyun ecs RebootInstance --RegionId cn-hangzhou --InstanceId i-xxxxxxxx

# 删除实例
aliyun ecs DeleteInstance --RegionId cn-hangzhou --InstanceId i-xxxxxxxx

# 查询实例状态
aliyun ecs DescribeInstanceStatus --RegionId cn-hangzhou

# 查询磁盘列表
aliyun ecs DescribeDisks --RegionId cn-hangzhou --InstanceId i-xxxxxxxx

# 创建云盘
aliyun ecs CreateDisk --RegionId cn-hangzhou \
  --ZoneId cn-hangzhou-h \
  --DiskCategory cloud_essd \
  --Size 100

# 挂载云盘
aliyun ecs AttachDisk --RegionId cn-hangzhou --InstanceId i-xxxxxxxx --DiskId d-xxxxxxxx

# 解绑云盘
aliyun ecs DetachDisk --RegionId cn-hangzhou --InstanceId i-xxxxxxxx --DiskId d-xxxxxxxx

# 查询安全组列表
aliyun ecs DescribeSecurityGroups --RegionId cn-hangzhou

# 查询安全组规则
aliyun ecs DescribeSecurityGroupRule --RegionId cn-hangzhou --SecurityGroupId sg-xxxxxxxx

# 授权安全组规则
aliyun ecs AuthorizeSecurityGroup --RegionId cn-hangzhou \
  --SecurityGroupId sg-xxxxxxxx \
  --IpProtocol tcp \
  --PortRange 22/22 \
  --SourceCidrIp 0.0.0.0/0

# 查询实例监控数据
aliyun ecs DescribeInstanceMonitorData --RegionId cn-hangzhou --InstanceId i-xxxxxxxx --StartTime 20240501000000
```

---

### 容器服务ACK

```bash
# 查询容器集群列表
aliyun cs DescribeClusters --RegionId cn-hangzhou

# 创建Kubernetes集群
aliyun cs CreateCluster --RegionId cn-hangzhou \
  --Name my-k8s-cluster \
  --ClusterType Kubernetes \
  --VSwitchId vsw-xxxxxxxx \
  --KubernetesVersion 1.28 \
  --NodePoolInstanceTypes '["ecs.g7.large"]' \
  --NumOfNodes 2

# 扩展节点池
aliyun cs ScaleCluster --RegionId cn-hangzhou --ClusterId cs-xxxxxxxx --Count 5

# 删除集群
aliyun cs DeleteCluster --RegionId cn-hangzhou --ClusterId cs-xxxxxxxx

# 查询集群信息
aliyun cs DescribeClusterDetails --RegionId cn-hangzhou --ClusterId cs-xxxxxxxx

# 下载集群kubeconfig
aliyun cs DescribeClusterUserKubeconfig --RegionId cn-hangzhou --ClusterId cs-xxxxxxxx
```

---

### 函数计算FC

```bash
# 查询函数列表
aliyun fc ListFunctions --RegionId cn-hangzhou --ServiceName my-service

# 创建函数
aliyun fc CreateFunction --RegionId cn-hangzhou \
  --ServiceName my-service \
  --FunctionName my-function \
  --Runtime python3.10 \
  --Code '{"zipFile": "base64-encoded-code.zip"}' \
  --Handler index.handler

# 调用函数
aliyun fc InvokeFunction --RegionId cn-hangzhou \
  --ServiceName my-service \
  --FunctionName my-function \
  --Payload '{"key": "value"}'

# 查询函数配置
aliyun fc GetFunction --RegionId cn-hangzhou \
  --ServiceName my-service \
  --FunctionName my-function

# 更新函数代码
aliyun fc UpdateFunctionCode --RegionId cn-hangzhou \
  --ServiceName my-service \
  --FunctionName my-function \
  --Code '{"zipFile": "base64-encoded-new-code.zip"}'

# 删除函数
aliyun fc DeleteFunction --RegionId cn-hangzhou \
  --ServiceName my-service \
  --FunctionName my-function
```

---

### 弹性容器实例ECI

```bash
# 查询ECI实例列表
aliyun eci DescribeContainers --RegionId cn-hangzhou

# 创建ECI实例
aliyun eci CreateContainer --RegionId cn-hangzhou \
  --ContainerGroupName my-container \
  --Cpu 2 \
  --Memory 4 \
  --Image nginx:latest

# 删除ECI实例
aliyun eci DeleteContainerGroup --RegionId cn-hangzhou --ContainerGroupId ecigrp-xxxxxxxx
```

---

## 存储服务

### OSS对象存储

```bash
# 查询Bucket列表
aliyun oss ls oss:// --region cn-hangzhou

# 创建Bucket
aliyun oss mb oss://my-bucket --region cn-hangzhou

# 上传文件
aliyun oss cp ./file.txt oss://my-bucket/ --region cn-hangzhou

# 下载文件
aliyun oss cp oss://my-bucket/file.txt ./download.txt --region cn-hangzhou

# 列出Bucket内文件
aliyun oss ls oss://my-bucket/ --region cn-hangzhou

# 设置Bucket ACL
aliyun oss set-acl oss://my-bucket private --region cn-hangzhou

# 生成签名URL（临时访问）
aliyun oss sign oss://my-bucket/file.txt --region cn-hangzhou --expiry 3600

# 同步目录
aliyun oss sync /local/dir oss://my-bucket/prefix/ --region cn-hangzhou

# 删除文件
aliyun oss rm oss://my-bucket/file.txt --region cn-hangzhou

# 设置存储类型（IA/Archive/ColdArchive）
aliyun oss cp file.txt oss://my-bucket/ --region cn-hangzhou \
  --storage-class IA

# 开启生命周期规则
aliyun oss lifecycle oss://my-bucket --region cn-hangzhou \
  --expiry days=30 --file-type file

# 配置CORS跨域规则
aliyun oss cors oss://my-bucket --region cn-hangzhou \
  --origin "*" --method GET,PUT

# 静态网站托管
aliyun oss website oss://my-bucket --region cn-hangzhou \
  --index index.html --error 404.html

# 跨区域复制
aliyun oss cname oss://my-bucket --region cn-hangzhou --cname "cdn.example.com"
```

---

### NAS文件存储

```bash
# 查询文件系统列表
aliyun nas DescribeFileSystems --RegionId cn-hangzhou

# 创建NAS文件系统
aliyun nas CreateFileSystem --RegionId cn-hangzhou \
  --FileSystemType standard \
  --Capacity 100

# 创建挂载点
aliyun nas CreateMountTarget --RegionId cn-hangzhou \
  --FileSystemId 1xxxxx \
  --VSwitchId vsw-xxxxxxxx \
  --AccessGroupName DEFAULT_VPC_GROUP_NAME

# 查询挂载点
aliyun nas DescribeMountTargets --RegionId cn-hangzhou --FileSystemId 1xxxxx

# 删除挂载点
aliyun nas DeleteMountTarget --RegionId cn-hangzhou \
  --FileSystemId 1xxxxx \
  --MountTargetDomain mount-xxxxx

# 添加权限组规则
aliyun nas AddAccessRule --RegionId cn-hangzhou \
  --AccessGroupName DEFAULT_VPC_GROUP_NAME \
  --SourceCidrIp 10.0.0.0/8 \
  --RWAccessPermission read-write \
  --Priority 1
```

---

### 云盘与快照

```bash
# 查询云盘列表
aliyun ecs DescribeDisks --RegionId cn-hangzhou \
  --DiskCategory cloud_essd \
  --Status Available

# 创建云盘快照
aliyun ecs CreateSnapshot --RegionId cn-hangzhou --DiskId d-xxxxxxxx

# 查询快照列表
aliyun ecs DescribeSnapshots --RegionId cn-hangzhou --DiskId d-xxxxxxxx

# 创建快照策略
aliyun ecs CreateAutoSnapshotPolicy --RegionId cn-hangzhou \
  --TimePoints '["0230"]' \
  --WeekDays '["1,2,3,4,5"]' \
  --RetentionDays 7

# 应用快照策略到云盘
aliyun ecs ApplyAutoSnapshotPolicy --RegionId cn-hangzhou \
  --DiskIds '["d-xxxxxxxx"]'

# 回滚云盘到快照
aliyun ecs ResetDisk --RegionId cn-hangzhou \
  --SnapshotId s-xxxxxxxx \
  --DiskId d-xxxxxxxx

# 删除快照
aliyun ecs DeleteSnapshot --RegionId cn-hangzhou --SnapshotId s-xxxxxxxx

# 复制快照到其他地域
aliyun ecs CopySnapshot --RegionId cn-hangzhou \
  --SourceSnapshotId s-xxxxxxxx \
  --DestinationRegionId cn-beijing

# 云盘加密
aliyun ecs CreateDisk --RegionId cn-hangzhou \
  --ZoneId cn-hangzhou-h \
  --DiskCategory cloud_essd \
  --Size 100 \
  --Encrypted true
```

---

## 数据库服务

### RDS关系型数据库

```bash
# 查询RDS实例列表
aliyun rds DescribeDBInstances --RegionId cn-hangzhou

# 创建RDS实例
aliyun rds CreateDBInstance --RegionId cn-hangzhou \
  --Engine MySQL \
  --EngineVersion 8.0 \
  --DBInstanceClass mysql.n2.large.2 \
  --DBInstanceStorage 20 \
  --ZoneId cn-hangzhou-h \
  --SecurityGroupId sg-xxxxxxxx

# 查询数据库列表
aliyun rds DescribeDatabases --RegionId cn-hangzhou --DBInstanceId rm-xxxxxxxx

# 创建数据库
aliyun rds CreateDatabase --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxxxx \
  --DBName mydb \
  --CharacterSetName utf8mb4

# 查询账号列表
aliyun rds DescribeAccounts --RegionId cn-hangzhou --DBInstanceId rm-xxxxxxxx

# 创建账号
aliyun rds CreateAccount --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxxxx \
  --AccountName myuser \
  --AccountPassword MyP@ssw0rd!

# 授权账号数据库权限
aliyun rds GrantAccountPrivilege --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxxxx \
  --AccountName myuser \
  --DBName mydb \
  --Privilege ReadOnly

# 设置白名单
aliyun rds DescribeDBInstanceIPArray --RegionId cn-hangzhou --DBInstanceId rm-xxxxxxxx

aliyun rds ModifyDBInstanceIPArray --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxxxx \
  --DBInstanceIPArrayName default \
  --SecurityIps "192.168.1.0/24,100.100.100.100"

# 备份数据库
aliyun rds CreateBackup --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxxxx \
  --BackupMethod Physical

# 查询备份列表
aliyun rds DescribeBackups --RegionId cn-hangzhou --DBInstanceId rm-xxxxxxxx

# 恢复数据库
aliyun rds RestoreDBInstance --RegionId cn-hangzhou \
  --TargetDBInstanceId rm-xxxxxxxx \
  --BackupId b-xxxxxxxx

# 变配实例规格
aliyun rds ModifyDBInstanceSpec --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxxxx \
  --DBInstanceClass mysql.n2.large.4

# 开启TDE加密
aliyun rds ModifyDBInstanceTDE --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxxxx \
  --TDEStatus Enabled

# 迁移可用区
aliyun rds SwitchDBInstanceZone --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxxxx \
  --TargetZoneId cn-hangzhou-h
```

---

### Redis数据库

```bash
# 查询Redis实例列表
aliyun kvstore DescribeInstances --RegionId cn-hangzhou --InstanceType Redis

# 创建Redis实例
aliyun kvstore CreateInstance --RegionId cn-hangzhou \
  --InstanceType redis_standard \
  --EngineVersion 6.0 \
  --ShardingType cluster \
  --ReplicaSize 2 \
  --Capacity 64 \
  --ZoneId cn-hangzhou-h

# 查询实例配置
aliyun kvstore DescribeInstanceConfig --RegionId cn-hangzhou --InstanceId r-xxxxxxxx

# 修改实例配置
aliyun kvstore ModifyInstanceConfig --RegionId cn-hangzhou \
  --InstanceId r-xxxxxxxx \
  --Config "{\"maxmemory-policy\":\"volatile-lru\"}"

# 创建账号
aliyun kvstore CreateAccount --RegionId cn-hangzhou \
  --InstanceId r-xxxxxxxx \
  --AccountName myuser \
  --AccountPassword MyP@ssw0rd! \
  --Privilege ReadOnly

# 开启SSL加密
aliyun kvstore ModifySSLStatus --RegionId cn-hangzhou \
  --InstanceId r-xxxxxxxx \
  --SSLEnabled true

# 备份实例
aliyun kvstore CreateBackup --RegionId cn-hangzhou --InstanceId r-xxxxxxxx

# 变配
aliyun kvstore ModifyInstanceSpec --RegionId cn-hangzhou \
  --InstanceId r-xxxxxxxx \
  --InstanceClass redis.master.2x.default

# 升级小版本
aliyun kvstore ModifyInstanceMinorVersion --RegionId cn-hangzhou \
  --InstanceId r-xxxxxxxx
```

---

### MongoDB数据库

```bash
# 查询MongoDB实例列表
aliyun dds DescribeInstances --RegionId cn-hangzhou --EngineType MongoDB

# 创建MongoDB副本集实例
aliyun dds CreateDBInstance --RegionId cn-hangzhou \
  --EngineVersion 5.0 \
  --DBInstanceClass dd.mongodb.standard.v2 \
  --DBInstanceStorage 20 \
  --ZoneId cn-hangzhou-h \
  --ReplicationFactor 3

# 创建MongoDB分片集群
aliyun dds CreateShardingDBInstance --RegionId cn-hangzhou \
  --EngineVersion 5.0 \
  --MongosNodeCount 2 \
  --ShardNodeCount 2 \
  --ShardStorage 10

# 创建数据库账号
aliyun dds CreateAccount --RegionId cn-hangzhou \
  --DBInstanceId dds-xxxxxxxx \
  --AccountName myuser \
  --AccountPassword MyP@ssw0rd! \
  --DatabasePrivilege mydb:ReadWrite

# 设置白名单
aliyun dds ModifySecurityIps --RegionId cn-hangzhou \
  --DBInstanceId dds-xxxxxxxx \
  --SecurityIps "192.168.1.0/24"

# 备份实例
aliyun dds CreateBackup --RegionId cn-hangzhou \
  --DBInstanceId dds-xxxxxxxx \
  --BackupMethod Logical

# 变配
aliyun dds ModifyDBInstanceSpec --RegionId cn-hangzhou \
  --DBInstanceId dds-xxxxxxxx \
  --DBInstanceClass dd.mongodb.standard.v2
```

---

## 网络服务

### VPC专有网络

```bash
# 查询VPC列表
aliyun vpc DescribeVpcs --RegionId cn-hangzhou

# 创建VPC
aliyun vpc CreateVpc --RegionId cn-hangzhou \
  --VpcName my-vpc \
  --CidrBlock 10.0.0.0/8

# 删除VPC
aliyun vpc DeleteVpc --RegionId cn-hangzhou --VpcId vpc-xxxxxxxx

# 查询交换机列表
aliyun vpc DescribeVSwitches --RegionId cn-hangzhou --VpcId vpc-xxxxxxxx

# 创建交换机
aliyun vpc CreateVSwitch --RegionId cn-hangzhou \
  --VpcId vpc-xxxxxxxx \
  --VSwitchName my-vswitch \
  --CidrBlock 10.0.1.0/24 \
  --ZoneId cn-hangzhou-h

# 查询路由表
aliyun vpc DescribeRouteTables --RegionId cn-hangzhou --VpcId vpc-xxxxxxxx

# 创建自定义路由表
aliyun vpc CreateRouteTable --RegionId cn-hangzhou \
  --VpcId vpc-xxxxxxxx \
  --RouteTableName my-routetable

# 添加路由条目
aliyun vpc AddRouteEntry --RegionId cn-hangzhou \
  --RouteTableId vt-xxxxxxxx \
  --DestinationCidrBlock 192.168.0.0/16 \
  --NextHopType RouterInterface \
  --NextHopId ri-xxxxxxxx

# 创建NAT网关
aliyun vpc CreateNatGateway --RegionId cn-hangzhou \
  --VpcId vpc-xxxxxxxx \
  --NatGatewayName my-natgw \
  --Specification EcsMedium

# 创建弹性公网IP
aliyun vpc AllocateEipAddress --RegionId cn-hangzhou \
  --Bandwidth 100 \
  --InternetChargeType PayByBandwidth

# 绑定EIP到实例
aliyun vpc AssociateEipAddress --RegionId cn-hangzhou \
  --AllocationId eip-xxxxxxxx \
  --InstanceId i-xxxxxxxx \
  --InstanceType EcsInstance

# 解绑EIP
aliyun vpc UnassociateEipAddress --RegionId cn-hangzhou \
  --AllocationId eip-xxxxxxxx

# 查询网络ACL
aliyun vpc DescribeNetworkAcls --RegionId cn-hangzhou --VpcId vpc-xxxxxxxx

# 创建网络ACL
aliyun vpc CreateNetworkAcl --RegionId cn-hangzhou \
  --VpcId vpc-xxxxxxxx \
  --NetworkAclName my-acl

# 创建VPC对等连接
aliyun vpc CreateVpcPeerConnection --RegionId cn-hangzhou \
  --VpcId vpc-xxxxxxxx \
  --PeerVpcId vpc-yyyyyyyy \
  --Name my-peer
```

---

### SLB负载均衡

```bash
# 查询SLB实例列表
aliyun slb DescribeLoadBalancers --RegionId cn-hangzhou

# 创建公网SLB实例
aliyun slb CreateLoadBalancer --RegionId cn-hangzhou \
  --LoadBalancerName my-slb \
  --InternetChargeType paybybandwidth \
  --Bandwidth 100 \
  --LoadBalancerSpec slb.s2.small

# 创建私网SLB实例
aliyun slb CreateLoadBalancer --RegionId cn-hangzhou \
  --LoadBalancerName my-internal-slb \
  --VSwitchId vsw-xxxxxxxx \
  --AddressType intranet

# 查询SLB后端服务器
aliyun slb DescribeBackendServers --RegionId cn-hangzhou --LoadBalancerId lsb-xxxxxxxx

# 添加后端服务器
aliyun slb AddBackendServers --RegionId cn-hangzhou \
  --LoadBalancerId lsb-xxxxxxxx \
  --BackendServers '[{"ServerId":"i-xxxxxxxx","Weight":100}]'

# 创建监听
aliyun slb CreateLoadBalancerTCPListener --RegionId cn-hangzhou \
  --LoadBalancerId lsb-xxxxxxxx \
  --BackendServerPort 80 \
  --FrontendPort 80 \
  --Protocol TCP \
  --HealthCheckType tcp \
  --HealthCheckConnectTimeout 2

# 创建HTTP监听
aliyun slb CreateLoadBalancerHTTPListener --RegionId cn-hangzhou \
  --LoadBalancerId lsb-xxxxxxxx \
  --BackendServerPort 80 \
  --FrontendPort 80 \
  --Protocol HTTP \
  --XForwardedFor On

# 创建HTTPS监听
aliyun slb CreateLoadBalancerHTTPSListener --RegionId cn-hangzhou \
  --LoadBalancerId lsb-xxxxxxxx \
  --BackendServerPort 443 \
  --FrontendPort 443 \
  --Protocol HTTPS \
  --ServerCertificateId 1234abcd

# 设置白名单
aliyun slb SetLoadBalancerAcl --RegionId cn-hangzhou \
  --LoadBalancerId lsb-xxxxxxxx \
  --AclId acl-xxxxxxxx

# 查询监听健康状态
aliyun slb DescribeHealthCheckStatus --RegionId cn-hangzhou --LoadBalancerId lsb-xxxxxxxx

# 删除监听
aliyun slb DeleteLoadBalancerListener --RegionId cn-hangzhou \
  --LoadBalancerId lsb-xxxxxxxx \
  --ListenerPort 80
```

---

### NAT网关

```bash
# 创建NAT网关
aliyun vpc CreateNatGateway --RegionId cn-hangzhou \
  --VpcId vpc-xxxxxxxx \
  --NatGatewayName my-natgw \
  --Specification EcsMedium

# 创建DNAT规则（端口映射）
aliyun vpc CreateNatGatewayDnat --RegionId cn-hangzhou \
  --NatGatewayId ngw-xxxxxxxx \
  --ExternalPort 80 \
  --InternalPort 80 \
  --ExternalIp eip-xxxxxxxx \
  --InternalIp 10.0.1.10 \
  --Protocol TCP

# 创建SNAT规则（上网）
aliyun vpc CreateNatGatewaySnat --RegionId cn-hangzhou \
  --NatGatewayId ngw-xxxxxxxx \
  --SnatIp eip-xxxxxxxx \
  --SourceCIDR 10.0.1.0/24

# 查询NAT网关
aliyun vpc DescribeNatGateways --RegionId cn-hangzhou --VpcId vpc-xxxxxxxx

# 删除NAT网关
aliyun vpc DeleteNatGateway --RegionId cn-hangzhou --NatGatewayId ngw-xxxxxxxx
```

---

### CDN内容分发

```bash
# 添加加速域名
aliyun cdn AddCdnDomain --RegionId cn-hangzhou \
  --CdnDomain example.com \
  --CdnType download \
  --Sources '[{"Content":"oss.example.com","Type":"oss"}]'

# 查询加速域名
aliyun cdn DescribeCdnDomains --RegionId cn-hangzhou

# 启用/停用加速域名
aliyun cdn StartCdnDomain --RegionId cn-hangzhou --CdnDomain example.com
aliyun cdn StopCdnDomain --RegionId cn-hangzhou --CdnDomain example.com

# 配置缓存规则
aliyun cdn ModifyCacheConfig --RegionId cn-hangzhou \
  --CdnDomain example.com \
  --CacheRules '[{"RuleType":"suffix","Target":".jpg,.png","Ttl":31536000,"Weight":1}]'

# 设置Referer防盗链
aliyun cdn ModifyCdnDomainReferer --RegionId cn-hangzhou \
  --CdnDomain example.com \
  --ReferType whitelist \
  --ReferList "*.example.com,example.com"

# 配置回源请求头
aliyun cdn SetCdnDomainStagingConfig --RegionId cn-hangzhou \
  --CdnDomain example.com \
  --HeaderKey "X-CDN-Custom"

# 刷新缓存
aliyun cdn DeleteCdnCache --RegionId cn-hangzhou \
  --ObjectPath "http://example.com/index.html" \
  --ObjectType File

# 预热缓存
aliyun cdn PushCdnCache --RegionId cn-hangzhou \
  --ObjectPath "http://example.com/index.html"

# 查询流量
aliyun cdn DescribeDomainHitRate --RegionId cn-hangzhou \
  --DomainName example.com \
  --StartTime 20240501000000

# 查询带宽
aliyun cdn DescribeDomainBpsData --RegionId cn-hangzhou \
  --DomainName example.com
```

---

## 安全服务

### 安骑士Security

```bash
# 查询云盾安全体检
aliyun yundun DescribeDdosThreshold --RegionId cn-hangzhou

# 查询实例威胁详情
aliyun yundun DescribeOpenAiScreen --RegionId cn-hangzhou

# 修改安骑士配置
aliyun yundun ModifyAutoConfig --RegionId cn-hangzhou \
  --MachineGroupId 12345 \
  --EnableInternetSecurity false

# 开启恶意主机行为检测
aliyun yundun OpenBatchedThreatMachine --RegionId cn-hangzhou

# 基线检查
aliyun yundun DescribeBaseline --RegionId cn-hangzhou \
  --SourceIp 1.2.3.4

# 查询暴力破解拦截记录
aliyun yundun DescribeCrackSuccessLogs --RegionId cn-hangzhou
```

---

### 云防火墙CloudFirewall

```bash
# 查询防火墙开关状态
aliyun cloudfw DescribeFirewall --RegionId cn-hangzhou

# 开启防火墙
aliyun cloudfw OpenFirewall --RegionId cn-hangzhou

# 创建访问控制策略
aliyun cloudfw CreateAccessControlRule --RegionId cn-hangzhou \
  --Description "Allow HTTP" \
  --Action accept \
  --Protocol TCP \
  --SourceIp all \
  --DestIp all \
  --DestPort 80

# 查询访问控制策略
aliyun cloudfw DescribeControlPolicy --RegionId cn-hangzhou \
  --Direction inbound

# 开启攻击防护
aliyun cloudfw OpenDefense --RegionId cn-hangzhou \
  --DefenseType anti DDoS
```

---

### 密钥管理KMS

```bash
# 创建密钥
aliyun kms CreateKey --RegionId cn-hangzhou \
  --KeyUsage ENCRYPT/DECRYPT \
  --KeyDescription "My first key" \
  --ProtectionLevel HSM

# 列出密钥
aliyun kms ListKeys --RegionId cn-hangzhou

# 查询密钥信息
aliyun kms GetKeyMetadata --RegionId cn-hangzhou --KeyId key-xxxxxxxx

# 加密数据
aliyun kms Encrypt --RegionId cn-hangzhou \
  --KeyId key-xxxxxxxx \
  --Plaintext "SGVsbG8gV29ybGQ="

# 解密数据
aliyun kms Decrypt --RegionId cn-hangzhou \
  --KeyId key-xxxxxxxx \
  --CiphertextBlob "CiC..."

# 生成数据密钥
aliyun kms GenerateDataKey --RegionId cn-hangzhou \
  --KeyId key-xxxxxxxx \
  --NumberOfBytes 32

# 创建密钥别名
aliyun kms CreateAlias --RegionId cn-hangzhou \
  --AliasName alias/my-key \
  --KeyId key-xxxxxxxx

# 计划删除密钥
aliyun kms ScheduleKeyDeletion --RegionId cn-hangzhou \
  --KeyId key-xxxxxxxx \
  --PendingWindowInDays 7
```

---

## 中间件服务

### 消息队列MQ

```bash
# 查询Topic列表
aliyun mq QueryTopic --RegionId cn-hangzhou --TopicName test-topic

# 创建Topic
aliyun mq CreateTopic --RegionId cn-hangzhou \
  --TopicName my-topic \
  --Readability 1 \
  --Writeability 2

# 创建Group
aliyun mq CreateGroup --RegionId cn-hangzhou \
  --GroupId my-consumer-group

# 查询Group消费位点
aliyun mq GetGroupState --RegionId cn-hangzhou \
  --GroupId my-consumer-group

# 重置消费位点
aliyun mq ResetConsumeOffset --RegionId cn-hangzhou \
  --GroupId my-consumer-group \
  --Topic my-topic \
  --Time 1704067200000

# 发送消息
aliyun mq SendMessage --RegionId cn-hangzhou \
  --Topic my-topic \
  --MessageBody "Hello World"

# 查询消息
aliyun mq QueryMessage --RegionId cn-hangzhou \
  --Topic my-topic \
  --Key test-key

# 清除Topic配置
aliyun mq DeleteTopic --RegionId cn-hangzhou --TopicName my-topic
```

---

### Kafka消息队列

```bash
# 查询Kafka实例列表
aliyunalikafka DescribeInstances --RegionId cn-hangzhou

# 创建Kafka实例
aliyun alikafka CreateInstance --RegionId cn-hangzhou \
  --Name my-kafka \
  --ZoneId cn-hangzhou-h \
  --KafkaVersion 2.7.0 \
  --DiskSize 300 \
  --DiskType cloud_essd \
  --Spec ali kafka.disk.xlarge

# 创建Topic
aliyun alikafka CreateTopic --RegionId cn-hangzhou \
  --InstanceId alikafka_post-cn-xxxxx \
  --Topic my-topic \
  --Partitions 6 \
  --ReplicationFactor 3

# 查询Topic列表
aliyun alikafka DescribeTopic --RegionId cn-hangzhou \
  --InstanceId alikafka_post-cn-xxxxx

# 创建Consumer Group
aliyun alikafka CreateConsumerGroup --RegionId cn-hangzhou \
  --InstanceId alikafka_post-cn-xxxxx \
  --ConsumerGroup my-group

# 查询Consumer Group
aliyun alikafka DescribeConsumerGroup --RegionId cn-hangzhou \
  --InstanceId alikafka_post-cn-xxxxx \
  --ConsumerGroup my-group
```

---

### 分布式协调Nacos

```bash
# 查询Nacos实例列表
aliyun Nacos DescribeInstances --RegionId cn-hangzhou --InstanceId nacos-xxxxxxxx

# 创建Nacos实例
aliyun Nacos CreateInstance --RegionId cn-hangzhou \
  --InstanceName my-nacos \
  --Specification medium

# 配置服务注册中心
aliyun Nacos RegisterInstance --RegionId cn-hangzhou \
  --InstanceId nacos-xxxxxxxx \
  --ServiceName my-service \
  --Ip 10.0.1.10 \
  --Port 8848

# 查询服务列表
aliyun Nacos SelectInstances --RegionId cn-hangzhou \
  --InstanceId nacos-xxxxxxxx \
  --ServiceName my-service

# 发布配置
aliyun Nacos PublishConfig --RegionId cn-hangzhou \
  --InstanceId nacos-xxxxxxxx \
  --DataId my-config \
  --Group DEFAULT_GROUP \
  --Content "key=value"

# 查询配置
aliyun Nacos GetConfig --RegionId cn-hangzhou \
  --InstanceId nacos-xxxxxxxx \
  --DataId my-config
```

---

## 日志与监控

### 日志服务SLS

```bash
# 查询Project列表
aliyun log ListProject --RegionId cn-hangzhou

# 创建Project
aliyun log CreateProject --RegionId cn-hangzhou \
  --ProjectName my-project \
  --Description "My log project"

# 创建Logstore
aliyun log CreateLogstore --RegionId cn-hangzhou \
  --ProjectName my-project \
  --LogStoreName my-logstore \
  --TTL 30 \
  --ShardCount 2

# 查询Logstore
aliyun log ListLogStore --RegionId cn-hangzhou --ProjectName my-project

# 写入日志
aliyun log PutLogs --RegionId cn-hangzhou \
  --ProjectName my-project \
  --LogStoreName my-logstore \
  --LogStoreName my-logstore \
  --Topic test \
  --LogFile "[]"

# 查询日志
aliyun log GetLogs --RegionId cn-hangzhou \
  --ProjectName my-project \
  --LogStoreName my-logstore \
  --From 1704067200 \
  --To 1704153600 \
  --Query "status:200"

# 创建索引
aliyun log CreateIndex --RegionId cn-hangzhou \
  --ProjectName my-project \
  --LogStoreName my-logstore \
  --KeyClause '{"tokenizer":"[\" ,;]","keys":[{"Name":"status","Type":"long"}]}' \
  --LineClause ""

# 查询机器组
aliyun log ListMachineGroup --RegionId cn-hangzhou

# 创建机器组
aliyun log CreateMachineGroup --RegionId cn-hangzhou \
  --ProjectName my-project \
  --MachineGroupName my-group \
  --MachineGroupType "idips" \
  --GroupAttribute ""
```

---

### 云监控CMS

```bash
# 查询应用分组列表
aliyun cms DescribeApplicationGroups --RegionId cn-hangzhou

# 创建应用分组
aliyun cms CreateApplicationGroup --RegionId cn-hangzhou \
  --GroupName my-group \
  --TemplateIds '["11000001"]'

# 添加监控站点
aliyun cms CreateSiteMonitor --RegionId cn-hangzhou \
  --TaskName my-site \
  --TargetHost www.example.com \
  --TaskType HTTP \
  --Interval 60

# 查询监控任务
aliyun cms DescribeSiteMonitorData --RegionId cn-hangzhou \
  --TaskId 12345 \
  --StartTime 1704067200

# 创建报警规则
aliyun cms PutMonitoringConfig --RegionId cn-hangzhou \
  --GroupId 12345 \
  --RuleName "High CPU" \
  --MetricName cpu_idle \
  --Statistics Average \
  --Period 300 \
  --Threshold 30

# 查询指标列表
aliyun cms DescribeMetricMetaList --RegionId cn-hangzhou \
  --Namespace acs_ecs_disc

# 查询报警历史
aliyun cms DescribeAlertHistoryList --RegionId cn-hangzhou

# 创建仪表盘
aliyun cms CreateDashboard --RegionId cn-hangzhou \
  --DashboardName my-dashboard

# 添加图表到仪表盘
aliyun cms PutDashboard --RegionId cn-hangzhou \
  --DashboardName my-dashboard \
  --Widget '{"title":"CPU","type":"line","queries":[{"metric":"acs_ecs_disc.cpu_idle"}]}'
```

---

## 容器与编排

### 容器镜像服务ACR

```bash
# 查询镜像仓库列表
aliyun cr DescribeRepositories --RegionId cn-hangzhou --RepoName my-repo

# 创建镜像仓库
aliyun cr CreateRepository --RegionId cn-hangzhou \
  --RepoName my-repo \
  --RepoType public \
  --Summary "My repository"

# 扫描镜像漏洞
aliyun cr ScanRepository --RegionId cn-hangzhou \
  --RepoId 1234abcd \
  --Tag latest

# 查询镜像扫描结果
aliyun cr GetImageScan --RegionId cn-hangzhou \
  --RepoId 1234abcd \
  --Tag latest

# 构建镜像
aliyun cr StartBuild --RegionId cn-hangzhou --RepoId 1234abcd

# 设置访问凭证
aliyun cr GetAuthorizationToken --RegionId cn-hangzhou

# 同步镜像到其他地域
aliyun cr SyncImage --RegionId cn-hangzhou \
  --SourceRegion cn-hangzhou \
  --SourceRepoName my-repo \
  --TargetRegion cn-beijing \
  --TargetRepoName my-repo
```

---

### 企业级分布式应用EDAS

```bash
# 查询EDAS集群列表
aliyun edas GetClusterList --RegionId cn-hangzhou

# 导入ECS集群
aliyun edas InsertCluster --RegionId cn-hangzhou \
  --ClusterName my-cluster \
  --ClusterType 2 \
  --VSwitchId vsw-xxxxxxxx \
  --CIDR 10.0.0.0/16

# 查询应用列表
aliyun edas ListApp --RegionId cn-hangzhou

# 部署应用
aliyun edas DeployApplication --RegionId cn-hangzhou \
  --AppId xxxxxxxx-xxxx \
  --PackageVersion 1.0.0

# 启动应用
aliyun edas StartApplication --RegionId cn-hangzhou --AppId xxxxxxxx-xxxx

# 扩缩容
aliyun edas ScaleApplication --RegionId cn-hangzhou \
  --AppId xxxxxxxx-xxxx \
  --Replicas 5

# 查询应用实例
aliyun edas GetApplicationInstanceList --RegionId cn-hangzhou \
  --AppId xxxxxxxx-xxxx

# 创建配置
aliyun edas CreateConfig --RegionId cn-hangzhou \
  --AppId xxxxxxxx-xxxx \
  --DataId my-config \
  --Content "key=value"
```

---

## 运维与权限

### 资源管理RAM

```bash
# 创建RAM用户
aliyun ram CreateUser --RegionId cn-hangzhou \
  --UserName alice \
  --DisplayName "Alice Wang" \
  --MobilePhone "13800000000"

# 创建访问密钥
aliyun ram CreateAccessKey --RegionId cn-hangzhou --UserName alice

# 创建权限策略
aliyun ram CreatePolicy --RegionId cn-hangzhou \
  --PolicyName my-policy \
  --PolicyDocument '{"Version":"1","Statement":[{"Effect":"Allow","Action":["ecs:Describe*"],"Resource":["*"]}]}'

# 创建角色
aliyun ram CreateRole --RegionId cn-hangzhou \
  --RoleName my-role \
  --AssumeRolePolicyDocument '{"Version":"1","Statement":[{"Effect":"Allow","Principal":{"Service":["ecs.aliyuncs.com"]}}],"Action":"sts:AssumeRole"}'

# 绑定权限到用户
aliyun ram AttachPolicyToUser --RegionId cn-hangzhou \
  --UserName alice \
  --PolicyType System \
  --PolicyName AliyunECSReadOnlyAccess

# 绑定权限到角色
aliyun ram AttachPolicyToRole --RegionId cn-hangzhou \
  --RoleName my-role \
  --PolicyType System \
  --PolicyName AliyunECSFullAccess

# 查询用户权限
aliyun ram ListPoliciesForUser --RegionId cn-hangzhou --UserName alice

# 创建资源组
aliyun ram CreateResourceGroup --RegionId cn-hangzhou \
  --ResourceGroupName my-group \
  --DisplayName "My Resource Group"

# 将资源加入资源组
aliyun ram JoinResourceGroup --RegionId cn-hangzhou \
  --ResourceGroupId rg-xxxxxxxx \
  --ResourceType ecs:instance \
  --ResourceIds '["i-xxxxxxxx"]'
```

---

### 配置审计Config

```bash
# 查询资源合规列表
aliyun config ListComplianceResults --RegionId cn-hangzhou

# 查询评估结果
aliyun config GetCompliancePackResult --RegionId cn-hangzhou \
  --CompliancePackId xxxxxxxx

# 创建合规规则
aliyun config CreateConfigRule --RegionId cn-hangzhou \
  --RuleName "EBS Encryption" \
  --SourceIdentifier EBS_ENCRYPTION \
  --ConfigRuleScope '{"ResourceGroup":"rg-xxxxxxxx"}'

# 查询规则评估状态
aliyun config DescribeConfigRule --RegionId cn-hangzhou \
  --ConfigRuleId cr-xxxxxxxx

# 修正资源不合规项
aliyun config StartRemediation --RegionId cn-hangzhou \
  --ConfigRuleId cr-xxxxxxxx \
  --ResourceId i-xxxxxxxx
```

---

### 操作审计ActionTrail

```bash
# 查询跟踪列表
aliyun actiontrail DescribeTrails --RegionId cn-hangzhou

# 创建跟踪
aliyun actiontrail CreateTrail --RegionId cn-hangzhou \
  --Name my-trail \
  --TrailRegion cn-hangzhou \
  --RoleName acs:ram::xxxxx:role/aliyuntrailmanagementrole \
  --OssBucket my-bucket

# 查询事件历史
aliyun actiontrail LookupEvents --RegionId cn-hangzhou \
  --StartTime 1704067200 \
  --EndTime 1704153600 \
  --Username alice

# 查询事件概要
aliyun actiontrail DescribeEventHistograms --RegionId cn-hangzhou \
  --StartTime 1704067200

# 开启跟踪
aliyun actiontrail StartTrail --RegionId cn-hangzhou --Name my-trail

# 停止跟踪
aliyun actiontrail StopTrail --RegionId cn-hangzhou --Name my-trail
```

---

## 附录：常用产品对应关系

| 产品类别 | CLI服务名 | 控制台名称 |
|:---|:---|:---|
| 云服务器 | `ecs` | ECS |
| 容器服务 | `cs` | ACK |
| 对象存储 | `oss` | OSS |
| 文件存储 | `nas` | NAS |
| 关系型数据库 | `rds` | RDS |
| Redis数据库 | `kvstore` | Redis |
| MongoDB | `dds` | MongoDB |
| 专有网络 | `vpc` | VPC |
| 负载均衡 | `slb` | SLB |
| 内容分发 | `cdn` | CDN |
| 日志服务 | `log` | SLS |
| 云监控 | `cms` | CMS |
| 密钥管理 | `kms` | KMS |
| 资源管理 | `ram` | RAM |
| 操作审计 | `actiontrail` | ActionTrail |
| 函数计算 | `fc` | FC |
| 消息队列 | `mq` | MQ |
| Kafka | `alikafka` | Kafka |
| 镜像仓库 | `cr` | ACR |