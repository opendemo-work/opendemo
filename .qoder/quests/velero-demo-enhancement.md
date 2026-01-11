# Velero Demo 完整功能演示设计文档

## 1. 概述

### 1.1 设计目标

为opendemo-cli项目新增Velero工具的完整功能演示，覆盖Velero备份和恢复Kubernetes集群资源及持久化卷的全部核心能力。该Demo集将帮助用户系统性掌握Velero的安装、配置和使用，满足生产级容灾备份需求。

### 1.2 Demo定位

- **语言分类**: Kubernetes
- **工具名称**: velero
- **目标目录**: `opendemo_output/kubernetes/velero/`
- **难度分级**: 从beginner到advanced的完整梯度覆盖
- **受众**: Kubernetes运维人员、平台工程师、SRE

### 1.3 与现有架构的对齐

遵循项目现有的Kubernetes工具组织结构：
- 使用`kubernetes/<tool_name>/<demo_name>`的目录结构
- 每个Demo包含标准化的metadata.json、README.md和YAML资源清单
- 集成到现有的验证流程和README文档更新机制

## 2. Velero功能覆盖矩阵

### 2.1 功能分类与优先级

| 功能模块 | Demo名称 | 难度 | 核心能力 | 优先级 |
|---------|---------|-----|---------|-------|
| **安装部署** | basic-installation | beginner | Velero基础安装与MinIO配置 | P0 |
| **备份操作** | namespace-backup | beginner | 命名空间级别备份 | P0 |
| **备份操作** | cluster-backup | intermediate | 集群级别全量备份 | P0 |
| **备份操作** | scheduled-backup | intermediate | 定时备份策略配置 | P0 |
| **备份操作** | resource-filtering | intermediate | 资源过滤与标签选择器 | P1 |
| **恢复操作** | backup-restore | beginner | 基础恢复操作 | P0 |
| **恢复操作** | namespace-mapping | intermediate | 跨命名空间恢复 | P1 |
| **恢复操作** | disaster-recovery-simulation | advanced | 完整灾难恢复演练 | P1 |
| **持久卷管理** | pv-snapshot-backup | intermediate | 持久卷快照备份 | P0 |
| **持久卷管理** | volume-snapshot-location | advanced | 卷快照位置配置 | P1 |
| **高级功能** | backup-hooks | advanced | 备份前后钩子操作 | P2 |
| **高级功能** | backup-encryption | advanced | 备份数据加密 | P2 |
| **高级功能** | migration-across-clusters | advanced | 跨集群资源迁移 | P1 |
| **监控运维** | backup-monitoring | intermediate | 备份状态监控与告警 | P1 |
| **运维操作** | backup-deletion | beginner | 备份清理与保留策略 | P1 |

### 2.2 Demo数量与范围

- **计划总数**: 15个Demo
- **核心Demo(P0)**: 7个
- **扩展Demo(P1)**: 6个
- **高级Demo(P2)**: 2个

## 3. 详细Demo设计规格

### 3.1 Demo #1: basic-installation

#### 元数据定义
- **名称**: Velero基础安装与配置演示
- **难度**: beginner
- **关键字**: velero, installation, minio, backup-storage
- **描述**: 演示如何使用Helm或官方CLI安装Velero，并配置MinIO作为对象存储后端

#### 功能范围
1. MinIO对象存储部署（轻量级测试环境）
2. Velero Server端安装（Helm Chart方式）
3. Velero CLI工具安装与验证
4. BackupStorageLocation配置与连接测试
5. VolumeSnapshotLocation基础配置

#### 资源清单结构
- `minio-deployment.yaml`: MinIO服务部署
- `minio-service.yaml`: MinIO服务暴露
- `velero-values.yaml`: Helm安装配置文件
- `backup-storage-location.yaml`: 备份存储位置定义
- `credentials-secret.yaml`: 对象存储凭证（示例模板）

#### 验证点
- MinIO服务健康检查
- Velero Pod运行状态
- BackupStorageLocation连接可达性
- 执行`velero version`和`velero backup-location get`命令成功

---

### 3.2 Demo #2: namespace-backup

#### 元数据定义
- **名称**: 命名空间级别备份演示
- **难度**: beginner
- **关键字**: velero, backup, namespace, restore
- **描述**: 演示如何备份指定命名空间的所有资源并进行恢复验证

#### 功能范围
1. 创建示例应用（Nginx Deployment + Service + ConfigMap）
2. 使用`velero backup create`备份指定命名空间
3. 模拟数据丢失场景（删除命名空间）
4. 使用`velero restore create`恢复备份
5. 验证资源完整性

#### 资源清单结构
- `sample-app.yaml`: 示例应用资源定义
- `backup-spec.yaml`: 备份任务声明式定义（备选）
- `restore-spec.yaml`: 恢复任务定义（备选）

#### 关键命令示例
```bash
velero backup create nginx-backup --include-namespaces nginx-example
velero backup describe nginx-backup
velero restore create --from-backup nginx-backup
```

#### 验证点
- 备份状态为Completed
- 备份包含正确数量的资源（通过`velero backup describe`）
- 恢复后应用可正常访问
- ConfigMap数据一致性检查

---

### 3.3 Demo #3: cluster-backup

#### 元数据定义
- **名称**: 集群级别全量备份演示
- **难度**: intermediate
- **关键字**: velero, cluster-backup, full-backup, disaster-recovery
- **描述**: 演示如何执行集群级别全量备份，包括系统命名空间和CRD资源

#### 功能范围
1. 全集群资源备份（不包含kube-system等系统命名空间）
2. CRD资源自动包含
3. PersistentVolume和PVC的备份
4. 备份排除规则配置（示例排除临时资源）

#### 资源清单结构
- `cluster-backup.yaml`: 集群备份任务定义
- `backup-exclude-config.yaml`: 排除规则ConfigMap

#### 关键配置
- `--include-cluster-resources=true`
- `--exclude-namespaces`: 排除系统命名空间
- `--default-volumes-to-restic=true`: 文件级备份启用（可选）

#### 验证点
- 备份包含多个命名空间资源
- CRD被正确备份
- 备份大小合理（通过MinIO或对象存储查看）

---

### 3.4 Demo #4: scheduled-backup

#### 元数据定义
- **名称**: 定时备份策略配置演示
- **难度**: intermediate
- **关键字**: velero, schedule, cron, automated-backup
- **描述**: 演示如何创建定时备份计划，并配置备份保留策略

#### 功能范围
1. 创建基于Cron表达式的定时备份（每日、每周）
2. 配置TTL（Time-To-Live）自动清理策略
3. 查看Schedule历史和下次执行时间
4. 暂停和恢复Schedule任务

#### 资源清单结构
- `daily-backup-schedule.yaml`: 每日备份Schedule定义
- `weekly-backup-schedule.yaml`: 每周备份Schedule定义

#### Schedule配置示例
```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-backup
  namespace: velero
spec:
  schedule: "0 2 * * *"  # 每天凌晨2点
  template:
    includedNamespaces:
    - production
    ttl: 168h  # 保留7天
```

#### 验证点
- Schedule对象创建成功
- 第一次备份自动触发
- 过期备份自动删除
- 执行`velero schedule describe`查看状态

---

### 3.5 Demo #5: backup-restore

#### 元数据定义
- **名称**: 备份恢复完整流程演示
- **难度**: beginner
- **关键字**: velero, restore, recovery, validation
- **描述**: 演示完整的备份→删除→恢复流程，重点展示恢复验证方法

#### 功能范围
1. 创建包含StatefulSet的有状态应用
2. 生成测试数据（写入PV）
3. 执行备份并验证成功
4. 模拟灾难（删除应用和PVC）
5. 恢复并验证数据完整性

#### 资源清单结构
- `statefulset-mysql.yaml`: MySQL StatefulSet示例
- `mysql-pvc.yaml`: PersistentVolumeClaim定义
- `data-validation-job.yaml`: 数据验证Job

#### 恢复验证步骤
- 检查Pod状态和启动日志
- 验证PVC绑定状态
- 执行数据完整性查询
- 对比恢复前后资源版本

#### 验证点
- 恢复状态为Completed
- StatefulSet Pod数量正确
- PVC数据完整（通过checksum或查询验证）
- Service端点可访问

---

### 3.6 Demo #6: pv-snapshot-backup

#### 元数据定义
- **名称**: 持久卷快照备份演示
- **难度**: intermediate
- **关键字**: velero, volume-snapshot, csi, persistent-volume
- **描述**: 演示如何使用CSI快照功能备份持久卷数据

#### 功能范围
1. 配置VolumeSnapshotClass（使用CSI驱动）
2. 创建包含PV的应用（如PostgreSQL）
3. 启用卷快照功能进行备份
4. 验证VolumeSnapshot对象创建
5. 从快照恢复PV

#### 资源清单结构
- `volumesnapshotclass.yaml`: 快照类定义
- `postgres-statefulset.yaml`: PostgreSQL应用
- `backup-with-snapshot.yaml`: 启用快照的备份配置

#### 关键配置
```yaml
spec:
  snapshotVolumes: true
  volumeSnapshotLocations:
  - default
```

#### 验证点
- VolumeSnapshot对象在备份后创建
- 快照数据在存储后端可见
- 恢复后PV数据与原始数据一致
- 快照恢复时间可接受（记录性能指标）

---

### 3.7 Demo #7: resource-filtering

#### 元数据定义
- **名称**: 资源过滤与选择器演示
- **难度**: intermediate
- **关键字**: velero, label-selector, resource-filter, selective-backup
- **描述**: 演示如何使用标签选择器、资源类型过滤等实现精细化备份

#### 功能范围
1. 按标签选择器备份（`--selector`）
2. 按资源类型过滤（`--include-resources`）
3. 排除特定资源（`--exclude-resources`）
4. 组合过滤条件的高级用法

#### 资源清单结构
- `labeled-resources.yaml`: 带标签的多种资源
- `filtered-backup.yaml`: 过滤规则备份定义

#### 过滤规则示例
```bash
# 仅备份带有app=critical标签的资源
velero backup create critical-only --selector app=critical

# 仅备份Deployment和Service
velero backup create deploy-svc --include-resources deployments,services

# 排除Secret和ConfigMap
velero backup create no-secrets --exclude-resources secrets,configmaps
```

#### 验证点
- 备份仅包含匹配标签的资源
- 未匹配资源未被备份
- 资源类型过滤准确
- 组合条件逻辑正确

---

### 3.8 Demo #8: namespace-mapping

#### 元数据定义
- **名称**: 跨命名空间恢复映射演示
- **难度**: intermediate
- **关键字**: velero, namespace-mapping, restore, multi-tenancy
- **描述**: 演示如何将备份的资源恢复到不同的命名空间

#### 功能范围
1. 备份源命名空间资源
2. 使用`--namespace-mappings`恢复到目标命名空间
3. 处理命名空间级别资源冲突
4. 验证资源所有者引用更新

#### 资源清单结构
- `source-namespace.yaml`: 源命名空间和应用
- `restore-with-mapping.yaml`: 带映射的恢复配置

#### 映射配置示例
```yaml
spec:
  namespaceMapping:
    old-namespace: new-namespace
    prod-app: staging-app
```

#### 验证点
- 资源成功恢复到目标命名空间
- Service和Endpoint正确更新
- RBAC资源命名空间绑定正确
- 应用功能正常

---

### 3.9 Demo #9: disaster-recovery-simulation

#### 元数据定义
- **名称**: 完整灾难恢复演练
- **难度**: advanced
- **关键字**: velero, disaster-recovery, rto, rpo, failover
- **描述**: 模拟完整的灾难场景（集群故障），演示灾难恢复的完整流程

#### 功能范围
1. 模拟生产环境多服务集群
2. 定期备份策略配置
3. 模拟灾难（删除关键命名空间）
4. 灾难恢复流程执行
5. RTO/RPO指标测量

#### 资源清单结构
- `production-workloads.yaml`: 模拟生产应用
- `dr-backup-schedule.yaml`: 灾备备份计划
- `dr-restore-playbook.yaml`: 恢复手册（文档形式）

#### 灾难恢复步骤
1. 检测灾难并触发恢复
2. 验证备份存储可访问性
3. 执行最新备份的恢复
4. 验证关键服务健康检查
5. 切换流量到恢复后的服务
6. 记录恢复时间和数据丢失窗口

#### 验证点
- RTO < 30分钟（示例目标）
- RPO < 1小时（基于备份频率）
- 恢复后所有服务可访问
- 数据一致性验证通过

---

### 3.10 Demo #10: backup-hooks

#### 元数据定义
- **名称**: 备份钩子操作演示
- **难度**: advanced
- **关键字**: velero, hooks, pre-backup, post-backup, database-consistency
- **描述**: 演示如何使用备份钩子在备份前后执行自定义操作（如数据库一致性检查）

#### 功能范围
1. Pre-backup hook（备份前执行数据库flush）
2. Post-backup hook（备份后验证）
3. 基于Annotation的Pod级别钩子
4. 钩子执行失败处理策略

#### 资源清单结构
- `mysql-with-hooks.yaml`: 带钩子的MySQL部署
- `backup-with-hooks.yaml`: 带钩子配置的备份

#### 钩子配置示例
```yaml
metadata:
  annotations:
    pre.hook.backup.velero.io/command: '["/bin/bash", "-c", "mysql -e \"FLUSH TABLES WITH READ LOCK\""]'
    pre.hook.backup.velero.io/timeout: 30s
    post.hook.backup.velero.io/command: '["/bin/bash", "-c", "mysql -e \"UNLOCK TABLES\""]'
```

#### 验证点
- Pre-backup钩子执行日志
- 数据库在备份期间的锁状态
- Post-backup钩子成功解锁
- 备份数据一致性验证

---

### 3.11 Demo #11: backup-encryption

#### 元数据定义
- **名称**: 备份数据加密演示
- **难度**: advanced
- **关键字**: velero, encryption, security, kms, sensitive-data
- **描述**: 演示如何启用备份数据加密，保护敏感资源

#### 功能范围
1. 配置加密密钥（使用Kubernetes Secret）
2. 启用客户端加密功能
3. 验证对象存储中的加密数据
4. 使用密钥恢复加密备份

#### 资源清单结构
- `encryption-secret.yaml`: 加密密钥Secret
- `encrypted-backup-location.yaml`: 启用加密的存储位置
- `encrypted-backup.yaml`: 加密备份配置

#### 加密配置
- 使用AES-256-GCM加密算法
- 密钥轮换策略说明
- 密钥管理最佳实践

#### 验证点
- 对象存储中的备份文件已加密（无法直接读取）
- 使用正确密钥可成功恢复
- 使用错误密钥恢复失败
- 加密对性能的影响可接受

---

### 3.12 Demo #12: migration-across-clusters

#### 元数据定义
- **名称**: 跨集群资源迁移演示
- **难度**: advanced
- **关键字**: velero, cluster-migration, multi-cluster, workload-portability
- **描述**: 演示如何使用Velero在不同Kubernetes集群间迁移工作负载

#### 功能范围
1. 源集群备份配置
2. 目标集群Velero安装并配置相同对象存储
3. 跨集群资源恢复
4. 处理集群特定资源（如StorageClass）
5. 验证迁移后的应用功能

#### 资源清单结构
- `source-cluster-backup.yaml`: 源集群备份
- `target-cluster-restore.yaml`: 目标集群恢复
- `cluster-specific-mappings.yaml`: 集群特定资源映射

