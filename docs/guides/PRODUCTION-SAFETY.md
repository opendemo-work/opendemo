# OpenDemo 生产环境安全使用指南

> 本指南面向计划将 OpenDemo 案例用于生产环境或接近生产环境学习的用户，帮助你在学习、测试、演示过程中规避误操作风险。

---

## 🎯 适用范围

OpenDemo 中的案例主要设计用于：

- ✅ 本地开发机 / 个人学习环境
- ✅ 隔离的虚拟机（VM）
- ✅ 容器化测试环境（Docker / Kind / Minikube）
- ✅ 专门的测试/预发布 Kubernetes 集群

**不推荐**直接在以下环境执行案例中的命令：

- ❌ 生产业务服务器
- ❌ 生产 Kubernetes 集群
- ❌ 共享的 CI/CD 构建节点
- ❌ 含有真实用户数据的数据库实例

---

## 🛡️ 风险等级说明

项目中所有可执行命令均已按以下三级模型标注：

| 等级 | 徽章 | 含义 | 建议操作 |
|------|------|------|----------|
| 🔴 高风险 | `🔴 高风险` | 可能导致数据丢失、服务中断、权限提升或不可逆破坏 | 必须在隔离环境验证，生产环境禁止直接执行 |
| 🟡 中风险 | `🟡 中风险` | 会修改系统状态、安装软件、启动/停止服务或创建/删除资源 | 先在测试环境验证，确认影响范围后再执行 |
| 🟢 低风险 | `🟢 低风险` | 只读查询或 harmless 信息展示，不会修改系统状态 | 可安全在学习环境中执行 |

> 风险标注基于命令内容的静态启发式分析，仅供参考。具体风险仍需结合实际执行环境和业务上下文判断。

---

## ⚠️ 常见高风险命令类型

### 1. 数据删除与格式化

```bash
rm -rf /path/to/data
mkfs.ext4 /dev/sdb
dd if=/dev/zero of=/dev/sda
```

**风险**：数据永久丢失。  
**缓解措施**：
- 执行前使用 `ls` 或 `df` 再次确认目标路径/设备。
- 确保已备份关键数据。
- 禁止在生产服务器上运行格式化命令。

### 2. Kubernetes 资源删除

```bash
kubectl delete namespace <namespace>
kubectl delete -f <manifest.yaml>
kubectl delete pods --all
```

**风险**：删除运行中的工作负载、服务、配置或命名空间，导致服务中断。  
**缓解措施**：
- 先用 `kubectl config current-context` 确认当前集群。
- 使用 `--dry-run=client` 或 `kubectl diff` 预览变更。
- 删除前确认标签选择器和命名空间范围。

### 3. 系统服务停止/重启

```bash
sudo systemctl restart kubelet
sudo systemctl stop docker
```

**风险**：影响节点或容器运行时可用性。  
**缓解措施**：
- 在维护窗口内执行。
- 优先在测试节点验证。
- 确保有回滚或重启方案。

### 4. 网络与防火墙变更

```bash
sudo iptables -F
sudo ufw --force reset
```

**风险**：清空防火墙规则可能导致服务暴露或不可访问。  
**缓解措施**：
- 先备份现有规则：`sudo iptables-save > iptables.bak`。
- 在隔离网络环境中验证。

### 5. 管道执行远程脚本

```bash
curl -fsSL https://example.com/install.sh | bash
```

**风险**：执行未经验证的远程代码，可能导致恶意软件安装或信息泄露。  
**缓解措施**：
- 先下载脚本到本地并审阅内容。
- 校验脚本来源和校验和（checksum）。
- 在沙箱环境中首次运行。

---

## 🔧 推荐的安全实践

### 1. 使用隔离环境

```bash
# 使用 Docker / Podman 创建隔离容器
docker run -it --rm ubuntu:22.04 bash

# 或使用 Kind / Minikube 创建隔离 K8s 集群
kind create cluster --name opendemo-test
```

### 2. 执行前预览变更

```bash
# Kubernetes：先 diff 再 apply
kubectl diff -f manifest.yaml
kubectl apply -f manifest.yaml

# Terraform：先 plan 再 apply
terraform plan
terraform apply
```

### 3. 备份与快照

```bash
# 虚拟机快照
virsh snapshot-create-as vm-name snapshot-before-test

# 数据库备份
mysqldump -u root -p db_name > db_backup.sql

# Kubernetes 资源备份
kubectl get all -n namespace -o yaml > namespace-backup.yaml
```

### 4. 最小权限原则

- 避免使用 `root` 或集群管理员权限运行学习案例。
- 使用具有最小必要权限的账号/ServiceAccount。
- 不要在命令中硬编码密码、API Key 或 Token。

### 5. 版本与来源校验

```bash
# 校验下载文件的 checksum
sha256sum -c file.sha256

# 确认软件包签名
rpm -K package.rpm
```

---

## 🚨 应急处理

如果误在生产环境执行了高风险命令：

1. **立即停止操作**，不要继续执行后续命令。
2. **评估影响范围**：
   - 删除了哪些资源/数据？
   - 影响了哪些服务/用户？
3. **启动恢复流程**：
   - 从备份恢复数据。
   - 使用版本控制回滚配置（`kubectl rollout undo`、`git revert` 等）。
   - 重新创建被删除的资源。
4. **通知相关团队**并按照组织的事件管理流程处理。
5. **事后复盘**：记录原因、影响和改进措施，避免再次发生。

---

## 📚 相关资源

- [项目根 README](../../README.md)
- [命令风险规则配置](../../configs/command-risk-rules.json)
- [命令风险标注报告](../../docs/reports/COMMAND-RISK-ASSESSMENT-REPORT.md)
- [五星案例结构校验脚本](../../scripts/quality/validate_five_star.py)

---

*最后更新：2026-07-01*  
*维护者：OpenDemo Team*
