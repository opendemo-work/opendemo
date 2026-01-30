# 完整灾难恢复演练

## 简介
模拟完整的灾难场景，演示灾难恢复的完整流程和RTO/RPO测量。本Demo是Velero系列演示的一部分，展示Velero的高级备份和恢复能力。

## 学习目标
- 理解完整灾难恢复演练的核心概念
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