#### 迁移步骤
1. 在源集群执行备份
2. 确保目标集群Velero配置相同BackupStorageLocation
3. 在目标集群同步备份元数据
4. 执行恢复并处理资源冲突
5. 更新DNS或负载均衡器指向

#### 验证点
- 应用在目标集群成功运行
- PV数据成功迁移
- Service和Ingress正确配置
- 无需修改应用配置

---

### 3.13 Demo #13: backup-monitoring

#### 元数据定义
- **名称**: 备份状态监控与告警演示
- **难度**: intermediate
- **关键字**: velero, monitoring, prometheus, alerting, metrics
- **描述**: 演示如何监控Velero备份任务状态并配置告警规则

#### 功能范围
1. 启用Velero Prometheus metrics
2. 配置ServiceMonitor（Prometheus Operator）
3. 创建备份失败告警规则
4. Grafana仪表板展示（可选）
5. 备份状态查询和日志分析

#### 资源清单结构
- `servicemonitor.yaml`: Prometheus监控配置
- `prometheus-rules.yaml`: 备份告警规则
- `grafana-dashboard.json`: Grafana仪表板（可选）

#### 关键指标
- `velero_backup_success_total`: 成功备份总数
- `velero_backup_failure_total`: 失败备份总数
- `velero_backup_duration_seconds`: 备份耗时
- `velero_backup_last_successful_timestamp`: 最后成功时间

#### 告警规则示例
```yaml
- alert: VeleroBackupFailure
  expr: increase(velero_backup_failure_total[1h]) > 0
  annotations:
    summary: "Velero backup failed"
```

#### 验证点
- Prometheus成功抓取Velero metrics
- 告警规则触发测试
- 仪表板显示备份历史趋势
- 日志集成到日志聚合平台

---

### 3.14 Demo #14: volume-snapshot-location

#### 元数据定义
- **名称**: 卷快照位置配置演示
- **难度**: advanced
- **关键字**: velero, volume-snapshot-location, csi, snapshot-provider
- **描述**: 演示如何配置多个VolumeSnapshotLocation以支持不同存储提供商

#### 功能范围
1. 配置默认VolumeSnapshotLocation
2. 配置多个快照位置（如AWS EBS、Azure Disk）
3. 备份时指定快照位置
4. 快照位置的可用性检查

#### 资源清单结构
- `default-vsl.yaml`: 默认快照位置
- `aws-ebs-vsl.yaml`: AWS EBS快照位置
- `azure-disk-vsl.yaml`: Azure Disk快照位置

#### 配置示例（AWS EBS）
```yaml
apiVersion: velero.io/v1
kind: VolumeSnapshotLocation
metadata:
  name: aws-ebs
  namespace: velero
spec:
  provider: aws
  config:
    region: us-west-2
```

#### 验证点
- 多个VolumeSnapshotLocation对象创建成功
- 备份时可选择特定快照位置
- 快照存储在对应的提供商后端
- 跨区域快照复制验证（高级场景）

---

### 3.15 Demo #15: backup-deletion

#### 元数据定义
- **名称**: 备份清理与保留策略演示
- **难度**: beginner
- **关键字**: velero, backup-deletion, retention-policy, storage-management
- **描述**: 演示如何手动删除备份、配置自动清理策略和管理对象存储空间

#### 功能范围
1. 手动删除单个备份
2. 批量删除过期备份
3. 配置TTL自动清理
4. 验证对象存储空间释放
5. 删除保护机制说明

#### 资源清单结构
- `ttl-backup.yaml`: 带TTL的备份定义
- `cleanup-job.yaml`: 清理脚本Job（可选）

#### 删除命令示例
```bash
# 删除单个备份
velero backup delete old-backup

# 删除所有Completed状态的备份
velero backup delete --selector velero.io/phase=Completed

# 查看即将过期的备份
velero backup get --show-labels
```

#### TTL配置
```yaml
spec:
  ttl: 720h  # 30天后自动删除
```

#### 验证点
- 执行删除后备份对象消失
- 对象存储中的备份文件被删除
- TTL到期后备份自动清理
- 删除操作记录在审计日志中

---

## 4. 测试用例设计

### 4.1 测试用例分类

| 测试类别 | 测试目标 | 覆盖Demo |
|---------|---------|---------|
| **安装验证** | Velero组件正常安装 | #1 |
| **功能正确性** | 备份和恢复功能正常 | #2, #3, #5, #6 |
| **策略配置** | 定时任务和过滤规则生效 | #4, #7 |
| **高级场景** | 钩子、加密、跨集群功能 | #10, #11, #12 |
| **运维监控** | 监控指标和告警正常 | #13 |
| **数据一致性** | 恢复后数据完整无损 | #5, #6, #9 |

### 4.2 测试用例详细规格

#### TC-001: Velero基础安装验证
- **对应Demo**: #1 basic-installation
- **前置条件**: 
  - Kubernetes集群可用（minikube或云厂商集群）
  - kubectl已配置并可访问集群
  - Helm 3+已安装
- **测试步骤**:
  1. 执行MinIO部署YAML
  2. 验证MinIO Pod状态为Running
  3. 使用Helm安装Velero（提供values文件）
  4. 检查Velero Pod状态
  5. 执行`velero version`命令
  6. 执行`velero backup-location get`验证存储连接
- **期望结果**:
  - 所有Pod状态为Running
  - Velero CLI输出server和client版本一致
  - BackupStorageLocation状态为Available
- **失败处理**: 查看Pod日志，检查凭证配置是否正确

#### TC-002: 命名空间备份与恢复
- **对应Demo**: #2 namespace-backup
- **前置条件**: 
  - Velero已成功安装（TC-001通过）
  - 存在测试命名空间和示例应用
- **测试步骤**:
  1. 创建nginx-example命名空间和应用
  2. 写入测试数据到ConfigMap
  3. 执行备份命令：`velero backup create test-backup --include-namespaces nginx-example`
  4. 等待备份完成（检查状态为Completed）
  5. 删除nginx-example命名空间
  6. 执行恢复命令：`velero restore create --from-backup test-backup`
  7. 验证命名空间和资源恢复
- **期望结果**:
  - 备份状态显示Completed
  - 恢复后命名空间存在
  - 应用Pod正常运行
  - ConfigMap数据与备份前一致
- **数据验证**: 使用checksum或kubectl diff对比资源

#### TC-003: 持久卷快照功能
- **对应Demo**: #6 pv-snapshot-backup
- **前置条件**:
  - 集群支持CSI快照功能
  - VolumeSnapshotClass已配置
- **测试步骤**:
  1. 部署带PVC的StatefulSet应用
  2. 写入测试文件到PV（例如：`echo "test-data" > /data/test.txt`）
  3. 创建启用快照的备份
  4. 验证VolumeSnapshot对象创建
  5. 删除应用和PVC
  6. 从备份恢复
  7. 验证文件内容一致
- **期望结果**:
  - VolumeSnapshot对象存在且状态为ReadyToUse
  - 恢复后PV挂载成功
  - 文件内容匹配
- **性能指标**: 记录快照创建和恢复时间

#### TC-004: 定时备份任务
- **对应Demo**: #4 scheduled-backup
- **前置条件**: 
  - Velero已安装
  - 存在需要定期备份的命名空间
- **测试步骤**:
  1. 创建Schedule对象（cron表达式设置为每5分钟）
  2. 等待第一次备份触发
  3. 检查自动创建的Backup对象
  4. 修改应用并等待第二次备份
  5. 验证两次备份都成功
  6. 检查TTL策略（设置为10分钟）
  7. 等待过期备份自动删除
- **期望结果**:
  - Schedule对象显示下次执行时间
  - 每次定时触发都成功创建Backup
  - 过期备份被自动清理
- **监控验证**: 查看Prometheus metrics中的备份计数器

#### TC-005: 资源过滤与选择器
- **对应Demo**: #7 resource-filtering
- **前置条件**: 
  - 命名空间中存在多种标签的资源
- **测试步骤**:
  1. 创建带有不同标签的资源（app=critical和app=test）
  2. 执行带标签选择器的备份：`--selector app=critical`
  3. 检查备份描述中的资源列表
  4. 验证仅critical标签的资源被备份
  5. 执行资源类型过滤：`--include-resources deployments,services`
  6. 验证仅指定类型被备份
- **期望结果**:
  - 备份中仅包含匹配标签的资源
  - 未匹配资源不在备份中
  - 资源计数符合预期
- **验证方法**: 使用`velero backup describe --details`查看资源列表

#### TC-006: 跨集群资源迁移
- **对应Demo**: #12 migration-across-clusters
- **前置条件**:
  - 两个独立的Kubernetes集群
  - 两个集群的Velero配置相同的对象存储
- **测试步骤**:
  1. 在源集群创建应用和数据
  2. 在源集群执行备份
  3. 验证备份上传到共享对象存储
  4. 在目标集群安装Velero（相同配置）
  5. 在目标集群执行`velero backup get`同步备份
  6. 执行恢复操作
  7. 验证应用在目标集群正常运行
- **期望结果**:
  - 应用在目标集群功能正常
  - PV数据迁移成功
  - 无需修改应用配置
- **网络验证**: 测试Service和Ingress是否可访问

#### TC-007: 备份钩子执行
- **对应Demo**: #10 backup-hooks
- **前置条件**:
  - 部署支持钩子的应用（如MySQL）
- **测试步骤**:
  1. 配置pre-backup钩子（数据库flush）
  2. 执行备份
  3. 查看Pod日志验证钩子执行
  4. 验证post-backup钩子执行
  5. 恢复备份并验证数据一致性
- **期望结果**:
  - 钩子命令在日志中可见
  - 数据库一致性检查通过
  - 备份期间应用短暂只读
- **失败场景**: 测试钩子超时和失败处理

#### TC-008: 备份数据加密
- **对应Demo**: #11 backup-encryption
- **前置条件**:
  - 准备加密密钥Secret
- **测试步骤**:
  1. 配置启用加密的BackupStorageLocation
  2. 创建包含敏感数据的资源（Secret）
  3. 执行加密备份
  4. 检查对象存储中的备份文件（应无法直接读取）
  5. 使用正确密钥恢复备份
  6. 测试使用错误密钥恢复（应失败）
- **期望结果**:
  - 对象存储中的备份文件已加密
  - 正确密钥可恢复
  - 错误密钥恢复失败并有明确错误提示
- **安全验证**: 使用hex编辑器检查备份文件无明文

#### TC-009: 灾难恢复演练
- **对应Demo**: #9 disaster-recovery-simulation
- **前置条件**:
  - 模拟生产环境应用运行
  - 定时备份策略已配置
- **测试步骤**:
  1. 记录灾难前的应用状态和数据
  2. 模拟灾难（删除关键命名空间）
  3. 记录检测到灾难的时间（T0）
  4. 执行灾难恢复流程
  5. 记录恢复完成时间（T1）
  6. 验证应用功能和数据完整性
  7. 计算RTO和RPO
- **期望结果**:
  - RTO（T1-T0）< 30分钟
  - RPO（数据丢失）< 1小时（基于备份频率）
  - 所有关键服务恢复
  - 数据一致性验证通过
- **性能记录**: 记录每个步骤的耗时

#### TC-010: 备份监控与告警
- **对应Demo**: #13 backup-monitoring
- **前置条件**:
  - Prometheus Operator已安装
  - Grafana已安装（可选）
- **测试步骤**:
  1. 应用ServiceMonitor配置
  2. 验证Prometheus抓取Velero metrics
  3. 查询备份成功和失败计数器
  4. 触发备份失败场景（如存储不可用）
  5. 验证告警触发
  6. 导入Grafana仪表板（可选）
- **期望结果**:
  - Metrics端点可访问
  - Prometheus成功抓取数据
  - 告警规则在失败时触发
  - 仪表板显示备份趋势
- **集成验证**: 测试告警发送到钉钉/Slack

---

### 4.3 自动化测试脚本设计

每个Demo的`code/`目录下提供自动化测试脚本：

#### 脚本结构（示例：test-backup.sh）
```bash
#!/bin/bash
# 自动化测试脚本：命名空间备份与恢复

set -e  # 遇到错误立即退出

# 步骤1: 创建测试命名空间
kubectl create namespace test-backup-ns

# 步骤2: 部署示例应用
kubectl apply -f sample-app.yaml -n test-backup-ns

# 步骤3: 等待应用就绪
kubectl wait --for=condition=Ready pod -l app=nginx -n test-backup-ns --timeout=60s

# 步骤4: 执行备份
velero backup create test-backup --include-namespaces test-backup-ns

# 步骤5: 等待备份完成
while [[ $(velero backup describe test-backup -o json | jq -r '.status.phase') != "Completed" ]]; do
  echo "等待备份完成..."
  sleep 5
done

# 步骤6: 验证备份
RESOURCE_COUNT=$(velero backup describe test-backup --details | grep -c "Deployment\|Service")
if [ "$RESOURCE_COUNT" -lt 2 ]; then
  echo "❌ 备份资源数量不足"
  exit 1
fi

# 步骤7: 删除命名空间
kubectl delete namespace test-backup-ns

# 步骤8: 恢复备份
velero restore create --from-backup test-backup

# 步骤9: 验证恢复
kubectl wait --for=condition=Ready pod -l app=nginx -n test-backup-ns --timeout=120s

echo "✅ 测试通过：备份和恢复成功"

# 清理
velero backup delete test-backup --confirm
kubectl delete namespace test-backup-ns
```

#### 测试脚本规范
- 使用`set -e`确保错误时退出
- 每个步骤添加日志输出
- 使用`kubectl wait`等待资源就绪
- 验证点使用条件判断和明确的成功/失败提示
- 测试结束清理所有资源
- 支持幂等执行（可重复运行）

---

## 5. 测试报告规格

### 5.1 测试报告模板

#### 报告文件位置
每个Demo的根目录下生成`TEST_REPORT.md`文件。

#### 报告内容结构

```markdown
# Velero Demo测试报告

## 测试概要

| 项目 | 值 |
|-----|---|
| Demo名称 | {demo_name} |
| 测试日期 | {date} |
| 测试环境 | Kubernetes {version}, Velero {version} |
| 测试执行者 | {executor} |
| 测试结果 | ✅ 通过 / ❌ 失败 |

## 测试用例执行结果

| 用例ID | 用例名称 | 状态 | 耗时 | 备注 |
|-------|---------|------|-----|------|
| TC-001 | 安装验证 | ✅ 通过 | 120s | - |
| TC-002 | 备份执行 | ✅ 通过 | 45s | - |
| TC-003 | 恢复验证 | ✅ 通过 | 90s | - |

## 详细测试日志

### TC-001: 安装验证

**执行步骤**:
1. 部署MinIO: 成功
2. 安装Velero: 成功
3. 验证连接: 成功

**执行输出**:
```
Client:
        Version: v1.12.0
Server:
        Version: v1.12.0
```

**验证结果**: ✅ 通过

---

## 性能指标

| 指标 | 值 | 目标 | 结果 |
|-----|---|------|------|
| 备份耗时 | 45s | < 60s | ✅ |
| 恢复耗时 | 90s | < 120s | ✅ |
| 数据一致性 | 100% | 100% | ✅ |

## 问题与风险

### 发现的问题
- 无

### 风险评估
- **风险**: CSI快照依赖存储插件支持
- **缓解措施**: 文档中明确CSI要求

## 测试环境信息

```yaml
Kubernetes版本: v1.28.0
Velero版本: v1.12.0
对象存储: MinIO (模拟S3)
存储插件: CSI hostpath
节点数量: 1 (minikube)
```

## 测试结论

本次测试覆盖了Velero的核心功能，所有测试用例均通过验证。Demo可用于生产参考。

**建议**: 在生产环境应使用云厂商的对象存储服务（如AWS S3）替代MinIO。
```

