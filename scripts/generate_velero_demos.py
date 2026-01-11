#!/usr/bin/env python3
"""
批量生成Velero Demo的metadata.json和README.md文件
"""
import json
import os
from datetime import datetime

# Demo配置列表
demos = [
    {
        "name": "namespace-backup",
        "title": "命名空间级别备份演示",
        "difficulty": "beginner",
        "keywords": ["velero", "backup", "namespace", "restore", "kubernetes"],
        "description": "演示如何使用Velero备份指定命名空间的所有资源并进行恢复验证"
    },
    {
        "name": "cluster-backup",
        "title": "集群级别全量备份演示",
        "difficulty": "intermediate",
        "keywords": ["velero", "cluster-backup", "full-backup", "disaster-recovery", "kubernetes"],
        "description": "演示如何执行集群级别全量备份，包括CRD资源和持久卷"
    },
    {
        "name": "scheduled-backup",
        "title": "定时备份策略配置演示",
        "difficulty": "intermediate",
        "keywords": ["velero", "schedule", "cron", "automated-backup", "kubernetes"],
        "description": "演示如何创建定时备份计划，并配置备份保留策略"
    },
    {
        "name": "backup-restore",
        "title": "备份恢复完整流程演示",
        "difficulty": "beginner",
        "keywords": ["velero", "restore", "recovery", "validation", "kubernetes"],
        "description": "演示完整的备份→删除→恢复流程，重点展示恢复验证方法"
    },
    {
        "name": "pv-snapshot-backup",
        "title": "持久卷快照备份演示",
        "difficulty": "intermediate",
        "keywords": ["velero", "volume-snapshot", "csi", "persistent-volume", "kubernetes"],
        "description": "演示如何使用CSI快照功能备份持久卷数据"
    },
    {
        "name": "resource-filtering",
        "title": "资源过滤与选择器演示",
        "difficulty": "intermediate",
        "keywords": ["velero", "label-selector", "resource-filter", "selective-backup", "kubernetes"],
        "description": "演示如何使用标签选择器、资源类型过滤等实现精细化备份"
    },
    {
        "name": "namespace-mapping",
        "title": "跨命名空间恢复映射演示",
        "difficulty": "intermediate",
        "keywords": ["velero", "namespace-mapping", "restore", "multi-tenancy", "kubernetes"],
        "description": "演示如何将备份的资源恢复到不同的命名空间"
    },
    {
        "name": "disaster-recovery-simulation",
        "title": "完整灾难恢复演练",
        "difficulty": "advanced",
        "keywords": ["velero", "disaster-recovery", "rto", "rpo", "failover"],
        "description": "模拟完整的灾难场景，演示灾难恢复的完整流程和RTO/RPO测量"
    },
    {
        "name": "backup-hooks",
        "title": "备份钩子操作演示",
        "difficulty": "advanced",
        "keywords": ["velero", "hooks", "pre-backup", "post-backup", "database-consistency"],
        "description": "演示如何使用备份钩子在备份前后执行自定义操作"
    },
    {
        "name": "backup-encryption",
        "title": "备份数据加密演示",
        "difficulty": "advanced",
        "keywords": ["velero", "encryption", "security", "kms", "sensitive-data"],
        "description": "演示如何启用备份数据加密，保护敏感资源"
    },
    {
        "name": "migration-across-clusters",
        "title": "跨集群资源迁移演示",
        "difficulty": "advanced",
        "keywords": ["velero", "cluster-migration", "multi-cluster", "workload-portability", "kubernetes"],
        "description": "演示如何使用Velero在不同Kubernetes集群间迁移工作负载"
    },
    {
        "name": "backup-monitoring",
        "title": "备份状态监控与告警演示",
        "difficulty": "intermediate",
        "keywords": ["velero", "monitoring", "prometheus", "alerting", "metrics"],
        "description": "演示如何监控Velero备份任务状态并配置告警规则"
    },
    {
        "name": "volume-snapshot-location",
        "title": "卷快照位置配置演示",
        "difficulty": "advanced",
        "keywords": ["velero", "volume-snapshot-location", "csi", "snapshot-provider", "kubernetes"],
        "description": "演示如何配置多个VolumeSnapshotLocation以支持不同存储提供商"
    },
    {
        "name": "backup-deletion",
        "title": "备份清理与保留策略演示",
        "difficulty": "beginner",
        "keywords": ["velero", "backup-deletion", "retention-policy", "storage-management", "kubernetes"],
        "description": "演示如何手动删除备份、配置自动清理策略和管理对象存储空间"
    }
]

base_path = r"C:\Users\Allen\Documents\GitHub\opendemo-cli\opendemo_output\kubernetes\velero"

