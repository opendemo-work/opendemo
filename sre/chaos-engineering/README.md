# 混沌工程 - 通过故障注入提升系统韧性

> 使用 Chaos Mesh 或 Litmus 在 Kubernetes 上进行故障注入实验，验证系统的容错能力和恢复机制。

---

## 📋 目录

- [🎯 学习目标](#-学习目标)
- [📐 架构图](#-架构图)
- [🚀 快速开始](#-快速开始)
- [📖 核心概念](#-核心概念)
- [💻 代码示例](#-代码示例)
- [🔧 配置说明](#-配置说明)
- [🧪 验证测试](#-验证测试)
- [📊 运行结果](#-运行结果)
- [🐛 常见问题](#-常见问题)
- [📚 扩展学习](#-扩展学习)

---

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解混沌工程的原则和价值
- ✅ 设计合理的故障注入实验
- ✅ 使用 Chaos Mesh 进行 Pod 故障、网络延迟实验
- ✅ 分析实验结果并制定改进措施

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    混沌工程实验流程                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   定义稳态假设 ──▶ 注入故障 ──▶ 观察指标 ──▶ 分析结果          │
│        │              │              │              │          │
│        ▼              ▼              ▼              ▼          │
│   服务 SLO 正常    Pod 终止       延迟/错误率     改进措施      │
│   吞吐稳定         网络分区       可用性变化      修复缺陷      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

```bash
cd sre/chaos-engineering
./scripts/start.sh
./scripts/check.sh
```

---

## 📖 核心概念

### 1. 混沌工程原则

- 建立稳态假设
- 模拟真实世界事件
- 生产环境运行
- 持续自动化运行
- 最小化爆炸半径

### 2. 常见故障类型

| 类型 | 说明 |
|------|------|
| Pod Failure | 随机终止 Pod |
| Network Latency | 注入网络延迟 |
| Network Partition | 网络分区 |
| CPU/Memory Stress | 资源压力测试 |
| DNS Chaos | DNS 故障 |

### 3. 安全边界

- 从小范围开始
- 设定自动回滚条件
- 确保有止损机制
- 非工作时间谨慎实验

---

## 💻 代码示例

### Chaos Mesh Pod Failure 实验

```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: pod-failure-example
  namespace: chaos-testing
spec:
  action: pod-failure
  mode: one
  duration: "30s"
  selector:
    namespaces:
      - default
    labelSelectors:
      app: nginx
```

### 网络延迟实验

```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: network-delay-example
spec:
  action: delay
  mode: all
  selector:
    namespaces:
      - default
  delay:
    latency: "100ms"
    correlation: "100"
    jitter: "0ms"
```

---

## 🧪 验证测试

```bash
# 应用混沌实验
kubectl apply -f experiments/pod-failure.yaml

# 观察应用状态
kubectl get pods -w

# 查看实验结果
kubectl describe podchaos pod-failure-example
```

---

## 📚 扩展学习

- [SLO/SLI 管理](../slo-sli-management/)
- [灰度发布](../canary-deployment/)
- [Chaos Mesh 官方文档](https://chaos-mesh.org/docs/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*


---

## 📖 深入理解

### 工作原理

Chaos Engineering 的核心机制可以概括为以下几个步骤：

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