---

### 5.2 自动化报告生成

#### 脚本：generate-test-report.sh
```bash
#!/bin/bash
# 生成测试报告脚本

DEMO_NAME=$1
REPORT_FILE="TEST_REPORT.md"

# 执行测试并捕获输出
TEST_OUTPUT=$(./code/test-*.sh 2>&1)
TEST_RESULT=$?

# 记录测试时间
START_TIME=$(date -Iseconds)
# ... 执行测试 ...
END_TIME=$(date -Iseconds)
DURATION=$((END_TIME - START_TIME))

# 生成报告
cat > $REPORT_FILE <<EOF
# Velero Demo测试报告

## 测试概要

| 项目 | 值 |
|-----|---|
| Demo名称 | $DEMO_NAME |
| 测试日期 | $(date) |
| 测试结果 | $([ $TEST_RESULT -eq 0 ] && echo "✅ 通过" || echo "❌ 失败") |
| 测试耗时 | ${DURATION}s |

## 测试输出

\`\`\`
$TEST_OUTPUT
\`\`\`

EOF

echo "测试报告已生成: $REPORT_FILE"
```

---

## 6. README文档更新规格

### 6.1 README.md更新内容

在主README中的Kubernetes章节添加Velero工具清单：

#### 更新位置
在`⎈ Kubernetes`部分，kubeflow、kubeskoop之后新增velero。

#### 更新内容格式
```markdown
<details>
<summary><b>📦 Velero工具 (15个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/velero/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-installation` | Velero基础安装与配置 | beginner | ✅ |
| 2 | `namespace-backup` | 命名空间级别备份 | beginner | ✅ |
| 3 | `cluster-backup` | 集群级别全量备份 | intermediate | ✅ |
| 4 | `scheduled-backup` | 定时备份策略配置 | intermediate | ✅ |
| 5 | `resource-filtering` | 资源过滤与标签选择器 | intermediate | ✅ |
| 6 | `backup-restore` | 备份恢复完整流程 | beginner | ✅ |
| 7 | `namespace-mapping` | 跨命名空间恢复映射 | intermediate | ✅ |
| 8 | `disaster-recovery-simulation` | 完整灾难恢复演练 | advanced | ✅ |
| 9 | `pv-snapshot-backup` | 持久卷快照备份 | intermediate | ✅ |
| 10 | `volume-snapshot-location` | 卷快照位置配置 | advanced | ✅ |
| 11 | `backup-hooks` | 备份前后钩子操作 | advanced | ✅ |
| 12 | `backup-encryption` | 备份数据加密 | advanced | ✅ |
| 13 | `migration-across-clusters` | 跨集群资源迁移 | advanced | ✅ |
| 14 | `backup-monitoring` | 备份状态监控与告警 | intermediate | ✅ |
| 15 | `backup-deletion` | 备份清理与保留策略 | beginner | ✅ |

**功能覆盖**:
- ✅ 安装部署与基础配置
- ✅ 命名空间和集群级别备份
- ✅ 定时备份与保留策略
- ✅ 持久卷快照与数据恢复
- ✅ 灾难恢复与跨集群迁移
- ✅ 备份钩子与数据加密
- ✅ 监控告警与运维管理

</details>
```

### 6.2 Demo统计表更新

更新主README顶部的统计表：

```markdown
| 语言 | 基础Demo | 第三方库/工具 | 总计 | 测试状态 |
|---------|----------|----------|------|----------|
| ⎈ **Kubernetes** | 0 | kubeflow(42), kubeskoop(10), velero(15), operator-framework(2) | 69 | ✅ 全部通过 |
| **总计** | **210** | **96** | **306** | ✅ |
```

### 6.3 STATUS.md文件更新

如果项目存在STATUS.md跟踪功能状态，应添加：

```markdown
## Velero工具支持 (v1.0.0)

- [x] 基础安装与配置
- [x] 命名空间备份与恢复
- [x] 集群级别备份
- [x] 定时备份策略
- [x] 持久卷快照
- [x] 灾难恢复演练
- [x] 跨集群迁移
- [x] 备份加密
- [x] 监控告警集成
- [x] 完整测试覆盖
```

---

## 7. 实施计划

### 7.1 开发阶段

#### 阶段1: 核心功能Demo (P0优先级)
**时间**: 第1周
- 开发Demo #1: basic-installation
- 开发Demo #2: namespace-backup
- 开发Demo #3: cluster-backup
- 开发Demo #4: scheduled-backup
- 开发Demo #5: backup-restore
- 开发Demo #6: pv-snapshot-backup
- 开发Demo #15: backup-deletion

**交付物**: 7个核心Demo，每个包含完整的README、YAML和测试脚本

#### 阶段2: 扩展功能Demo (P1优先级)
**时间**: 第2周
- 开发Demo #7: resource-filtering
- 开发Demo #8: namespace-mapping
- 开发Demo #9: disaster-recovery-simulation
- 开发Demo #13: backup-monitoring
- 开发Demo #12: migration-across-clusters
- 开发Demo #14: volume-snapshot-location

**交付物**: 6个扩展Demo

#### 阶段3: 高级功能Demo (P2优先级)
**时间**: 第3周
- 开发Demo #10: backup-hooks
- 开发Demo #11: backup-encryption

**交付物**: 2个高级Demo

### 7.2 测试与验证阶段

#### 阶段4: 集成测试
**时间**: 第3周
- 执行所有15个Demo的测试用例
- 生成测试报告
- 修复发现的问题
- 性能基准测试

#### 阶段5: 文档完善
**时间**: 第4周
- 完善每个Demo的README
- 生成统一的测试报告汇总
- 更新主README.md
- 更新STATUS.md

### 7.3 交付清单

#### 最终交付物
1. **15个Velero Demo**，每个包含：
   - `metadata.json`: 元数据文件
   - `README.md`: 详细使用文档
   - `code/`: YAML资源清单和测试脚本
   - `TEST_REPORT.md`: 测试报告

2. **文档更新**：
   - 主`README.md`添加Velero章节
   - 统计数据更新（306个Demo）
   - `STATUS.md`功能跟踪更新

3. **测试报告**：
   - 每个Demo的独立测试报告
   - 汇总测试报告（覆盖率、通过率）

4. **CI集成**（可选）：
   - GitHub Actions工作流验证Demo
   - 自动化测试执行

---

## 8. 验证标准

### 8.1 Demo质量标准

每个Demo必须满足以下标准才能交付：

#### 文档完整性
- [x] README.md包含完整的功能说明
- [x] 环境要求明确（Kubernetes版本、工具依赖）
- [x] 逐步实操指南清晰
- [x] 代码解析和预期输出完整
- [x] 常见问题FAQ覆盖

#### 资源清单质量
- [x] 所有YAML文件语法正确（通过验证器）
- [x] 资源定义遵循最佳实践
- [x] 包含必要的注释和说明
- [x] 命名空间隔离（避免冲突）

#### 测试覆盖
- [x] 提供自动化测试脚本
- [x] 测试脚本幂等且可重复执行
- [x] 验证点明确（成功/失败判断）
- [x] 测试报告自动生成

#### 验证机制对齐
- [x] 通过`demo_verifier.py`的Kubernetes验证逻辑
- [x] 静态YAML语法检查通过
- [x] kubectl和helm工具可用性检查
- [x] Dry-run验证通过（如适用）

### 8.2 集成验证流程

#### 自动化验证步骤
1. **静态检查**: 验证所有YAML文件语法
2. **元数据验证**: 检查metadata.json格式和必填字段
3. **文档检查**: README.md存在且包含关键章节
4. **测试执行**: 运行测试脚本并记录结果
5. **性能检查**: 记录备份和恢复耗时

#### 验证通过标准
- 所有静态检查无错误
- 测试脚本执行成功（退出码0）
- 测试报告显示所有用例通过
- 性能指标在可接受范围内

---

## 9. 风险与缓解措施

### 9.1 技术风险

| 风险 | 影响 | 概率 | 缓解措施 |
|-----|-----|------|---------|
| CSI快照功能依赖存储插件 | 部分Demo无法在所有环境运行 | 中 | 文档明确环境要求；提供备选方案（Restic文件备份） |
| 对象存储配置复杂度 | 用户安装难度大 | 中 | 提供MinIO快速部署方案；多云厂商配置示例 |
| Velero版本兼容性 | 不同版本行为差异 | 低 | 明确测试版本；提供多版本兼容性说明 |
| 跨集群迁移需要多集群环境 | 测试复杂度高 | 中 | 提供minikube多实例方案；云厂商测试集群 |

### 9.2 运维风险

| 风险 | 影响 | 概率 | 缓解措施 |
|-----|-----|------|---------|
| 备份数据占用大量存储 | 成本增加 | 高 | 文档说明TTL策略；提供存储空间监控方案 |
| 恢复时间超出预期 | RTO目标无法满足 | 中 | 性能基准测试；提供优化建议 |
| 加密密钥丢失导致数据不可恢复 | 数据永久丢失 | 低 | 文档强调密钥管理重要性；提供密钥备份方案 |

### 9.3 项目集成风险

| 风险 | 影响 | 概率 | 缓解措施 |
|-----|-----|------|---------|
| Demo结构与现有不一致 | 集成失败 | 低 | 严格遵循kubernetes/<tool>/<demo>结构 |
| 验证流程未覆盖新场景 | CI失败 | 中 | 扩展demo_verifier.py支持Velero特定验证 |
| 文档更新冲突 | 合并问题 | 低 | 预先协调README更新位置 |

---

## 10. 成功标准

### 10.1 功能完整性
- [x] 覆盖Velero官方文档中的核心功能（备份、恢复、定时任务、快照）
- [x] 提供beginner到advanced的完整难度梯度
- [x] 每个功能点至少有一个Demo演示

### 10.2 质量标准
- [x] 所有15个Demo通过自动化验证
- [x] 测试覆盖率达到100%（每个Demo有对应测试用例）
- [x] 文档完整性检查通过（README、metadata、TEST_REPORT）

### 10.3 用户体验
- [x] 用户可通过`opendemo get kubernetes velero`命令列出所有Demo
- [x] 每个Demo可独立运行（依赖明确）
- [x] 平均10分钟内完成单个Demo的部署和验证

### 10.4 社区影响
- [x] README中Kubernetes Demo数量从54增加到69
- [x] 提供生产级灾备方案参考
- [x] 社区用户反馈评分≥4.5/5（如适用）

---

## 11. 附录

### 11.1 Velero架构参考

Velero由以下组件构成：
- **Server**: 运行在Kubernetes集群中的控制器（Deployment）
- **CLI**: 用户命令行工具（velero命令）
- **Plugins**: 对象存储和卷快照插件（AWS、Azure、GCP等）
- **Restic**: 可选的文件级备份工具（集成在Server中）

### 11.2 对象存储后端支持

| 存储类型 | 插件 | Demo中的使用 |
|---------|-----|-------------|
| AWS S3 | velero-plugin-for-aws | 文档中提供配置示例 |
| Azure Blob | velero-plugin-for-microsoft-azure | 文档中提供配置示例 |
| GCP Storage | velero-plugin-for-gcp | 文档中提供配置示例 |
| MinIO | S3兼容API | Demo中默认使用（测试环境） |

### 11.3 参考资料
- Velero官方文档: https://velero.io/docs/
- Velero GitHub仓库: https://github.com/vmware-tanzu/velero
- CSI快照规范: https://kubernetes.io/docs/concepts/storage/volume-snapshots/
- 项目现有Kubernetes Demo: `opendemo_output/kubernetes/kubeskoop/`
| **持久卷管理** | volume-snapshot-location | advanced | 卷快照位置配置 | P1 |
| **高级功能** | backup-hooks | advanced | 备份前后钩子操作 | P2 |
| **高级功能** | backup-encryption | advanced | 备份数据加密 | P2 |
| **高级功能** | migration-across-clusters | advanced | 跨集群资源迁移 | P1 |
| **监控运维** | backup-monitoring | intermediate | 备份状态监控与告警 | P1 |
| **运维操作** | backup-deletion | beginner | 备份清理与保留策略 | P1 |

### 2.2 Demo数量与范围

- **计划总数**: 15个Demo
- **核心Demo(P0)**: 7个
- **扩展Demo(P1)**: 6个
- **高级Demo(P2)**: 2个

## 3. 详细Demo设计规格

### 3.1 Demo #1: basic-installation

#### 元数据定义
- **名称**: Velero基础安装与配置演示
- **难度**: beginner
- **关键字**: velero, installation, minio, backup-storage
- **描述**: 演示如何使用Helm或官方CLI安装Velero，并配置MinIO作为对象存储后端

#### 功能范围
1. MinIO对象存储部署（轻量级测试环境）
2. Velero Server端安装（Helm Chart方式）
3. Velero CLI工具安装与验证
4. BackupStorageLocation配置与连接测试
5. VolumeSnapshotLocation基础配置

#### 资源清单结构
- `minio-deployment.yaml`: MinIO服务部署
- `minio-service.yaml`: MinIO服务暴露
- `velero-values.yaml`: Helm安装配置文件
- `backup-storage-location.yaml`: 备份存储位置定义
- `credentials-secret.yaml`: 对象存储凭证（示例模板）

#### 验证点
- MinIO服务健康检查
- Velero Pod运行状态
- BackupStorageLocation连接可达性
- 执行`velero version`和`velero backup-location get`命令成功

---

### 3.2 Demo #2: namespace-backup

#### 元数据定义
- **名称**: 命名空间级别备份演示
- **难度**: beginner
- **关键字**: velero, backup, namespace, restore
- **描述**: 演示如何备份指定命名空间的所有资源并进行恢复验证

#### 功能范围
1. 创建示例应用（Nginx Deployment + Service + ConfigMap）
2. 使用`velero backup create`备份指定命名空间
3. 模拟数据丢失场景（删除命名空间）
4. 使用`velero restore create`恢复备份
5. 验证资源完整性

#### 资源清单结构
- `sample-app.yaml`: 示例应用资源定义
- `backup-spec.yaml`: 备份任务声明式定义（备选）
- `restore-spec.yaml`: 恢复任务定义（备选）

#### 关键命令示例
```bash
velero backup create nginx-backup --include-namespaces nginx-example
velero backup describe nginx-backup
velero restore create --from-backup nginx-backup
```

#### 验证点
- 备份状态为Completed
- 备份包含正确数量的资源（通过`velero backup describe`）
- 恢复后应用可正常访问
- ConfigMap数据一致性检查

---

### 3.3 Demo #3: cluster-backup

#### 元数据定义
- **名称**: 集群级别全量备份演示
- **难度**: intermediate
- **关键字**: velero, cluster-backup, full-backup, disaster-recovery
- **描述**: 演示如何执行集群级别全量备份，包括系统命名空间和CRD资源

#### 功能范围
1. 全集群资源备份（不包含kube-system等系统命名空间）
2. CRD资源自动包含
3. PersistentVolume和PVC的备份
4. 备份排除规则配置（示例排除临时资源）

#### 资源清单结构
- `cluster-backup.yaml`: 集群备份任务定义
- `backup-exclude-config.yaml`: 排除规则ConfigMap

#### 关键配置
- `--include-cluster-resources=true`
- `--exclude-namespaces`: 排除系统命名空间
- `--default-volumes-to-restic=true`: 文件级备份启用（可选）

#### 验证点
- 备份包含多个命名空间资源
- CRD被正确备份
- 备份大小合理（通过MinIO或对象存储查看）

---

### 3.4 Demo #4: scheduled-backup

#### 元数据定义
- **名称**: 定时备份策略配置演示
- **难度**: intermediate
- **关键字**: velero, schedule, cron, automated-backup
- **描述**: 演示如何创建定时备份计划，并配置备份保留策略

#### 功能范围
1. 创建基于Cron表达式的定时备份（每日、每周）
2. 配置TTL（Time-To-Live）自动清理策略
3. 查看Schedule历史和下次执行时间
4. 暂停和恢复Schedule任务

#### 资源清单结构
- `daily-backup-schedule.yaml`: 每日备份Schedule定义
- `weekly-backup-schedule.yaml`: 每周备份Schedule定义

#### Schedule配置示例
```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-backup
  namespace: velero
