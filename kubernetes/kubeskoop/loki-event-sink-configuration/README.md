<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Loki日志事件接收器配置演示

## 简介
本演示展示了如何在Kubernetes集群中部署并配置Grafana Loki作为日志聚合系统，使应用能够将日志发送至Loki进行集中存储与查询。通过本示例，您将学习到Loki的基本架构、日志路径配置以及Promtail的部署方法。

## 学习目标
- 理解Loki在Kubernetes中的角色与优势
- 掌握使用Helm部署Loki和Promtail的方法
- 配置Pod日志自动收集并发送至Loki
- 查询和验证日志是否成功摄入

## 环境要求
- `kubectl` >= 1.20
- `helm` >= 3.0.0
- Kubernetes 集群（Minikube、Kind、EKS、AKS等均可）
- 可选：`minikube` >= 1.0.0（用于本地测试）

## 安装依赖的详细步骤

### 1. 安装kubectl
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# Linux/macOS
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Windows: 下载 https://dl.k8s.io/release/v1.29.0/bin/windows/amd64/kubectl.exe
```

### 2. 安装Helm
🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### 3. 启动Kubernetes集群（以Minikube为例）
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
minikube start --memory=4096 --cpus=2
```

## 文件说明
- `loki-values.yaml`: Helm自定义配置文件，用于定制Loki部署参数
- `promtail-config.yaml`: Promtail的配置文件，定义日志采集规则

## 逐步实操指南

### 步骤1：添加Grafana Helm仓库
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

**预期输出**：`"grafana" has been added to your repositories`

### 步骤2：部署Loki
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
helm install loki grafana/loki --version 5.30.1 -f loki-values.yaml
```

**预期输出**：显示Loki服务、StatefulSet等资源创建成功

### 步骤3：部署Promtail
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
helm install promtail grafana/promtail --version 6.16.2 -f promtail-config.yaml
```

**预期输出**：Promtail DaemonSet 和 ConfigMap 创建成功

### 步骤4：验证Pod状态
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
kubectl get pods -l app=loki
kubectl get pods -l app=promtail
```

**预期输出**：所有Pod处于 `Running` 状态

### 步骤5：查看日志摄入情况
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
kubectl logs -l app=promtail --tail=10
```

应看到类似 `level=info msg="Sending batch of entries" ...` 的日志，表示日志已发送至Loki

## 代码解析

### `loki-values.yaml`
- 设置 `ingester.replication_factor: 1` 适用于单节点环境
- 启用 `auth_enabled: false` 简化本地测试流程
- 使用 `inmemory` 作为索引存储，适合演示

### `promtail-config.yaml`
- `clients.url`: 指向Loki服务的内部ClusterIP地址
- `scrape_configs.job_name: kubernetes-pods`: 自动发现所有命名空间的Pod日志
- `pipeline_stages`: 提取Pod标签作为日志流标签（如job, namespace, pod）

## 预期输出示例
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
$ kubectl get svc loki
NAME   TYPE        CLUSTER-IP      PORT(S)
loki   ClusterIP   10.96.123.45    3100/TCP

$ kubectl logs promtail-abcde
... level=info msg="Starting Promtail" ...
... level=info msg="Sending batch" ...
```

## 常见问题解答

**Q: Promtail无法连接Loki？**
A: 检查服务名称是否为`loki`且在同一命名空间，或使用FQDN `loki.default.svc.cluster.local`

**Q: 日志未出现在Loki中？**
A: 查看Promtail日志是否有错误；确认容器日志路径为`/var/log/pods/*/*/*.log`

**Q: 如何查询Loki中的日志？**
A: 使用`logcli`工具或部署Grafana并添加Loki数据源进行可视化查询

## 扩展学习建议
- 将Loki与Grafana集成实现日志仪表板
- 使用持久化存储（如S3、GCS）替换内存存储
- 配置RBAC和多租户支持用于生产环境
- 实现日志保留策略和压缩设置

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 Kubernetes 核心概念
- ✅ 掌握相关的资源配置与命令
- ✅ 能够在本地集群中复现

## 🚀 快速开始

### 部署资源

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/apply.sh
```

### 检查状态

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/check.sh
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的 Kubernetes 核心概念。

### 2. 适用场景

- 场景 1：开发与测试
- 场景 2：生产环境参考
- 场景 3：故障排查

## 💻 代码示例

### 基本命令

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际场景替换
kubectl apply -f manifests/
```


---

## 📚 扩展阅读

### 相关概念

- 概念 1：补充说明
- 概念 2：补充说明
- 概念 3：补充说明

### 常见问题

#### Q1：本案例适用于哪些场景？

**A**：本案例适用于学习、实验和工程参考。

#### Q2：如何验证运行结果？

**A**：按照 README 中的命令执行，并观察输出是否符合预期。

#### Q3：遇到问题时如何排查？

**A**：检查环境依赖是否正确安装，查看命令输出和日志信息。

### 推荐资源

- [OpenDemo 官方文档](https://github.com/opendemo)
- [相关技术官方文档](https://example.com)

### 进阶主题

- [ ] 进阶主题 1
- [ ] 进阶主题 2
- [ ] 进阶主题 3

---

*本 README 为自动生成模板，请根据实际案例内容补充完善。*
