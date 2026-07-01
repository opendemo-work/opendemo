<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Kubernetes Loki 日志管理基础案例

## 什么是 Loki？

Loki 是一个水平可扩展、高可用性、多租户的日志聚合系统，由 Grafana 团队开发。它专为云原生环境设计，特别适合与 Kubernetes 集成。

Loki 主要由两部分组成：
- **Loki**: 日志存储和查询引擎
- **Promtail**: 日志收集代理，部署在每个节点上，负责收集容器日志并发送到 Loki

## 本案例包含的内容

- **loki.yaml**: Loki 部署配置
- **promtail.yaml**: Promtail DaemonSet 配置

## 快速开始

### 1. 部署 Loki

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl apply -f loki.yaml
```

### 2. 验证 Loki 部署

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 检查 Loki Pod 状态
kubectl get pods -n loki -l app=loki

# 等待 Loki 就绪
kubectl wait --for=condition=ready pod -l app=loki -n loki --timeout=300s
```

### 3. 部署 Promtail

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl apply -f promtail.yaml
```

### 4. 验证 Promtail 部署

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 检查 Promtail Pod 状态
kubectl get pods -n loki -l app=promtail
```

### 5. 与 Grafana 集成

Loki 通常与 Grafana 一起使用，用于日志可视化。以下是如何将 Loki 添加到 Grafana 中：

#### 5.1 确保 Grafana 已部署

如果还没有部署 Grafana，可以使用之前的 Grafana 案例进行部署。

#### 5.2 添加 Loki 数据源

1. 登录 Grafana UI
2. 点击左侧菜单栏的 **Configuration** > **Data Sources**
3. 点击 **Add data source**
4. 选择 **Loki**
5. 在 **URL** 字段中输入：`http://loki.loki:3100`
6. 点击 **Save & Test**

## 基本使用

### 1. 在 Grafana 中查询日志

1. 登录 Grafana UI
2. 点击左侧菜单栏的 **Explore**
3. 在顶部的数据源下拉菜单中选择 **Loki**
4. 使用 Loki 查询语言 (LogQL) 查询日志

### 2. LogQL 查询示例

#### 2.1 查询特定命名空间的日志

```
{namespace="default"}
```

#### 2.2 查询特定 Pod 的日志

```
{namespace="default", pod="my-pod"}
```

#### 2.3 查询包含特定关键词的日志

```
{namespace="default"} |= "error"
```

#### 2.4 查询特定时间段的日志

使用 Grafana 界面上的时间选择器，或者在查询中使用范围修饰符：

```
{namespace="default"}[1h] |= "warning"
```

#### 2.5 按容器过滤日志

```
{namespace="default", container="nginx"}
```

### 3. 查看 Loki 指标

Loki 提供了自身的监控指标，可以通过 Prometheus 进行监控：

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 端口转发 Loki 指标端口
kubectl port-forward svc/loki 3100:3100 -n loki

# 访问指标
curl http://localhost:3100/metrics
```

## 清理资源

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
kubectl delete -f promtail.yaml
kubectl delete -f loki.yaml
```

## Loki vs ELK/EFK

| 特性 | Loki | ELK/EFK |
|------|------|---------|
| 存储方式 | 索引标签，日志内容作为纯文本 | 全文索引 |
| 资源消耗 | 轻量 | 较重 |
| 查询语言 | LogQL（类 PromQL） | Elasticsearch Query DSL |
| 集成性 | 与 Grafana 无缝集成 | 需要 Kibana |
| 部署复杂度 | 简单 | 复杂 |
| 扩展性 | 水平扩展 | 水平扩展 |

## 扩展建议

1. **添加持久化存储**: 将 Loki 的存储从 emptyDir 改为 PersistentVolumeClaim
2. **配置高可用性**: 部署多个 Loki 实例，使用分布式存储后端
3. **调整保留策略**: 配置日志保留时间，避免存储过大
4. **添加告警规则**: 结合 Prometheus 和 Alertmanager 实现日志告警
5. **使用 Loki 分布式模式**: 部署独立的读、写和后端组件

## 相关链接

- [Loki 官方文档](https://grafana.com/docs/loki/latest/)
- [Promtail 官方文档](https://grafana.com/docs/loki/latest/clients/promtail/)
- [LogQL 查询语言](https://grafana.com/docs/loki/latest/logql/)
- [Grafana 官方文档](https://grafana.com/docs/)
- [Kubernetes 日志管理最佳实践](https://kubernetes.io/docs/concepts/cluster-administration/logging/)

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