spec:
  schedule: "0 2 * * *"  # 每天凌晨2点
  template:
    includedNamespaces:
    - production
    ttl: 168h  # 保留7天
```

#### 验证点
- Schedule对象创建成功
- 第一次备份自动触发
- 过期备份自动删除
- 执行`velero schedule describe`查看状态

---

### 3.5 Demo #5: backup-restore

#### 元数据定义
- **名称**: 备份恢复完整流程演示
- **难度**: beginner
- **关键字**: velero, restore, recovery, validation
- **描述**: 演示完整的备份→删除→恢复流程，重点展示恢复验证方法

#### 功能范围
1. 创建包含StatefulSet的有状态应用
2. 生成测试数据（写入PV）
3. 执行备份并验证成功
4. 模拟灾难（删除应用和PVC）
5. 恢复并验证数据完整性

#### 资源清单结构
- `statefulset-mysql.yaml`: MySQL StatefulSet示例
- `mysql-pvc.yaml`: PersistentVolumeClaim定义
- `data-validation-job.yaml`: 数据验证Job

#### 恢复验证步骤
- 检查Pod状态和启动日志
- 验证PVC绑定状态
- 执行数据完整性查询
- 对比恢复前后资源版本

#### 验证点
- 恢复状态为Completed
- StatefulSet Pod数量正确
- PVC数据完整（通过checksum或查询验证）
- Service端点可访问

---

### 3.6 Demo #6: pv-snapshot-backup

#### 元数据定义
- **名称**: 持久卷快照备份演示
- **难度**: intermediate
- **关键字**: velero, volume-snapshot, csi, persistent-volume
- **描述**: 演示如何使用CSI快照功能备份持久卷数据

#### 功能范围
1. 配置VolumeSnapshotClass（使用CSI驱动）
2. 创建包含PV的应用（如PostgreSQL）
3. 启用卷快照功能进行备份
4. 验证VolumeSnapshot对象创建
5. 从快照恢复PV

#### 资源清单结构
- `volumesnapshotclass.yaml`: 快照类定义
- `postgres-statefulset.yaml`: PostgreSQL应用
- `backup-with-snapshot.yaml`: 启用快照的备份配置

#### 关键配置
```yaml
spec:
  snapshotVolumes: true
  volumeSnapshotLocations:
  - default
```

#### 验证点
- VolumeSnapshot对象在备份后创建
- 快照数据在存储后端可见
- 恢复后PV数据与原始数据一致
- 快照恢复时间可接受（记录性能指标）

---

### 3.7 Demo #7: resource-filtering

#### 元数据定义
- **名称**: 资源过滤与选择器演示
- **难度**: intermediate
- **关键字**: velero, label-selector, resource-filter, selective-backup
- **描述**: 演示如何使用标签选择器、资源类型过滤等实现精细化备份

#### 功能范围
1. 按标签选择器备份（`--selector`）
2. 按资源类型过滤（`--include-resources`）
3. 排除特定资源（`--exclude-resources`）
4. 组合过滤条件的高级用法

#### 资源清单结构
- `labeled-resources.yaml`: 带标签的多种资源
- `filtered-backup.yaml`: 过滤规则备份定义

#### 过滤规则示例
```bash
# 仅备份带有app=critical标签的资源
velero backup create critical-only --selector app=critical

# 仅备份Deployment和Service
velero backup create deploy-svc --include-resources deployments,services

# 排除Secret和ConfigMap
velero backup create no-secrets --exclude-resources secrets,configmaps
```

#### 验证点
- 备份仅包含匹配标签的资源
- 未匹配资源未被备份
- 资源类型过滤准确
- 组合条件逻辑正确

---

### 3.8 Demo #8: namespace-mapping

#### 元数据定义
- **名称**: 跨命名空间恢复映射演示
- **难度**: intermediate
- **关键字**: velero, namespace-mapping, restore, multi-tenancy
- **描述**: 演示如何将备份的资源恢复到不同的命名空间

#### 功能范围
1. 备份源命名空间资源
2. 使用`--namespace-mappings`恢复到目标命名空间
3. 处理命名空间级别资源冲突
4. 验证资源所有者引用更新

#### 资源清单结构
- `source-namespace.yaml`: 源命名空间和应用
- `restore-with-mapping.yaml`: 带映射的恢复配置

#### 映射配置示例
```yaml
spec:
  namespaceMapping:
    old-namespace: new-namespace
    prod-app: staging-app
```

#### 验证点
- 资源成功恢复到目标命名空间
- Service和Endpoint正确更新
- RBAC资源命名空间绑定正确
- 应用功能正常

---

### 3.9 Demo #9: disaster-recovery-simulation

#### 元数据定义
- **名称**: 完整灾难恢复演练
- **难度**: advanced
- **关键字**: velero, disaster-recovery, rto, rpo, failover
- **描述**: 模拟完整的灾难场景（集群故障），演示灾难恢复的完整流程

#### 功能范围
1. 模拟生产环境多服务集群
2. 定期备份策略配置
3. 模拟灾难（删除关键命名空间）
4. 灾难恢复流程执行
5. RTO/RPO指标测量

#### 资源清单结构
- `production-workloads.yaml`: 模拟生产应用
- `dr-backup-schedule.yaml`: 灾备备份计划
- `dr-restore-playbook.yaml`: 恢复手册（文档形式）

#### 灾难恢复步骤
1. 检测灾难并触发恢复
2. 验证备份存储可访问性
3. 执行最新备份的恢复
4. 验证关键服务健康检查
5. 切换流量到恢复后的服务
6. 记录恢复时间和数据丢失窗口

#### 验证点
- RTO < 30分钟（示例目标）
- RPO < 1小时（基于备份频率）
- 恢复后所有服务可访问
- 数据一致性验证通过

---

### 3.10 Demo #10: backup-hooks

#### 元数据定义
- **名称**: 备份钩子操作演示
- **难度**: advanced
- **关键字**: velero, hooks, pre-backup, post-backup, database-consistency
- **描述**: 演示如何使用备份钩子在备份前后执行自定义操作（如数据库一致性检查）

#### 功能范围
1. Pre-backup hook（备份前执行数据库flush）
2. Post-backup hook（备份后验证）
3. 基于Annotation的Pod级别钩子
4. 钩子执行失败处理策略

#### 资源清单结构
- `mysql-with-hooks.yaml`: 带钩子的MySQL部署
- `backup-with-hooks.yaml`: 带钩子配置的备份

#### 钩子配置示例
```yaml
metadata:
  annotations:
    pre.hook.backup.velero.io/command: '["/bin/bash", "-c", "mysql -e \"FLUSH TABLES WITH READ LOCK\""]'
    pre.hook.backup.velero.io/timeout: 30s
    post.hook.backup.velero.io/command: '["/bin/bash", "-c", "mysql -e \"UNLOCK TABLES\""]'
```

#### 验证点
- Pre-backup钩子执行日志
- 数据库在备份期间的锁状态
- Post-backup钩子成功解锁
- 备份数据一致性验证

---

### 3.11 Demo #11: backup-encryption

#### 元数据定义
- **名称**: 备份数据加密演示
- **难度**: advanced
- **关键字**: velero, encryption, security, kms, sensitive-data
- **描述**: 演示如何启用备份数据加密，保护敏感资源

#### 功能范围
1. 配置加密密钥（使用Kubernetes Secret）
2. 启用客户端加密功能
3. 验证对象存储中的加密数据
4. 使用密钥恢复加密备份

#### 资源清单结构
- `encryption-secret.yaml`: 加密密钥Secret
- `encrypted-backup-location.yaml`: 启用加密的存储位置
- `encrypted-backup.yaml`: 加密备份配置

#### 加密配置
- 使用AES-256-GCM加密算法
- 密钥轮换策略说明
- 密钥管理最佳实践

#### 验证点
- 对象存储中的备份文件已加密（无法直接读取）
- 使用正确密钥可成功恢复
- 使用错误密钥恢复失败
- 加密对性能的影响可接受

---

### 3.12 Demo #12: migration-across-clusters

#### 元数据定义
- **名称**: 跨集群资源迁移演示
- **难度**: advanced
- **关键字**: velero, cluster-migration, multi-cluster, workload-portability
- **描述**: 演示如何使用Velero在不同Kubernetes集群间迁移工作负载

#### 功能范围
1. 源集群备份配置
2. 目标集群Velero安装并配置相同对象存储
3. 跨集群资源恢复
4. 处理集群特定资源（如StorageClass）
5. 验证迁移后的应用功能

#### 资源清单结构
- `source-cluster-backup.yaml`: 源集群备份
- `target-cluster-restore.yaml`: 目标集群恢复
- `cluster-specific-mappings.yaml`: 集群特定资源映射

#### 迁移步骤
1. 在源集群执行备份
2. 确保目标集群Velero配置相同BackupStorageLocation
3. 在目标集群同步备份元数据
4. 执行恢复并处理资源冲突
5. 更新DNS或负载均衡器指向

#### 验证点
- 应用在目标集群成功运行
- PV数据成功迁移
- Service和Ingress正确配置
- 无需修改应用配置

---

### 3.13 Demo #13: backup-monitoring

#### 元数据定义
- **名称**: 备份状态监控与告警演示
- **难度**: intermediate
- **关键字**: velero, monitoring, prometheus, alerting, metrics
- **描述**: 演示如何监控Velero备份任务状态并配置告警规则

#### 功能范围
1. 启用Velero Prometheus metrics
2. 配置ServiceMonitor（Prometheus Operator）
3. 创建备份失败告警规则
4. Grafana仪表板展示（可选）
5. 备份状态查询和日志分析

#### 资源清单结构
- `servicemonitor.yaml`: Prometheus监控配置
- `prometheus-rules.yaml`: 备份告警规则
- `grafana-dashboard.json`: Grafana仪表板（可选）

#### 关键指标
- `velero_backup_success_total`: 成功备份总数
- `velero_backup_failure_total`: 失败备份总数
- `velero_backup_duration_seconds`: 备份耗时
- `velero_backup_last_successful_timestamp`: 最后成功时间

#### 告警规则示例
```yaml
- alert: VeleroBackupFailure
  expr: increase(velero_backup_failure_total[1h]) > 0
  annotations:
    summary: "Velero backup failed"
```

#### 验证点
- Prometheus成功抓取Velero metrics
- 告警规则触发测试
- 仪表板显示备份历史趋势
- 日志集成到日志聚合平台

---

### 3.14 Demo #14: volume-snapshot-location

#### 元数据定义
- **名称**: 卷快照位置配置演示
- **难度**: advanced
- **关键字**: velero, volume-snapshot-location, csi, snapshot-provider
- **描述**: 演示如何配置多个VolumeSnapshotLocation以支持不同存储提供商

#### 功能范围
1. 配置默认VolumeSnapshotLocation
2. 配置多个快照位置（如AWS EBS、Azure Disk）
3. 备份时指定快照位置
4. 快照位置的可用性检查

#### 资源清单结构
- `default-vsl.yaml`: 默认快照位置
- `aws-ebs-vsl.yaml`: AWS EBS快照位置
- `azure-disk-vsl.yaml`: Azure Disk快照位置

#### 配置示例（AWS EBS）
```yaml
apiVersion: velero.io/v1
kind: VolumeSnapshotLocation
metadata:
  name: aws-ebs
  namespace: velero
spec:
  provider: aws
  config:
    region: us-west-2
```

#### 验证点
- 多个VolumeSnapshotLocation对象创建成功
- 备份时可选择特定快照位置
- 快照存储在对应的提供商后端
- 跨区域快照复制验证（高级场景）

---

### 3.15 Demo #15: backup-deletion

#### 元数据定义
- **名称**: 备份清理与保留策略演示
- **难度**: beginner
- **关键字**: velero, backup-deletion, retention-policy, storage-management
- **描述**: 演示如何手动删除备份、配置自动清理策略和管理对象存储空间

#### 功能范围
1. 手动删除单个备份
2. 批量删除过期备份
3. 配置TTL自动清理
4. 验证对象存储空间释放
5. 删除保护机制说明

#### 资源清单结构
- `ttl-backup.yaml`: 带TTL的备份定义
- `cleanup-job.yaml`: 清理脚本Job（可选）

#### 删除命令示例
```bash
# 删除单个备份
velero backup delete old-backup

# 删除所有Completed状态的备份
velero backup delete --selector velero.io/phase=Completed

# 查看即将过期的备份
velero backup get --show-labels
```

#### TTL配置
```yaml
spec:
  ttl: 720h  # 30天后自动删除