for demo in demos:
    demo_path = os.path.join(base_path, demo["name"])
    
    # 创建metadata.json
    metadata = {
        "name": demo["title"],
        "language": "kubernetes",
        "keywords": demo["keywords"],
        "description": demo["description"],
        "difficulty": demo["difficulty"],
        "author": "",
        "created_at": "2026-01-11T23:45:00.000000",
        "updated_at": "2026-01-11T23:45:00.000000",
        "version": "1.0.0",
        "dependencies": {
            "kubernetes": ">=1.20",
            "velero": ">=1.12"
        },
        "verified": False
    }
    
    metadata_file = os.path.join(demo_path, "metadata.json")
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    # 创建简化的README.md
    readme_content = f"""# {demo["title"]}

## 简介
{demo["description"]}。本Demo是Velero系列演示的一部分，展示Velero的高级备份和恢复能力。

## 学习目标
- 理解{demo["title"]}的核心概念
- 掌握Velero相关功能的实际操作
- 学会验证备份和恢复的正确性

## 环境要求
- Kubernetes集群 >= v1.20
- Velero >= v1.12（已安装并配置，参考basic-installation演示）
- kubectl >= v1.20

> **前置条件**: 请确保已完成`basic-installation` Demo，Velero已正常安装和配置。

## 文件说明
- `code/*.yaml`: Kubernetes资源清单文件
- `code/*.sh`: 自动化测试和演示脚本

## 快速开始

### 步骤1: 验证Velero环境

```bash
# 检查Velero状态
kubectl get pods -n velero
velero version

# 检查备份存储位置
velero backup-location get
```

### 步骤2: 执行Demo

请参考`code/`目录下的具体YAML文件和脚本，按照注释说明逐步操作。

### 步骤3: 验证结果

根据具体场景验证备份和恢复的正确性。

## 常见问题

### Q: 如何查看详细的备份信息？
A: 使用命令 `velero backup describe <backup-name> --details`

### Q: 恢复失败怎么办？
A: 查看恢复日志 `velero restore logs <restore-name>` 和Velero Pod日志

## 参考资料
- [Velero官方文档](https://velero.io/docs/v1.12/)
- [Velero GitHub](https://github.com/vmware-tanzu/velero)

## 相关Demo
- `basic-installation`: Velero基础安装与配置
- 其他Velero系列Demo

---
> 注: 本Demo为演示目的，生产环境请根据实际需求调整配置。
"""
    
    readme_file = os.path.join(demo_path, "README.md")
    if not os.path.exists(readme_file):  # 只创建不存在的README
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    print(f"✓ Created files for {demo['name']}")

print(f"\n✅ Successfully generated files for {len(demos)} demos")
#!/usr/bin/env python3
"""
批量生成Velero Demo的metadata.json和README.md文件
"""
import json
import os
from datetime import datetime

# Demo配置列表
demos = [
    {
        "name": "namespace-backup",
        "title": "命名空间级别备份演示",
        "difficulty": "beginner",
        "keywords": ["velero", "backup", "namespace", "restore", "kubernetes"],
        "description": "演示如何使用Velero备份指定命名空间的所有资源并进行恢复验证"
    },
    {
        "name": "cluster-backup",
        "title": "集群级别全量备份演示",
        "difficulty": "intermediate",
        "keywords": ["velero", "cluster-backup", "full-backup", "disaster-recovery", "kubernetes"],
        "description": "演示如何执行集群级别全量备份，包括CRD资源和持久卷"
    },
    {
        "name": "scheduled-backup",
        "title": "定时备份策略配置演示",
        "difficulty": "intermediate",
        "keywords": ["velero", "schedule", "cron", "automated-backup", "kubernetes"],
        "description": "演示如何创建定时备份计划，并配置备份保留策略"
    },
    {
        "name": "backup-restore",
        "title": "备份恢复完整流程演示",
        "difficulty": "beginner",
        "keywords": ["velero", "restore", "recovery", "validation", "kubernetes"],
        "description": "演示完整的备份→删除→恢复流程，重点展示恢复验证方法"
    },
    {
        "name": "pv-snapshot-backup",
        "title": "持久卷快照备份演示",
        "difficulty": "intermediate",
        "keywords": ["velero", "volume-snapshot", "csi", "persistent-volume", "kubernetes"],
        "description": "演示如何使用CSI快照功能备份持久卷数据"
    },
    {
        "name": "resource-filtering",
        "title": "资源过滤与选择器演示",
        "difficulty": "intermediate",
        "keywords": ["velero", "label-selector", "resource-filter", "selective-backup", "kubernetes"],
        "description": "演示如何使用标签选择器、资源类型过滤等实现精细化备份"
    },
    {
        "name": "namespace-mapping",
        "title": "跨命名空间恢复映射演示",
        "difficulty": "intermediate",
        "keywords": ["velero", "namespace-mapping", "restore", "multi-tenancy", "kubernetes"],
        "description": "演示如何将备份的资源恢复到不同的命名空间"
    },
    {
        "name": "disaster-recovery-simulation",
        "title": "完整灾难恢复演练",
        "difficulty": "advanced",
        "keywords": ["velero", "disaster-recovery", "rto", "rpo", "failover"],
        "description": "模拟完整的灾难场景，演示灾难恢复的完整流程和RTO/RPO测量"
    },
    {
        "name": "backup-hooks",
        "title": "备份钩子操作演示",
        "difficulty": "advanced",
        "keywords": ["velero", "hooks", "pre-backup", "post-backup", "database-consistency"],
        "description": "演示如何使用备份钩子在备份前后执行自定义操作"
    },
    {
        "name": "backup-encryption",
        "title": "备份数据加密演示",
        "difficulty": "advanced",
        "keywords": ["velero", "encryption", "security", "kms", "sensitive-data"],
        "description": "演示如何启用备份数据加密，保护敏感资源"
    },
    {
        "name": "migration-across-clusters",
        "title": "跨集群资源迁移演示",
        "difficulty": "advanced",
        "keywords": ["velero", "cluster-migration", "multi-cluster", "workload-portability", "kubernetes"],
        "description": "演示如何使用Velero在不同Kubernetes集群间迁移工作负载"
    },
    {
        "name": "backup-monitoring",
        "title": "备份状态监控与告警演示",
        "difficulty": "intermediate",
        "keywords": ["velero", "monitoring", "prometheus", "alerting", "metrics"],
        "description": "演示如何监控Velero备份任务状态并配置告警规则"
    },
    {
        "name": "volume-snapshot-location",
        "title": "卷快照位置配置演示",
        "difficulty": "advanced",
        "keywords": ["velero", "volume-snapshot-location", "csi", "snapshot-provider", "kubernetes"],
        "description": "演示如何配置多个VolumeSnapshotLocation以支持不同存储提供商"
    },
    {
        "name": "backup-deletion",
        "title": "备份清理与保留策略演示",
        "difficulty": "beginner",
        "keywords": ["velero", "backup-deletion", "retention-policy", "storage-management", "kubernetes"],
        "description": "演示如何手动删除备份、配置自动清理策略和管理对象存储空间"
    }
]

