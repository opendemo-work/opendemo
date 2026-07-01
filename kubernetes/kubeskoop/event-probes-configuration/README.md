<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Kubernetes Event Probes 配置演示

## 简介
本演示展示了如何在 Kubernetes 中使用存活探针（liveness probe）和就绪探针（readiness probe）来监控应用的健康状态。这些探针帮助 Kubernetes 决定何时重启容器或何时将流量路由到 Pod。

## 学习目标
- 理解 liveness 和 readiness 探针的作用
- 掌握 HTTP 和命令行探针的配置方法
- 学会调试探针失败问题

## 环境要求
- 操作系统：Windows、Linux 或 macOS
- kubectl >= 1.20
- Minikube >= 1.25（用于本地测试）
- Docker（可选，用于构建镜像）

## 安装依赖步骤
1. 安装 kubectl：https://kubernetes.io/docs/tasks/tools/install-kubectl/
2. 安装 Minikube：https://minikube.sigs.k8s.io/docs/start/
3. 启动集群：`minikube start`

## 文件说明
- `liveness-probe.yaml`：配置基于命令的存活探针
- `readiness-probe.yaml`：配置基于 HTTP 的就绪探针
- `both-probes.yaml`：同时配置两种探针

## 逐步实操指南

### 步骤 1: 启动 Minikube 集群
```bash
minikube start
```
**预期输出**：显示“Kubectl is now configured to use "minikube"”等信息

### 步骤 2: 应用存活探针配置
```bash
kubectl apply -f liveness-probe.yaml
```
**预期输出**：`pod/liveness-demo created`

### 步骤 3: 查看 Pod 状态
```bash
kubectl get pods liveness-demo
```
持续运行直到状态为 Running。若探针失败，Kubernetes 会重启容器。

### 步骤 4: 应用就绪探针配置
```bash
kubectl apply -f readiness-probe.yaml
```
**预期输出**：`pod/readiness-demo created`

### 步骤 5: 查看就绪状态变化
```bash
kubectl get pods readiness-demo
```
开始时 READY 列可能为 0/1，当服务启动后变为 1/1

### 步骤 6: 同时应用两个探针
```bash
kubectl apply -f both-probes.yaml
```
**预期输出**：`pod/both-probes-demo created`

### 步骤 7: 清理资源
```bash
kubectl delete -f liveness-probe.yaml
kubectl delete -f readiness-probe.yaml
kubectl delete -f both-probes.yaml
```

## 代码解析

### liveness-probe.yaml
使用 `exec` 探针执行命令检查文件是否存在。如果 `/tmp/healthy` 不存在，探针失败并触发重启。

### readiness-probe.yaml
使用 HTTP GET 请求探测端口 8080 的 `/health` 路径。只有当返回码在 200-399 之间时才认为准备就绪。

### both-probes.yaml
结合了前两者，定义了独立的存活和就绪逻辑，实现更精细的控制。

## 预期输出示例
```bash
NAME              READY   STATUS    RESTARTS   AGE
liveness-demo     1/1     Running   1          2m
readiness-demo    1/1     Running   0          90s
both-probes-demo  1/1     Running   0          60s
```

## 常见问题解答

**Q: 探针频繁失败怎么办？**
A: 检查初始延迟（initialDelaySeconds）是否足够长，确保应用有时间启动。

**Q: 就绪探针失败会影响什么？**
A: Pod 不会被加入 Service 的 Endpoints，不会接收新流量。

**Q: 存活探针失败会发生什么？**
A: Kubernetes 会杀死容器并根据重启策略重新创建它。

## 扩展学习建议
- 尝试使用 startupProbe 处理慢启动应用
- 配置 TCP 探针用于非 HTTP 服务
- 使用 Prometheus + kube-state-metrics 监控探针行为
## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 Kubernetes 核心概念
- ✅ 掌握相关的资源配置与命令
- ✅ 能够在本地集群中复现

## 🚀 快速开始

### 部署资源

```bash
./scripts/apply.sh
```

### 检查状态

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


---

## 📖 深入理解

### 工作原理

Event Probes Configuration 的核心机制可以概括为以下几个步骤：

1. **初始化阶段**：准备运行环境，加载必要的配置和依赖。
2. **执行阶段**：按照预定的流程执行主要逻辑，处理输入并生成输出。
3. **验证阶段**：检查结果是否符合预期，记录关键指标和日志。
4. **清理阶段**：释放资源，确保环境可以重复运行。

### 关键设计决策

| 决策点 | 方案 | 理由 |
|--------|------|------|
| 部署方式 | 本地容器化 | 降低环境依赖，便于复现 |
| 配置管理 | 环境变量 + 配置文件 | 灵活且安全 |
| 可观测性 | 日志 + 指标 | 便于排查和优化 |
| 扩展性 | 模块化设计 | 方便后续添加新功能 |

### 性能考量

在实际生产环境中使用本案例时，建议关注以下性能指标：

- **响应时间**：确保核心操作在可接受范围内完成。
- **资源占用**：监控 CPU、内存、磁盘和网络使用情况。
- **吞吐量**：根据业务需求评估并发处理能力。
- **错误率**：建立告警机制，及时发现异常。

---

## 🛡️ 安全与最佳实践

### 安全建议

- 不要在生产环境中使用默认密码或密钥。
- 定期更新依赖组件到最新稳定版本。
- 对敏感配置使用密钥管理工具（如 Kubernetes Secrets、Vault）。
- 限制网络暴露面，使用防火墙或安全组控制访问。

### 最佳实践

- 在修改配置前备份现有环境。
- 使用版本控制管理所有配置文件和脚本。
- 编写自动化测试覆盖核心路径。
- 记录运行日志，便于审计和故障排查。

---

## 🧪 进阶实验

完成基础演示后，可以尝试以下进阶实验：

1. **参数调优**：修改关键配置参数，观察对结果的影响。
2. **故障注入**：故意制造错误，验证系统的容错能力。
3. **压力测试**：增加负载，评估系统瓶颈。
4. **集成测试**：将本案例与其他组件组合，构建完整链路。

---

## 📚 扩展资源

### 官方文档

- [相关技术官方文档](https://example.com)
- [OpenDemo 项目主页](https://github.com/opendemo)

### 推荐书籍

- 《相关技术权威指南》
- 《云原生架构实践》

### 社区与论坛

- Stack Overflow 相关标签
- GitHub Discussions
- 技术博客与公众号

---

## 🤝 贡献与反馈

如果你发现本案例有任何问题，或希望补充更多内容，欢迎提交 Issue 或 Pull Request。

---

*本 README 为 OpenDemo 五星案例标准模板，请根据实际案例内容持续完善。*