```

#### 验证点
- 执行删除后备份对象消失
- 对象存储中的备份文件被删除
- TTL到期后备份自动清理
- 删除操作记录在审计日志中

---

## 4. 测试用例设计

### 4.1 测试用例分类

| 测试类别 | 测试目标 | 覆盖Demo |
|---------|---------|---------|
| **安装验证** | Velero组件正常安装 | #1 |
| **功能正确性** | 备份和恢复功能正常 | #2, #3, #5, #6 |
| **策略配置** | 定时任务和过滤规则生效 | #4, #7 |
| **高级场景** | 钩子、加密、跨集群功能 | #10, #11, #12 |
| **运维监控** | 监控指标和告警正常 | #13 |
| **数据一致性** | 恢复后数据完整无损 | #5, #6, #9 |

### 4.2 测试用例详细规格

#### TC-001: Velero基础安装验证
- **对应Demo**: #1 basic-installation
- **前置条件**: 
  - Kubernetes集群可用（minikube或云厂商集群）
  - kubectl已配置并可访问集群
  - Helm 3+已安装
- **测试步骤**:
  1. 执行MinIO部署YAML
  2. 验证MinIO Pod状态为Running
  3. 使用Helm安装Velero（提供values文件）
  4. 检查Velero Pod状态
  5. 执行`velero version`命令
  6. 执行`velero backup-location get`验证存储连接
- **期望结果**:
  - 所有Pod状态为Running
  - Velero CLI输出server和client版本一致
  - BackupStorageLocation状态为Available
- **失败处理**: 查看Pod日志，检查凭证配置是否正确

#### TC-002: 命名空间备份与恢复
- **对应Demo**: #2 namespace-backup
- **前置条件**: 
  - Velero已成功安装（TC-001通过）
  - 存在测试命名空间和示例应用
- **测试步骤**:
  1. 创建nginx-example命名空间和应用
  2. 写入测试数据到ConfigMap
  3. 执行备份命令：`velero backup create test-backup --include-namespaces nginx-example`
  4. 等待备份完成（检查状态为Completed）
  5. 删除nginx-example命名空间
  6. 执行恢复命令：`velero restore create --from-backup test-backup`
  7. 验证命名空间和资源恢复
- **期望结果**:
  - 备份状态显示Completed
  - 恢复后命名空间存在
  - 应用Pod正常运行
  - ConfigMap数据与备份前一致
- **数据验证**: 使用checksum或kubectl diff对比资源

#### TC-003: 持久卷快照功能
- **对应Demo**: #6 pv-snapshot-backup
- **前置条件**:
  - 集群支持CSI快照功能
  - VolumeSnapshotClass已配置
- **测试步骤**:
  1. 部署带PVC的StatefulSet应用
  2. 写入测试文件到PV（例如：`echo "test-data" > /data/test.txt`）
  3. 创建启用快照的备份
  4. 验证VolumeSnapshot对象创建
  5. 删除应用和PVC
  6. 从备份恢复
  7. 验证文件内容一致
- **期望结果**:
  - VolumeSnapshot对象存在且状态为ReadyToUse
  - 恢复后PV挂载成功
  - 文件内容匹配
- **性能指标**: 记录快照创建和恢复时间

#### TC-004: 定时备份任务
- **对应Demo**: #4 scheduled-backup
- **前置条件**: 
  - Velero已安装
  - 存在需要定期备份的命名空间
- **测试步骤**:
  1. 创建Schedule对象（cron表达式设置为每5分钟）
  2. 等待第一次备份触发
  3. 检查自动创建的Backup对象
  4. 修改应用并等待第二次备份
  5. 验证两次备份都成功
  6. 检查TTL策略（设置为10分钟）
  7. 等待过期备份自动删除
- **期望结果**:
  - Schedule对象显示下次执行时间
  - 每次定时触发都成功创建Backup
  - 过期备份被自动清理
- **监控验证**: 查看Prometheus metrics中的备份计数器

#### TC-005: 资源过滤与选择器
- **对应Demo**: #7 resource-filtering
- **前置条件**: 
  - 命名空间中存在多种标签的资源
- **测试步骤**:
  1. 创建带有不同标签的资源（app=critical和app=test）
  2. 执行带标签选择器的备份：`--selector app=critical`
  3. 检查备份描述中的资源列表
  4. 验证仅critical标签的资源被备份
  5. 执行资源类型过滤：`--include-resources deployments,services`
  6. 验证仅指定类型被备份
- **期望结果**:
  - 备份中仅包含匹配标签的资源
  - 未匹配资源不在备份中
  - 资源计数符合预期
- **验证方法**: 使用`velero backup describe --details`查看资源列表

#### TC-006: 跨集群资源迁移
- **对应Demo**: #12 migration-across-clusters
- **前置条件**:
  - 两个独立的Kubernetes集群
  - 两个集群的Velero配置相同的对象存储
- **测试步骤**:
  1. 在源集群创建应用和数据
  2. 在源集群执行备份
  3. 验证备份上传到共享对象存储
  4. 在目标集群安装Velero（相同配置）
  5. 在目标集群执行`velero backup get`同步备份
  6. 执行恢复操作
  7. 验证应用在目标集群正常运行
- **期望结果**:
  - 应用在目标集群功能正常
  - PV数据迁移成功
  - 无需修改应用配置
- **网络验证**: 测试Service和Ingress是否可访问

#### TC-007: 备份钩子执行
- **对应Demo**: #10 backup-hooks
- **前置条件**:
  - 部署支持钩子的应用（如MySQL）
- **测试步骤**:
  1. 配置pre-backup钩子（数据库flush）
  2. 执行备份
  3. 查看Pod日志验证钩子执行
  4. 验证post-backup钩子执行
  5. 恢复备份并验证数据一致性
- **期望结果**:
  - 钩子命令在日志中可见
  - 数据库一致性检查通过
  - 备份期间应用短暂只读
- **失败场景**: 测试钩子超时和失败处理

#### TC-008: 备份数据加密
- **对应Demo**: #11 backup-encryption
- **前置条件**:
  - 准备加密密钥Secret
- **测试步骤**:
  1. 配置启用加密的BackupStorageLocation
  2. 创建包含敏感数据的资源（Secret）
  3. 执行加密备份
  4. 检查对象存储中的备份文件（应无法直接读取）
  5. 使用正确密钥恢复备份
  6. 测试使用错误密钥恢复（应失败）
- **期望结果**:
  - 对象存储中的备份文件已加密
  - 正确密钥可恢复
  - 错误密钥恢复失败并有明确错误提示
- **安全验证**: 使用hex编辑器检查备份文件无明文

#### TC-009: 灾难恢复演练
- **对应Demo**: #9 disaster-recovery-simulation
- **前置条件**:
  - 模拟生产环境应用运行
  - 定时备份策略已配置
- **测试步骤**:
  1. 记录灾难前的应用状态和数据
  2. 模拟灾难（删除关键命名空间）
  3. 记录检测到灾难的时间（T0）
  4. 执行灾难恢复流程
  5. 记录恢复完成时间（T1）
  6. 验证应用功能和数据完整性
  7. 计算RTO和RPO
- **期望结果**:
  - RTO（T1-T0）< 30分钟
  - RPO（数据丢失）< 1小时（基于备份频率）
  - 所有关键服务恢复
  - 数据一致性验证通过
- **性能记录**: 记录每个步骤的耗时

#### TC-010: 备份监控与告警
- **对应Demo**: #13 backup-monitoring
- **前置条件**:
  - Prometheus Operator已安装
  - Grafana已安装（可选）
- **测试步骤**:
  1. 应用ServiceMonitor配置
  2. 验证Prometheus抓取Velero metrics
  3. 查询备份成功和失败计数器
  4. 触发备份失败场景（如存储不可用）
  5. 验证告警触发
  6. 导入Grafana仪表板（可选）
- **期望结果**:
  - Metrics端点可访问
  - Prometheus成功抓取数据
  - 告警规则在失败时触发
  - 仪表板显示备份趋势
- **集成验证**: 测试告警发送到钉钉/Slack

---

### 4.3 自动化测试脚本设计

每个Demo的`code/`目录下提供自动化测试脚本：

#### 脚本结构（示例：test-backup.sh）
```bash
#!/bin/bash
# 自动化测试脚本：命名空间备份与恢复

set -e  # 遇到错误立即退出

# 步骤1: 创建测试命名空间
kubectl create namespace test-backup-ns

# 步骤2: 部署示例应用
kubectl apply -f sample-app.yaml -n test-backup-ns

# 步骤3: 等待应用就绪
kubectl wait --for=condition=Ready pod -l app=nginx -n test-backup-ns --timeout=60s

# 步骤4: 执行备份
velero backup create test-backup --include-namespaces test-backup-ns

# 步骤5: 等待备份完成
while [[ $(velero backup describe test-backup -o json | jq -r '.status.phase') != "Completed" ]]; do
  echo "等待备份完成..."
  sleep 5
done

# 步骤6: 验证备份
RESOURCE_COUNT=$(velero backup describe test-backup --details | grep -c "Deployment\|Service")
if [ "$RESOURCE_COUNT" -lt 2 ]; then
  echo "❌ 备份资源数量不足"
  exit 1
fi

# 步骤7: 删除命名空间
kubectl delete namespace test-backup-ns

# 步骤8: 恢复备份
velero restore create --from-backup test-backup

# 步骤9: 验证恢复
kubectl wait --for=condition=Ready pod -l app=nginx -n test-backup-ns --timeout=120s

echo "✅ 测试通过：备份和恢复成功"

# 清理
velero backup delete test-backup --confirm
kubectl delete namespace test-backup-ns
```

#### 测试脚本规范
- 使用`set -e`确保错误时退出
- 每个步骤添加日志输出
- 使用`kubectl wait`等待资源就绪
- 验证点使用条件判断和明确的成功/失败提示
- 测试结束清理所有资源
- 支持幂等执行（可重复运行）

---

## 5. 测试报告规格

### 5.1 测试报告模板

#### 报告文件位置
每个Demo的根目录下生成`TEST_REPORT.md`文件。

#### 报告内容结构

```markdown
# Velero Demo测试报告

## 测试概要

| 项目 | 值 |
|-----|---|
| Demo名称 | {demo_name} |
| 测试日期 | {date} |
| 测试环境 | Kubernetes {version}, Velero {version} |
| 测试执行者 | {executor} |
| 测试结果 | ✅ 通过 / ❌ 失败 |

## 测试用例执行结果

| 用例ID | 用例名称 | 状态 | 耗时 | 备注 |
|-------|---------|------|-----|------|
| TC-001 | 安装验证 | ✅ 通过 | 120s | - |
| TC-002 | 备份执行 | ✅ 通过 | 45s | - |
| TC-003 | 恢复验证 | ✅ 通过 | 90s | - |

## 详细测试日志

### TC-001: 安装验证

**执行步骤**:
1. 部署MinIO: 成功
2. 安装Velero: 成功
3. 验证连接: 成功

**执行输出**:
```
Client:
        Version: v1.12.0
Server:
        Version: v1.12.0
```

**验证结果**: ✅ 通过

---

## 性能指标

| 指标 | 值 | 目标 | 结果 |
|-----|---|------|------|
| 备份耗时 | 45s | < 60s | ✅ |
| 恢复耗时 | 90s | < 120s | ✅ |
| 数据一致性 | 100% | 100% | ✅ |

## 问题与风险

### 发现的问题
- 无

### 风险评估
- **风险**: CSI快照依赖存储插件支持
- **缓解措施**: 文档中明确CSI要求

## 测试环境信息

```yaml
Kubernetes版本: v1.28.0
Velero版本: v1.12.0
对象存储: MinIO (模拟S3)
存储插件: CSI hostpath
节点数量: 1 (minikube)
```

## 测试结论

本次测试覆盖了Velero的核心功能，所有测试用例均通过验证。Demo可用于生产参考。

**建议**: 在生产环境应使用云厂商的对象存储服务（如AWS S3）替代MinIO。
```

---

### 5.2 自动化报告生成

#### 脚本：generate-test-report.sh
```bash
#!/bin/bash
# 生成测试报告脚本

DEMO_NAME=$1
REPORT_FILE="TEST_REPORT.md"

# 执行测试并捕获输出
TEST_OUTPUT=$(./code/test-*.sh 2>&1)
TEST_RESULT=$?

# 记录测试时间
START_TIME=$(date -Iseconds)
# ... 执行测试 ...
END_TIME=$(date -Iseconds)
DURATION=$((END_TIME - START_TIME))

# 生成报告
cat > $REPORT_FILE <<EOF
# Velero Demo测试报告

## 测试概要

| 项目 | 值 |
|-----|---|
| Demo名称 | $DEMO_NAME |
| 测试日期 | $(date) |
| 测试结果 | $([ $TEST_RESULT -eq 0 ] && echo "✅ 通过" || echo "❌ 失败") |
| 测试耗时 | ${DURATION}s |

## 测试输出

\`\`\`
$TEST_OUTPUT
\`\`\`

EOF

echo "测试报告已生成: $REPORT_FILE"
```

---

## 6. README文档更新规格

### 6.1 README.md更新内容

在主README中的Kubernetes章节添加Velero工具清单：

#### 更新位置
在`⎈ Kubernetes`部分，kubeflow、kubeskoop之后新增velero。

#### 更新内容格式
```markdown
<details>
<summary><b>📦 Velero工具 (15个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/velero/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-installation` | Velero基础安装与配置 | beginner | ✅ |
| 2 | `namespace-backup` | 命名空间级别备份 | beginner | ✅ |
| 3 | `cluster-backup` | 集群级别全量备份 | intermediate | ✅ |
| 4 | `scheduled-backup` | 定时备份策略配置 | intermediate | ✅ |
| 5 | `resource-filtering` | 资源过滤与标签选择器 | intermediate | ✅ |
| 6 | `backup-restore` | 备份恢复完整流程 | beginner | ✅ |
| 7 | `namespace-mapping` | 跨命名空间恢复映射 | intermediate | ✅ |
| 8 | `disaster-recovery-simulation` | 完整灾难恢复演练 | advanced | ✅ |
| 9 | `pv-snapshot-backup` | 持久卷快照备份 | intermediate | ✅ |
| 10 | `volume-snapshot-location` | 卷快照位置配置 | advanced | ✅ |
| 11 | `backup-hooks` | 备份前后钩子操作 | advanced | ✅ |
| 12 | `backup-encryption` | 备份数据加密 | advanced | ✅ |
| 13 | `migration-across-clusters` | 跨集群资源迁移 | advanced | ✅ |
| 14 | `backup-monitoring` | 备份状态监控与告警 | intermediate | ✅ |
| 15 | `backup-deletion` | 备份清理与保留策略 | beginner | ✅ |

**功能覆盖**:
- ✅ 安装部署与基础配置
- ✅ 命名空间和集群级别备份
- ✅ 定时备份与保留策略
- ✅ 持久卷快照与数据恢复
- ✅ 灾难恢复与跨集群迁移
- ✅ 备份钩子与数据加密
- ✅ 监控告警与运维管理

</details>
```

### 6.2 Demo统计表更新

更新主README顶部的统计表：

```markdown
| 语言 | 基础Demo | 第三方库/工具 | 总计 | 测试状态 |
|---------|----------|----------|------|----------|
| ⎈ **Kubernetes** | 0 | kubeflow(42), kubeskoop(10), velero(15), operator-framework(2) | 69 | ✅ 全部通过 |
| **总计** | **210** | **96** | **306** | ✅ |
```

### 6.3 STATUS.md文件更新

如果项目存在STATUS.md跟踪功能状态，应添加：

```markdown
## Velero工具支持 (v1.0.0)