base_path = r"C:\Users\Allen\Documents\GitHub\opendemo-cli\opendemo_output\kubernetes\velero"

for demo in demos:
    demo_path = os.path.join(base_path, demo["name"])
    
    # 创建metadata.json
    metadata = {
        "name": demo["title"],
        "language": "kubernetes",
        "keywords": demo["keywords"],
        "description": demo["description"],
        "difficulty": demo["difficulty"],
        "author": "",
        "created_at": "2026-01-11T23:45:00.000000",
        "updated_at": "2026-01-11T23:45:00.000000",
        "version": "1.0.0",
        "dependencies": {
            "kubernetes": ">=1.20",
            "velero": ">=1.12"
        },
        "verified": False
    }
    
    metadata_file = os.path.join(demo_path, "metadata.json")
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    # 创建简化的README.md
    readme_content = f"""# {demo["title"]}

## 简介
{demo["description"]}。本Demo是Velero系列演示的一部分，展示Velero的高级备份和恢复能力。

## 学习目标
- 理解{demo["title"]}的核心概念
- 掌握Velero相关功能的实际操作
- 学会验证备份和恢复的正确性

## 环境要求
- Kubernetes集群 >= v1.20
- Velero >= v1.12（已安装并配置，参考basic-installation演示）
- kubectl >= v1.20

> **前置条件**: 请确保已完成`basic-installation` Demo，Velero已正常安装和配置。

## 文件说明
- `code/*.yaml`: Kubernetes资源清单文件
- `code/*.sh`: 自动化测试和演示脚本

## 快速开始

### 步骤1: 验证Velero环境

```bash
# 检查Velero状态
kubectl get pods -n velero
velero version

# 检查备份存储位置
velero backup-location get
```

### 步骤2: 执行Demo

请参考`code/`目录下的具体YAML文件和脚本，按照注释说明逐步操作。

### 步骤3: 验证结果

根据具体场景验证备份和恢复的正确性。

## 常见问题

### Q: 如何查看详细的备份信息？
A: 使用命令 `velero backup describe <backup-name> --details`

### Q: 恢复失败怎么办？
A: 查看恢复日志 `velero restore logs <restore-name>` 和Velero Pod日志

## 参考资料
- [Velero官方文档](https://velero.io/docs/v1.12/)
- [Velero GitHub](https://github.com/vmware-tanzu/velero)

## 相关Demo
- `basic-installation`: Velero基础安装与配置
- 其他Velero系列Demo

---
> 注: 本Demo为演示目的，生产环境请根据实际需求调整配置。
"""
    
    readme_file = os.path.join(demo_path, "README.md")
    if not os.path.exists(readme_file):  # 只创建不存在的README
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    print(f"✓ Created files for {demo['name']}")

print(f"\n✅ Successfully generated files for {len(demos)} demos")