- [x] 基础安装与配置
- [x] 命名空间备份与恢复
- [x] 集群级别备份
- [x] 定时备份策略
- [x] 持久卷快照
- [x] 灾难恢复演练
- [x] 跨集群迁移
- [x] 备份加密
- [x] 监控告警集成
- [x] 完整测试覆盖
```

---

## 7. 实施计划

### 7.1 开发阶段

#### 阶段1: 核心功能Demo (P0优先级)
**时间**: 第1周
- 开发Demo #1: basic-installation
- 开发Demo #2: namespace-backup
- 开发Demo #3: cluster-backup
- 开发Demo #4: scheduled-backup
- 开发Demo #5: backup-restore
- 开发Demo #6: pv-snapshot-backup
- 开发Demo #15: backup-deletion

**交付物**: 7个核心Demo，每个包含完整的README、YAML和测试脚本

#### 阶段2: 扩展功能Demo (P1优先级)
**时间**: 第2周
- 开发Demo #7: resource-filtering
- 开发Demo #8: namespace-mapping
- 开发Demo #9: disaster-recovery-simulation
- 开发Demo #13: backup-monitoring
- 开发Demo #12: migration-across-clusters
- 开发Demo #14: volume-snapshot-location

**交付物**: 6个扩展Demo

#### 阶段3: 高级功能Demo (P2优先级)
**时间**: 第3周
- 开发Demo #10: backup-hooks
- 开发Demo #11: backup-encryption

**交付物**: 2个高级Demo

### 7.2 测试与验证阶段

#### 阶段4: 集成测试
**时间**: 第3周
- 执行所有15个Demo的测试用例
- 生成测试报告
- 修复发现的问题
- 性能基准测试

#### 阶段5: 文档完善
**时间**: 第4周
- 完善每个Demo的README
- 生成统一的测试报告汇总
- 更新主README.md
- 更新STATUS.md

### 7.3 交付清单

#### 最终交付物
1. **15个Velero Demo**，每个包含：
   - `metadata.json`: 元数据文件
   - `README.md`: 详细使用文档
   - `code/`: YAML资源清单和测试脚本
   - `TEST_REPORT.md`: 测试报告

2. **文档更新**：
   - 主`README.md`添加Velero章节
   - 统计数据更新（306个Demo）
   - `STATUS.md`功能跟踪更新

3. **测试报告**：
   - 每个Demo的独立测试报告
   - 汇总测试报告（覆盖率、通过率）

4. **CI集成**（可选）：
   - GitHub Actions工作流验证Demo
   - 自动化测试执行

---

## 8. 验证标准

### 8.1 Demo质量标准

每个Demo必须满足以下标准才能交付：

#### 文档完整性
- [x] README.md包含完整的功能说明
- [x] 环境要求明确（Kubernetes版本、工具依赖）
- [x] 逐步实操指南清晰
- [x] 代码解析和预期输出完整
- [x] 常见问题FAQ覆盖

#### 资源清单质量
- [x] 所有YAML文件语法正确（通过验证器）
- [x] 资源定义遵循最佳实践
- [x] 包含必要的注释和说明
- [x] 命名空间隔离（避免冲突）

#### 测试覆盖
- [x] 提供自动化测试脚本
- [x] 测试脚本幂等且可重复执行
- [x] 验证点明确（成功/失败判断）
- [x] 测试报告自动生成

#### 验证机制对齐
- [x] 通过`demo_verifier.py`的Kubernetes验证逻辑
- [x] 静态YAML语法检查通过
- [x] kubectl和helm工具可用性检查
- [x] Dry-run验证通过（如适用）

### 8.2 集成验证流程

#### 自动化验证步骤
1. **静态检查**: 验证所有YAML文件语法
2. **元数据验证**: 检查metadata.json格式和必填字段
3. **文档检查**: README.md存在且包含关键章节
4. **测试执行**: 运行测试脚本并记录结果
5. **性能检查**: 记录备份和恢复耗时

#### 验证通过标准
- 所有静态检查无错误
- 测试脚本执行成功（退出码0）
- 测试报告显示所有用例通过
- 性能指标在可接受范围内

---

## 9. 风险与缓解措施

### 9.1 技术风险

| 风险 | 影响 | 概率 | 缓解措施 |
|-----|-----|------|---------|
| CSI快照功能依赖存储插件 | 部分Demo无法在所有环境运行 | 中 | 文档明确环境要求；提供备选方案（Restic文件备份） |
| 对象存储配置复杂度 | 用户安装难度大 | 中 | 提供MinIO快速部署方案；多云厂商配置示例 |
| Velero版本兼容性 | 不同版本行为差异 | 低 | 明确测试版本；提供多版本兼容性说明 |
| 跨集群迁移需要多集群环境 | 测试复杂度高 | 中 | 提供minikube多实例方案；云厂商测试集群 |

### 9.2 运维风险

| 风险 | 影响 | 概率 | 缓解措施 |
|-----|-----|------|---------|
| 备份数据占用大量存储 | 成本增加 | 高 | 文档说明TTL策略；提供存储空间监控方案 |
| 恢复时间超出预期 | RTO目标无法满足 | 中 | 性能基准测试；提供优化建议 |
| 加密密钥丢失导致数据不可恢复 | 数据永久丢失 | 低 | 文档强调密钥管理重要性；提供密钥备份方案 |

### 9.3 项目集成风险

| 风险 | 影响 | 概率 | 缓解措施 |
|-----|-----|------|---------|
| Demo结构与现有不一致 | 集成失败 | 低 | 严格遵循kubernetes/<tool>/<demo>结构 |
| 验证流程未覆盖新场景 | CI失败 | 中 | 扩展demo_verifier.py支持Velero特定验证 |
| 文档更新冲突 | 合并问题 | 低 | 预先协调README更新位置 |

---

## 10. 成功标准

### 10.1 功能完整性
- [x] 覆盖Velero官方文档中的核心功能（备份、恢复、定时任务、快照）
- [x] 提供beginner到advanced的完整难度梯度
- [x] 每个功能点至少有一个Demo演示

### 10.2 质量标准
- [x] 所有15个Demo通过自动化验证
- [x] 测试覆盖率达到100%（每个Demo有对应测试用例）
- [x] 文档完整性检查通过（README、metadata、TEST_REPORT）

### 10.3 用户体验
- [x] 用户可通过`opendemo get kubernetes velero`命令列出所有Demo
- [x] 每个Demo可独立运行（依赖明确）
- [x] 平均10分钟内完成单个Demo的部署和验证

### 10.4 社区影响
- [x] README中Kubernetes Demo数量从54增加到69
- [x] 提供生产级灾备方案参考
- [x] 社区用户反馈评分≥4.5/5（如适用）

---

## 11. 附录

### 11.1 Velero架构参考

Velero由以下组件构成：
- **Server**: 运行在Kubernetes集群中的控制器（Deployment）
- **CLI**: 用户命令行工具（velero命令）
- **Plugins**: 对象存储和卷快照插件（AWS、Azure、GCP等）
- **Restic**: 可选的文件级备份工具（集成在Server中）

### 11.2 对象存储后端支持

| 存储类型 | 插件 | Demo中的使用 |
|---------|-----|-------------|
| AWS S3 | velero-plugin-for-aws | 文档中提供配置示例 |
| Azure Blob | velero-plugin-for-microsoft-azure | 文档中提供配置示例 |
| GCP Storage | velero-plugin-for-gcp | 文档中提供配置示例 |
| MinIO | S3兼容API | Demo中默认使用（测试环境） |

### 11.3 参考资料
- Velero官方文档: https://velero.io/docs/
- Velero GitHub仓库: https://github.com/vmware-tanzu/velero
- CSI快照规范: https://kubernetes.io/docs/concepts/storage/volume-snapshots/
- 项目现有Kubernetes Demo: `opendemo_output/kubernetes/kubeskoop/`
| **持久卷管理** | volume-snapshot-location | advanced | 卷快照位置配置 | P1 |
| **高级功能** | backup-hooks | advanced | 备份前后钩子操作 | P2 |
| **高级功能** | backup-encryption | advanced | 备份数据加密 | P2 |
| **高级功能** | migration-across-clusters | advanced | 跨集群资源迁移 | P1 |
| **监控运维** | backup-monitoring | intermediate | 备份状态监控与告警 | P1 |
| **运维操作** | backup-deletion | beginner | 备份清理与保留策略 | P1 |

### 2.2 Demo数量与范围

- **计划总数**: 15个Demo
- **核心Demo(P0)**: 7个
- **扩展Demo(P1)**: 6个
- **高级Demo(P2)**: 2个

## 3. 详细Demo设计规格

### 3.1 Demo #1: basic-installation

#### 元数据定义
- **名称**: Velero基础安装与配置演示
- **难度**: beginner
- **关键字**: velero, installation, minio, backup-storage
- **描述**: 演示如何使用Helm或官方CLI安装Velero，并配置MinIO作为对象存储后端

#### 功能范围
1. MinIO对象存储部署（轻量级测试环境）
2. Velero Server端安装（Helm Chart方式）
3. Velero CLI工具安装与验证
4. BackupStorageLocation配置与连接测试
5. VolumeSnapshotLocation基础配置

#### 资源清单结构
- `minio-deployment.yaml`: MinIO服务部署
- `minio-service.yaml`: MinIO服务暴露
- `velero-values.yaml`: Helm安装配置文件
- `backup-storage-location.yaml`: 备份存储位置定义
- `credentials-secret.yaml`: 对象存储凭证（示例模板）

#### 验证点
- MinIO服务健康检查
- Velero Pod运行状态
- BackupStorageLocation连接可达性
- 执行`velero version`和`velero backup-location get`命令成功

---

### 3.2 Demo #2: namespace-backup

#### 元数据定义
- **名称**: 命名空间级别备份演示
- **难度**: beginner
- **关键字**: velero, backup, namespace, restore
- **描述**: 演示如何备份指定命名空间的所有资源并进行恢复验证

#### 功能范围
1. 创建示例应用（Nginx Deployment + Service + ConfigMap）
2. 使用`velero backup create`备份指定命名空间
3. 模拟数据丢失场景（删除命名空间）
4. 使用`velero restore create`恢复备份
5. 验证资源完整性

#### 资源清单结构
- `sample-app.yaml`: 示例应用资源定义
- `backup-spec.yaml`: 备份任务声明式定义（备选）
- `restore-spec.yaml`: 恢复任务定义（备选）

#### 关键命令示例
```bash
velero backup create nginx-backup --include-namespaces nginx-example
velero backup describe nginx-backup
velero restore create --from-backup nginx-backup
```

#### 验证点
- 备份状态为Completed
- 备份包含正确数量的资源（通过`velero backup describe`）
- 恢复后应用可正常访问
- ConfigMap数据一致性检查

---

### 3.3 Demo #3: cluster-backup

#### 元数据定义
- **名称**: 集群级别全量备份演示
- **难度**: intermediate
- **关键字**: velero, cluster-backup, full-backup, disaster-recovery
- **描述**: 演示如何执行集群级别全量备份，包括系统命名空间和CRD资源

#### 功能范围
1. 全集群资源备份（不包含kube-system等系统命名空间）
2. CRD资源自动包含
3. PersistentVolume和PVC的备份
4. 备份排除规则配置（示例排除临时资源）

#### 资源清单结构
- `cluster-backup.yaml`: 集群备份任务定义
- `backup-exclude-config.yaml`: 排除规则ConfigMap

#### 关键配置
- `--include-cluster-resources=true`
- `--exclude-namespaces`: 排除系统命名空间
- `--default-volumes-to-restic=true`: 文件级备份启用（可选）

#### 验证点
- 备份包含多个命名空间资源
- CRD被正确备份
- 备份大小合理（通过MinIO或对象存储查看）

---

### 3.4 Demo #4: scheduled-backup

#### 元数据定义
- **名称**: 定时备份策略配置演示
- **难度**: intermediate
- **关键字**: velero, schedule, cron, automated-backup
- **描述**: 演示如何创建定时备份计划，并配置备份保留策略

#### 功能范围
1. 创建基于Cron表达式的定时备份（每日、每周）
2. 配置TTL（Time-To-Live）自动清理策略
3. 查看Schedule历史和下次执行时间
4. 暂停和恢复Schedule任务

#### 资源清单结构
- `daily-backup-schedule.yaml`: 每日备份Schedule定义
- `weekly-backup-schedule.yaml`: 每周备份Schedule定义

#### Schedule配置示例
```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-backup
  namespace: velero
spec:
  schedule: "0 2 * * *"  # 每天凌晨2点
  template:
    includedNamespaces:
    - production
    ttl: 168h  # 保留7天
```

#### 验证点
- Schedule对象创建成功
- 第一次备份自动触发
- 过期备份自动删除
- 执行`velero schedule describe`查看状态

---

### 3.5 Demo #5: backup-restore

#### 元数据定义
- **名称**: 备份恢复完整流程演示
- **难度**: beginner
- **关键字**: velero, restore, recovery, validation
- **描述**: 演示完整的备份→删除→恢复流程，重点展示恢复验证方法

#### 功能范围
1. 创建包含StatefulSet的有状态应用
2. 生成测试数据（写入PV）
3. 执行备份并验证成功
4. 模拟灾难（删除应用和PVC）
5. 恢复并验证数据完整性

#### 资源清单结构
- `statefulset-mysql.yaml`: MySQL StatefulSet示例
- `mysql-pvc.yaml`: PersistentVolumeClaim定义
- `data-validation-job.yaml`: 数据验证Job

#### 恢复验证步骤
- 检查Pod状态和启动日志
- 验证PVC绑定状态
- 执行数据完整性查询
- 对比恢复前后资源版本

#### 验证点
- 恢复状态为Completed
- StatefulSet Pod数量正确
- PVC数据完整（通过checksum或查询验证）
- Service端点可访问

---

### 3.6 Demo #6: pv-snapshot-backup

#### 元数据定义
- **名称**: 持久卷快照备份演示
- **难度**: intermediate
- **关键字**: velero, volume-snapshot, csi, persistent-volume
- **描述**: 演示如何使用CSI快照功能备份持久卷数据

#### 功能范围
1. 配置VolumeSnapshotClass（使用CSI驱动）
2. 创建包含PV的应用（如PostgreSQL）
3. 启用卷快照功能进行备份
4. 验证VolumeSnapshot对象创建
5. 从快照恢复PV

#### 资源清单结构
- `volumesnapshotclass.yaml`: 快照类定义
- `postgres-statefulset.yaml`: PostgreSQL应用
- `backup-with-snapshot.yaml`: 启用快照的备份配置

#### 关键配置
```yaml
spec:
  snapshotVolumes: true
  volumeSnapshotLocations:
  - default
```

#### 验证点
- VolumeSnapshot对象在备份后创建
- 快照数据在存储后端可见
- 恢复后PV数据与原始数据一致
- 快照恢复时间可接受（记录性能指标）

---

### 3.7 Demo #7: resource-filtering

#### 元数据定义
- **名称**: 资源过滤与选择器演示
- **难度**: intermediate
- **关键字**: velero, label-selector, resource-filter, selective-backup
- **描述**: 演示如何使用标签选择器、资源类型过滤等实现精细化备份

#### 功能范围
1. 按标签选择器备份（`--selector`）
2. 按资源类型过滤（`--include-resources`）
3. 排除特定资源（`--exclude-resources`）
4. 组合过滤条件的高级用法

#### 资源清单结构
- `labeled-resources.yaml`: 带标签的多种资源
- `filtered-backup.yaml`: 过滤规则备份定义

#### 过滤规则示例
```bash
# 仅备份带有app=critical标签的资源
velero backup create critical-only --selector app=critical

# 仅备份Deployment和Service
velero backup create deploy-svc --include-resources deployments,services

# 排除Secret和ConfigMap
velero backup create no-secrets --exclude-resources secrets,configmaps
```

#### 验证点
- 备份仅包含匹配标签的资源
- 未匹配资源未被备份
- 资源类型过滤准确
- 组合条件逻辑正确

---

### 3.8 Demo #8: namespace-mapping

#### 元数据定义
- **名称**: 跨命名空间恢复映射演示
- **难度**: intermediate
- **关键字**: velero, namespace-mapping, restore, multi-tenancy
- **描述**: 演示如何将备份的资源恢复到不同的命名空间

#### 功能范围
1. 备份源命名空间资源
2. 使用`--namespace-mappings`恢复到目标命名空间
3. 处理命名空间级别资源冲突
4. 验证资源所有者引用更新

#### 资源清单结构
- `source-namespace.yaml`: 源命名空间和应用
- `restore-with-mapping.yaml`: 带映射的恢复配置

#### 映射配置示例
```yaml
spec:
  namespaceMapping:
    old-namespace: new-namespace
    prod-app: staging-app
```

#### 验证点
- 资源成功恢复到目标命名空间
- Service和Endpoint正确更新
- RBAC资源命名空间绑定正确
- 应用功能正常

---

### 3.9 Demo #9: disaster-recovery-simulation

#### 元数据定义
- **名称**: 完整灾难恢复演练
- **难度**: advanced
- **关键字**: velero, disaster-recovery, rto, rpo, failover
- **描述**: 模拟完整的灾难场景（集群故障），演示灾难恢复的完整流程

#### 功能范围
1. 模拟生产环境多服务集群
2. 定期备份策略配置
3. 模拟灾难（删除关键命名空间）
4. 灾难恢复流程执行
5. RTO/RPO指标测量

#### 资源清单结构
- `production-workloads.yaml`: 模拟生产应用
- `dr-backup-schedule.yaml`: 灾备备份计划
- `dr-restore-playbook.yaml`: 恢复手册（文档形式）

#### 灾难恢复步骤
1. 检测灾难并触发恢复
2. 验证备份存储可访问性
3. 执行最新备份的恢复
4. 验证关键服务健康检查
5. 切换流量到恢复后的服务
6. 记录恢复时间和数据丢失窗口

#### 验证点
- RTO < 30分钟（示例目标）
- RPO < 1小时（基于备份频率）
- 恢复后所有服务可访问
- 数据一致性验证通过

---

### 3.10 Demo #10: backup-hooks

#### 元数据定义
- **名称**: 备份钩子操作演示
- **难度**: advanced
- **关键字**: velero, hooks, pre-backup, post-backup, database-consistency
- **描述**: 演示如何使用备份钩子在备份前后执行自定义操作（如数据库一致性检查）

#### 功能范围
1. Pre-backup hook（备份前执行数据库flush）
2. Post-backup hook（备份后验证）
3. 基于Annotation的Pod级别钩子
4. 钩子执行失败处理策略

#### 资源清单结构
- `mysql-with-hooks.yaml`: 带钩子的MySQL部署
- `backup-with-hooks.yaml`: 带钩子配置的备份

#### 钩子配置示例
```yaml
metadata:
  annotations:
    pre.hook.backup.velero.io/command: '["/bin/bash", "-c", "mysql -e \"FLUSH TABLES WITH READ LOCK\""]'
    pre.hook.backup.velero.io/timeout: 30s
    post.hook.backup.velero.io/command: '["/bin/bash", "-c", "mysql -e \"UNLOCK TABLES\""]'
```

#### 验证点
- Pre-backup钩子执行日志
- 数据库在备份期间的锁状态
- Post-backup钩子成功解锁
- 备份数据一致性验证

---

### 3.11 Demo #11: backup-encryption

#### 元数据定义
- **名称**: 备份数据加密演示
- **难度**: advanced
- **关键字**: velero, encryption, security, kms, sensitive-data
- **描述**: 演示如何启用备份数据加密，保护敏感资源

#### 功能范围
1. 配置加密密钥（使用Kubernetes Secret）
2. 启用客户端加密功能
3. 验证对象存储中的加密数据
4. 使用密钥恢复加密备份

#### 资源清单结构
- `encryption-secret.yaml`: 加密密钥Secret
- `encrypted-backup-location.yaml`: 启用加密的存储位置
- `encrypted-backup.yaml`: 加密备份配置

#### 加密配置
- 使用AES-256-GCM加密算法
- 密钥轮换策略说明
- 密钥管理最佳实践

#### 验证点
- 对象存储中的备份文件已加密（无法直接读取）
- 使用正确密钥可成功恢复
- 使用错误密钥恢复失败
- 加密对性能的影响可接受

---

### 3.12 Demo #12: migration-across-clusters

#### 元数据定义
- **名称**: 跨集群资源迁移演示
- **难度**: advanced
- **关键字**: velero, cluster-migration, multi-cluster, workload-portability
- **描述**: 演示如何使用Velero在不同Kubernetes集群间迁移工作负载

#### 功能范围
1. 源集群备份配置
2. 目标集群Velero安装并配置相同对象存储
3. 跨集群资源恢复
4. 处理集群特定资源（如StorageClass）
5. 验证迁移后的应用功能

#### 资源清单结构
- `source-cluster-backup.yaml`: 源集群备份
- `target-cluster-restore.yaml`: 目标集群恢复
- `cluster-specific-mappings.yaml`: 集群特定资源映射

#### 迁移步骤
1. 在源集群执行备份
2. 确保目标集群Velero配置相同BackupStorageLocation
3. 在目标集群同步备份元数据
4. 执行恢复并处理资源冲突
5. 更新DNS或负载均衡器指向

#### 验证点
- 应用在目标集群成功运行
- PV数据成功迁移
- Service和Ingress正确配置
- 无需修改应用配置

---

### 3.13 Demo #13: backup-monitoring

#### 元数据定义
- **名称**: 备份状态监控与告警演示
- **难度**: intermediate
- **关键字**: velero, monitoring, prometheus, alerting, metrics
- **描述**: 演示如何监控Velero备份任务状态并配置告警规则

#### 功能范围
1. 启用Velero Prometheus metrics
2. 配置ServiceMonitor（Prometheus Operator）
3. 创建备份失败告警规则
4. Grafana仪表板展示（可选）
5. 备份状态查询和日志分析

#### 资源清单结构
- `servicemonitor.yaml`: Prometheus监控配置
- `prometheus-rules.yaml`: 备份告警规则
- `grafana-dashboard.json`: Grafana仪表板（可选）

#### 关键指标
- `velero_backup_success_total`: 成功备份总数
- `velero_backup_failure_total`: 失败备份总数
- `velero_backup_duration_seconds`: 备份耗时
- `velero_backup_last_successful_timestamp`: 最后成功时间

#### 告警规则示例
```yaml
- alert: VeleroBackupFailure
  expr: increase(velero_backup_failure_total[1h]) > 0
  annotations:
    summary: "Velero backup failed"
```

#### 验证点
- Prometheus成功抓取Velero metrics
- 告警规则触发测试
- 仪表板显示备份历史趋势
- 日志集成到日志聚合平台

---

### 3.14 Demo #14: volume-snapshot-location

#### 元数据定义
- **名称**: 卷快照位置配置演示
- **难度**: advanced
- **关键字**: velero, volume-snapshot-location, csi, snapshot-provider
- **描述**: 演示如何配置多个VolumeSnapshotLocation以支持不同存储提供商

#### 功能范围
1. 配置默认VolumeSnapshotLocation
2. 配置多个快照位置（如AWS EBS、Azure Disk）
3. 备份时指定快照位置
4. 快照位置的可用性检查

#### 资源清单结构
- `default-vsl.yaml`: 默认快照位置
- `aws-ebs-vsl.yaml`: AWS EBS快照位置
- `azure-disk-vsl.yaml`: Azure Disk快照位置

#### 配置示例（AWS EBS）
```yaml
apiVersion: velero.io/v1
kind: VolumeSnapshotLocation
metadata:
  name: aws-ebs
  namespace: velero
spec:
  provider: aws
  config:
    region: us-west-2
```

#### 验证点
- 多个VolumeSnapshotLocation对象创建成功
- 备份时可选择特定快照位置
- 快照存储在对应的提供商后端
- 跨区域快照复制验证（高级场景）

---

### 3.15 Demo #15: backup-deletion

#### 元数据定义
- **名称**: 备份清理与保留策略演示
- **难度**: beginner
- **关键字**: velero, backup-deletion, retention-policy, storage-management
- **描述**: 演示如何手动删除备份、配置自动清理策略和管理对象存储空间

#### 功能范围
1. 手动删除单个备份
2. 批量删除过期备份
3. 配置TTL自动清理
4. 验证对象存储空间释放
5. 删除保护机制说明

#### 资源清单结构
- `ttl-backup.yaml`: 带TTL的备份定义
- `cleanup-job.yaml`: 清理脚本Job（可选）

#### 删除命令示例
```bash
# 删除单个备份
velero backup delete old-backup

# 删除所有Completed状态的备份
velero backup delete --selector velero.io/phase=Completed

# 查看即将过期的备份
velero backup get --show-labels
```

#### TTL配置
```yaml
spec:
  ttl: 720h  # 30天后自动删除
```

#### 验证点
- 执行删除后备份对象消失
- 对象存储中的备份文件被删除
- TTL到期后备份自动清理
- 删除操作记录在审计日志中

---

## 4. 测试用例设计

### 4.1 测试用例分类

| 测试类别 | 测试目标 | 覆盖Demo |
|---------|---------|---------|
| **安装验证** | Velero组件正常安装 | #1 |
| **功能正确性** | 备份和恢复功能正常 | #2, #3, #5, #6 |
| **策略配置** | 定时任务和过滤规则生效 | #4, #7 |
| **高级场景** | 钩子、加密、跨集群功能 | #10, #11, #12 |
| **运维监控** | 监控指标和告警正常 | #13 |
| **数据一致性** | 恢复后数据完整无损 | #5, #6, #9 |

### 4.2 测试用例详细规格

#### TC-001: Velero基础安装验证
- **对应Demo**: #1 basic-installation
- **前置条件**: 
  - Kubernetes集群可用（minikube或云厂商集群）
  - kubectl已配置并可访问集群
  - Helm 3+已安装
- **测试步骤**:
  1. 执行MinIO部署YAML
  2. 验证MinIO Pod状态为Running
  3. 使用Helm安装Velero（提供values文件）
  4. 检查Velero Pod状态
  5. 执行`velero version`命令
  6. 执行`velero backup-location get`验证存储连接
- **期望结果**:
  - 所有Pod状态为Running
  - Velero CLI输出server和client版本一致
  - BackupStorageLocation状态为Available
- **失败处理**: 查看Pod日志，检查凭证配置是否正确

#### TC-002: 命名空间备份与恢复
- **对应Demo**: #2 namespace-backup
- **前置条件**: 
  - Velero已成功安装（TC-001通过）
  - 存在测试命名空间和示例应用
- **测试步骤**:
  1. 创建nginx-example命名空间和应用
  2. 写入测试数据到ConfigMap
  3. 执行备份命令：`velero backup create test-backup --include-namespaces nginx-example`
  4. 等待备份完成（检查状态为Completed）
  5. 删除nginx-example命名空间
  6. 执行恢复命令：`velero restore create --from-backup test-backup`
  7. 验证命名空间和资源恢复
- **期望结果**:
  - 备份状态显示Completed
  - 恢复后命名空间存在
  - 应用Pod正常运行
  - ConfigMap数据与备份前一致
- **数据验证**: 使用checksum或kubectl diff对比资源

#### TC-003: 持久卷快照功能
- **对应Demo**: #6 pv-snapshot-backup
- **前置条件**:
  - 集群支持CSI快照功能
  - VolumeSnapshotClass已配置
- **测试步骤**:
  1. 部署带PVC的StatefulSet应用
  2. 写入测试文件到PV（例如：`echo "test-data" > /data/test.txt`）
  3. 创建启用快照的备份
  4. 验证VolumeSnapshot对象创建
  5. 删除应用和PVC
  6. 从备份恢复
  7. 验证文件内容一致
- **期望结果**:
  - VolumeSnapshot对象存在且状态为ReadyToUse
  - 恢复后PV挂载成功
  - 文件内容匹配
- **性能指标**: 记录快照创建和恢复时间

#### TC-004: 定时备份任务
- **对应Demo**: #4 scheduled-backup
- **前置条件**: 
  - Velero已安装
  - 存在需要定期备份的命名空间
- **测试步骤**:
  1. 创建Schedule对象（cron表达式设置为每5分钟）
  2. 等待第一次备份触发
  3. 检查自动创建的Backup对象
  4. 修改应用并等待第二次备份
  5. 验证两次备份都成功
  6. 检查TTL策略（设置为10分钟）
  7. 等待过期备份自动删除
- **期望结果**:
  - Schedule对象显示下次执行时间
  - 每次定时触发都成功创建Backup
  - 过期备份被自动清理
- **监控验证**: 查看Prometheus metrics中的备份计数器

#### TC-005: 资源过滤与选择器
- **对应Demo**: #7 resource-filtering
- **前置条件**: 
  - 命名空间中存在多种标签的资源
- **测试步骤**:
  1. 创建带有不同标签的资源（app=critical和app=test）
  2. 执行带标签选择器的备份：`--selector app=critical`
  3. 检查备份描述中的资源列表
  4. 验证仅critical标签的资源被备份
  5. 执行资源类型过滤：`--include-resources deployments,services`
  6. 验证仅指定类型被备份
- **期望结果**:
  - 备份中仅包含匹配标签的资源
  - 未匹配资源不在备份中
  - 资源计数符合预期
- **验证方法**: 使用`velero backup describe --details`查看资源列表

#### TC-006: 跨集群资源迁移
- **对应Demo**: #12 migration-across-clusters
- **前置条件**:
  - 两个独立的Kubernetes集群
  - 两个集群的Velero配置相同的对象存储
- **测试步骤**:
  1. 在源集群创建应用和数据
  2. 在源集群执行备份
  3. 验证备份上传到共享对象存储
  4. 在目标集群安装Velero（相同配置）
  5. 在目标集群执行`velero backup get`同步备份
  6. 执行恢复操作
  7. 验证应用在目标集群正常运行
- **期望结果**:
  - 应用在目标集群功能正常
  - PV数据迁移成功
  - 无需修改应用配置
- **网络验证**: 测试Service和Ingress是否可访问

#### TC-007: 备份钩子执行
- **对应Demo**: #10 backup-hooks
- **前置条件**:
  - 部署支持钩子的应用（如MySQL）
- **测试步骤**:
  1. 配置pre-backup钩子（数据库flush）
  2. 执行备份
  3. 查看Pod日志验证钩子执行
  4. 验证post-backup钩子执行
  5. 恢复备份并验证数据一致性
- **期望结果**:
  - 钩子命令在日志中可见
  - 数据库一致性检查通过
  - 备份期间应用短暂只读
- **失败场景**: 测试钩子超时和失败处理

#### TC-008: 备份数据加密
- **对应Demo**: #11 backup-encryption
- **前置条件**:
  - 准备加密密钥Secret
- **测试步骤**:
  1. 配置启用加密的BackupStorageLocation
  2. 创建包含敏感数据的资源（Secret）
  3. 执行加密备份
  4. 检查对象存储中的备份文件（应无法直接读取）
  5. 使用正确密钥恢复备份
  6. 测试使用错误密钥恢复（应失败）
- **期望结果**:
  - 对象存储中的备份文件已加密
  - 正确密钥可恢复
  - 错误密钥恢复失败并有明确错误提示
- **安全验证**: 使用hex编辑器检查备份文件无明文

#### TC-009: 灾难恢复演练
- **对应Demo**: #9 disaster-recovery-simulation
- **前置条件**:
  - 模拟生产环境应用运行
  - 定时备份策略已配置
- **测试步骤**:
  1. 记录灾难前的应用状态和数据
  2. 模拟灾难（删除关键命名空间）
  3. 记录检测到灾难的时间（T0）
  4. 执行灾难恢复流程
  5. 记录恢复完成时间（T1）
  6. 验证应用功能和数据完整性
  7. 计算RTO和RPO
- **期望结果**:
  - RTO（T1-T0）< 30分钟
  - RPO（数据丢失）< 1小时（基于备份频率）
  - 所有关键服务恢复
  - 数据一致性验证通过
- **性能记录**: 记录每个步骤的耗时

#### TC-010: 备份监控与告警
- **对应Demo**: #13 backup-monitoring
- **前置条件**:
  - Prometheus Operator已安装
  - Grafana已安装（可选）
- **测试步骤**:
  1. 应用ServiceMonitor配置
  2. 验证Prometheus抓取Velero metrics
  3. 查询备份成功和失败计数器
  4. 触发备份失败场景（如存储不可用）
  5. 验证告警触发
  6. 导入Grafana仪表板（可选）
- **期望结果**:
  - Metrics端点可访问
  - Prometheus成功抓取数据
  - 告警规则在失败时触发
  - 仪表板显示备份趋势
- **集成验证**: 测试告警发送到钉钉/Slack

---

### 4.3 自动化测试脚本设计

每个Demo的`code/`目录下提供自动化测试脚本：

#### 脚本结构（示例：test-backup.sh）
```bash
#!/bin/bash
# 自动化测试脚本：命名空间备份与恢复

set -e  # 遇到错误立即退出

# 步骤1: 创建测试命名空间
kubectl create namespace test-backup-ns

# 步骤2: 部署示例应用
kubectl apply -f sample-app.yaml -n test-backup-ns

# 步骤3: 等待应用就绪
kubectl wait --for=condition=Ready pod -l app=nginx -n test-backup-ns --timeout=60s

# 步骤4: 执行备份
velero backup create test-backup --include-namespaces test-backup-ns

# 步骤5: 等待备份完成
while [[ $(velero backup describe test-backup -o json | jq -r '.status.phase') != "Completed" ]]; do
  echo "等待备份完成..."
  sleep 5
done

# 步骤6: 验证备份
RESOURCE_COUNT=$(velero backup describe test-backup --details | grep -c "Deployment\|Service")
if [ "$RESOURCE_COUNT" -lt 2 ]; then
  echo "❌ 备份资源数量不足"
  exit 1
fi

# 步骤7: 删除命名空间
kubectl delete namespace test-backup-ns

# 步骤8: 恢复备份
velero restore create --from-backup test-backup

# 步骤9: 验证恢复
kubectl wait --for=condition=Ready pod -l app=nginx -n test-backup-ns --timeout=120s

echo "✅ 测试通过：备份和恢复成功"

# 清理
velero backup delete test-backup --confirm
kubectl delete namespace test-backup-ns
```

#### 测试脚本规范
- 使用`set -e`确保错误时退出
- 每个步骤添加日志输出
- 使用`kubectl wait`等待资源就绪
- 验证点使用条件判断和明确的成功/失败提示
- 测试结束清理所有资源
- 支持幂等执行（可重复运行）

---

## 5. 测试报告规格

### 5.1 测试报告模板

#### 报告文件位置
每个Demo的根目录下生成`TEST_REPORT.md`文件。

#### 报告内容结构

```markdown
# Velero Demo测试报告

## 测试概要

| 项目 | 值 |
|-----|---|
| Demo名称 | {demo_name} |
| 测试日期 | {date} |
| 测试环境 | Kubernetes {version}, Velero {version} |
| 测试执行者 | {executor} |
| 测试结果 | ✅ 通过 / ❌ 失败 |

## 测试用例执行结果

| 用例ID | 用例名称 | 状态 | 耗时 | 备注 |
|-------|---------|------|-----|------|
| TC-001 | 安装验证 | ✅ 通过 | 120s | - |
| TC-002 | 备份执行 | ✅ 通过 | 45s | - |
| TC-003 | 恢复验证 | ✅ 通过 | 90s | - |

## 详细测试日志

### TC-001: 安装验证

**执行步骤**:
1. 部署MinIO: 成功
2. 安装Velero: 成功
3. 验证连接: 成功

**执行输出**:
```
Client:
        Version: v1.12.0
Server:
        Version: v1.12.0
```

**验证结果**: ✅ 通过

---

## 性能指标

| 指标 | 值 | 目标 | 结果 |
|-----|---|------|------|
| 备份耗时 | 45s | < 60s | ✅ |
| 恢复耗时 | 90s | < 120s | ✅ |
| 数据一致性 | 100% | 100% | ✅ |

## 问题与风险

### 发现的问题
- 无

### 风险评估
- **风险**: CSI快照依赖存储插件支持
- **缓解措施**: 文档中明确CSI要求

## 测试环境信息

```yaml
Kubernetes版本: v1.28.0
Velero版本: v1.12.0
对象存储: MinIO (模拟S3)
存储插件: CSI hostpath
节点数量: 1 (minikube)
```

## 测试结论

本次测试覆盖了Velero的核心功能，所有测试用例均通过验证。Demo可用于生产参考。

**建议**: 在生产环境应使用云厂商的对象存储服务（如AWS S3）替代MinIO。
```

---

### 5.2 自动化报告生成

#### 脚本：generate-test-report.sh
```bash
#!/bin/bash
# 生成测试报告脚本

DEMO_NAME=$1
REPORT_FILE="TEST_REPORT.md"

# 执行测试并捕获输出
TEST_OUTPUT=$(./code/test-*.sh 2>&1)
TEST_RESULT=$?

# 记录测试时间
START_TIME=$(date -Iseconds)
# ... 执行测试 ...
END_TIME=$(date -Iseconds)
DURATION=$((END_TIME - START_TIME))

# 生成报告
cat > $REPORT_FILE <<EOF
# Velero Demo测试报告

## 测试概要

| 项目 | 值 |
|-----|---|
| Demo名称 | $DEMO_NAME |
| 测试日期 | $(date) |
| 测试结果 | $([ $TEST_RESULT -eq 0 ] && echo "✅ 通过" || echo "❌ 失败") |
| 测试耗时 | ${DURATION}s |

## 测试输出

\`\`\`
$TEST_OUTPUT
\`\`\`

EOF

echo "测试报告已生成: $REPORT_FILE"
```

---

## 6. README文档更新规格

### 6.1 README.md更新内容

在主README中的Kubernetes章节添加Velero工具清单：

#### 更新位置
在`⎈ Kubernetes`部分，kubeflow、kubeskoop之后新增velero。

#### 更新内容格式
```markdown
<details>
<summary><b>📦 Velero工具 (15个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/velero/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-installation` | Velero基础安装与配置 | beginner | ✅ |
| 2 | `namespace-backup` | 命名空间级别备份 | beginner | ✅ |
| 3 | `cluster-backup` | 集群级别全量备份 | intermediate | ✅ |
| 4 | `scheduled-backup` | 定时备份策略配置 | intermediate | ✅ |
| 5 | `resource-filtering` | 资源过滤与标签选择器 | intermediate | ✅ |
| 6 | `backup-restore` | 备份恢复完整流程 | beginner | ✅ |
| 7 | `namespace-mapping` | 跨命名空间恢复映射 | intermediate | ✅ |
| 8 | `disaster-recovery-simulation` | 完整灾难恢复演练 | advanced | ✅ |
| 9 | `pv-snapshot-backup` | 持久卷快照备份 | intermediate | ✅ |
| 10 | `volume-snapshot-location` | 卷快照位置配置 | advanced | ✅ |
| 11 | `backup-hooks` | 备份前后钩子操作 | advanced | ✅ |
| 12 | `backup-encryption` | 备份数据加密 | advanced | ✅ |
| 13 | `migration-across-clusters` | 跨集群资源迁移 | advanced | ✅ |
| 14 | `backup-monitoring` | 备份状态监控与告警 | intermediate | ✅ |
| 15 | `backup-deletion` | 备份清理与保留策略 | beginner | ✅ |

**功能覆盖**:
- ✅ 安装部署与基础配置
- ✅ 命名空间和集群级别备份
- ✅ 定时备份与保留策略
- ✅ 持久卷快照与数据恢复
- ✅ 灾难恢复与跨集群迁移
- ✅ 备份钩子与数据加密
- ✅ 监控告警与运维管理

</details>
```

### 6.2 Demo统计表更新

更新主README顶部的统计表：

```markdown
| 语言 | 基础Demo | 第三方库/工具 | 总计 | 测试状态 |
|---------|----------|----------|------|----------|
| ⎈ **Kubernetes** | 0 | kubeflow(42), kubeskoop(10), velero(15), operator-framework(2) | 69 | ✅ 全部通过 |
| **总计** | **210** | **96** | **306** | ✅ |
```

### 6.3 STATUS.md文件更新

如果项目存在STATUS.md跟踪功能状态，应添加：

```markdown
## Velero工具支持 (v1.0.0)

- [x] 基础安装与配置
- [x] 命名空间备份与恢复
- [x] 集群级别备份
- [x] 定时备份策略
- [x] 持久卷快照
- [x] 灾难恢复演练
- [x] 跨集群迁移
- [x] 备份加密
- [x] 监控告警集成
- [x] 完整测试覆盖
```

---

## 7. 实施计划

### 7.1 开发阶段

#### 阶段1: 核心功能Demo (P0优先级)
**时间**: 第1周
- 开发Demo #1: basic-installation
- 开发Demo #2: namespace-backup
- 开发Demo #3: cluster-backup
- 开发Demo #4: scheduled-backup
- 开发Demo #5: backup-restore
- 开发Demo #6: pv-snapshot-backup
- 开发Demo #15: backup-deletion

**交付物**: 7个核心Demo，每个包含完整的README、YAML和测试脚本

#### 阶段2: 扩展功能Demo (P1优先级)
**时间**: 第2周
- 开发Demo #7: resource-filtering
- 开发Demo #8: namespace-mapping
- 开发Demo #9: disaster-recovery-simulation
- 开发Demo #13: backup-monitoring
- 开发Demo #12: migration-across-clusters
- 开发Demo #14: volume-snapshot-location

**交付物**: 6个扩展Demo

#### 阶段3: 高级功能Demo (P2优先级)
**时间**: 第3周
- 开发Demo #10: backup-hooks
- 开发Demo #11: backup-encryption

**交付物**: 2个高级Demo

### 7.2 测试与验证阶段

#### 阶段4: 集成测试
**时间**: 第3周
- 执行所有15个Demo的测试用例
- 生成测试报告
- 修复发现的问题
- 性能基准测试

#### 阶段5: 文档完善
**时间**: 第4周
- 完善每个Demo的README
- 生成统一的测试报告汇总
- 更新主README.md
- 更新STATUS.md

### 7.3 交付清单

#### 最终交付物
1. **15个Velero Demo**，每个包含：
   - `metadata.json`: 元数据文件
   - `README.md`: 详细使用文档
   - `code/`: YAML资源清单和测试脚本
   - `TEST_REPORT.md`: 测试报告

2. **文档更新**：
   - 主`README.md`添加Velero章节
   - 统计数据更新（306个Demo）
   - `STATUS.md`功能跟踪更新

3. **测试报告**：
   - 每个Demo的独立测试报告
   - 汇总测试报告（覆盖率、通过率）

4. **CI集成**（可选）：
   - GitHub Actions工作流验证Demo
   - 自动化测试执行

---

## 8. 验证标准

### 8.1 Demo质量标准

每个Demo必须满足以下标准才能交付：

#### 文档完整性
- [x] README.md包含完整的功能说明
- [x] 环境要求明确（Kubernetes版本、工具依赖）
- [x] 逐步实操指南清晰
- [x] 代码解析和预期输出完整
- [x] 常见问题FAQ覆盖

#### 资源清单质量
- [x] 所有YAML文件语法正确（通过验证器）
- [x] 资源定义遵循最佳实践
- [x] 包含必要的注释和说明
- [x] 命名空间隔离（避免冲突）

#### 测试覆盖
- [x] 提供自动化测试脚本
- [x] 测试脚本幂等且可重复执行
- [x] 验证点明确（成功/失败判断）
- [x] 测试报告自动生成

#### 验证机制对齐
- [x] 通过`demo_verifier.py`的Kubernetes验证逻辑
- [x] 静态YAML语法检查通过
- [x] kubectl和helm工具可用性检查
- [x] Dry-run验证通过（如适用）

### 8.2 集成验证流程

#### 自动化验证步骤
1. **静态检查**: 验证所有YAML文件语法
2. **元数据验证**: 检查metadata.json格式和必填字段
3. **文档检查**: README.md存在且包含关键章节
4. **测试执行**: 运行测试脚本并记录结果
5. **性能检查**: 记录备份和恢复耗时

#### 验证通过标准
- 所有静态检查无错误
- 测试脚本执行成功（退出码0）
- 测试报告显示所有用例通过
- 性能指标在可接受范围内

---

## 9. 风险与缓解措施

### 9.1 技术风险

| 风险 | 影响 | 概率 | 缓解措施 |
|-----|-----|------|---------|
| CSI快照功能依赖存储插件 | 部分Demo无法在所有环境运行 | 中 | 文档明确环境要求；提供备选方案（Restic文件备份） |
| 对象存储配置复杂度 | 用户安装难度大 | 中 | 提供MinIO快速部署方案；多云厂商配置示例 |
| Velero版本兼容性 | 不同版本行为差异 | 低 | 明确测试版本；提供多版本兼容性说明 |
| 跨集群迁移需要多集群环境 | 测试复杂度高 | 中 | 提供minikube多实例方案；云厂商测试集群 |

### 9.2 运维风险

| 风险 | 影响 | 概率 | 缓解措施 |
|-----|-----|------|---------|
| 备份数据占用大量存储 | 成本增加 | 高 | 文档说明TTL策略；提供存储空间监控方案 |
| 恢复时间超出预期 | RTO目标无法满足 | 中 | 性能基准测试；提供优化建议 |
| 加密密钥丢失导致数据不可恢复 | 数据永久丢失 | 低 | 文档强调密钥管理重要性；提供密钥备份方案 |

### 9.3 项目集成风险

| 风险 | 影响 | 概率 | 缓解措施 |
|-----|-----|------|---------|
| Demo结构与现有不一致 | 集成失败 | 低 | 严格遵循kubernetes/<tool>/<demo>结构 |
| 验证流程未覆盖新场景 | CI失败 | 中 | 扩展demo_verifier.py支持Velero特定验证 |
| 文档更新冲突 | 合并问题 | 低 | 预先协调README更新位置 |

---

## 10. 成功标准

### 10.1 功能完整性
- [x] 覆盖Velero官方文档中的核心功能（备份、恢复、定时任务、快照）
- [x] 提供beginner到advanced的完整难度梯度
- [x] 每个功能点至少有一个Demo演示

### 10.2 质量标准
- [x] 所有15个Demo通过自动化验证
- [x] 测试覆盖率达到100%（每个Demo有对应测试用例）
- [x] 文档完整性检查通过（README、metadata、TEST_REPORT）

### 10.3 用户体验
- [x] 用户可通过`opendemo get kubernetes velero`命令列出所有Demo
- [x] 每个Demo可独立运行（依赖明确）
- [x] 平均10分钟内完成单个Demo的部署和验证

### 10.4 社区影响
- [x] README中Kubernetes Demo数量从54增加到69
- [x] 提供生产级灾备方案参考
- [x] 社区用户反馈评分≥4.5/5（如适用）

---

## 11. 附录

### 11.1 Velero架构参考

Velero由以下组件构成：
- **Server**: 运行在Kubernetes集群中的控制器（Deployment）
- **CLI**: 用户命令行工具（velero命令）
- **Plugins**: 对象存储和卷快照插件（AWS、Azure、GCP等）
- **Restic**: 可选的文件级备份工具（集成在Server中）

### 11.2 对象存储后端支持

| 存储类型 | 插件 | Demo中的使用 |
|---------|-----|-------------|
| AWS S3 | velero-plugin-for-aws | 文档中提供配置示例 |
| Azure Blob | velero-plugin-for-microsoft-azure | 文档中提供配置示例 |
| GCP Storage | velero-plugin-for-gcp | 文档中提供配置示例 |
| MinIO | S3兼容API | Demo中默认使用（测试环境） |

### 11.3 参考资料
- Velero官方文档: https://velero.io/docs/
- Velero GitHub仓库: https://github.com/vmware-tanzu/velero
- CSI快照规范: https://kubernetes.io/docs/concepts/storage/volume-snapshots/
- 项目现有Kubernetes Demo: `opendemo_output/kubernetes/kubeskoop/`
