# Prometheus 告警规则演示

> 通过 Docker Compose 部署 Prometheus，配置告警规则（Recording Rules + Alerting Rules），演示 CPU 使用率告警和磁盘空间告警的完整流程。

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

- ✅ 理解 Prometheus Alerting Rules 和 Recording Rules 的区别
- ✅ 编写 YAML 格式的告警规则文件
- ✅ 配置 Prometheus 加载告警规则并查看告警状态
- ✅ 使用 Alertmanager 路由和静默告警

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Prometheus 告警架构                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Node Exporter ──▶ Prometheus ──▶ Alertmanager ──▶ 通知渠道   │
│   (指标数据)         (评估规则)      (路由/去重)       (邮件/钉钉)│
│                       │                                        │
│                       ▼                                        │
│              ┌─────────────────┐                              │
│              │  Alerting Rules │                              │
│              │  Recording Rules│                              │
│              └─────────────────┘                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Docker | >= 20.10 | 运行 Prometheus 容器 |
| Docker Compose | >= 1.29 | 编排服务 |

### 启动服务

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd monitoring/prometheus-alerting
./scripts/start.sh
sleep 10
./scripts/check.sh
```

### 访问 Prometheus UI

```
http://localhost:9090
```

在 Status → Rules 中查看告警规则，在 Alerts 中查看当前告警状态。

---

## 📖 核心概念

### 1. Alerting Rules

定义在什么条件下触发告警。例如：

```yaml
groups:
  - name: node_alerts
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is above 80% for more than 2 minutes."
```

### 2. Recording Rules

预先计算常用或复杂的 PromQL 表达式，将结果保存为新的时间序列，提升查询性能。

```yaml
groups:
  - name: node_recording
    rules:
      - record: job:node_cpu_usage:avg5m
        expr: 100 - (avg by(job) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

### 3. Alertmanager

负责接收 Prometheus 发送的告警，进行：

- 分组（Grouping）
- 抑制（Inhibition）
- 静默（Silences）
- 路由到不同通知渠道

---

## 💻 代码示例

### CPU 告警规则

```yaml
# configs/alerts.yml
groups:
  - name: cpu_alerts
    rules:
      - alert: HighCPUUsage
        expr: |
          100 - (
            avg by (instance) (
              irate(node_cpu_seconds_total{mode="idle"}[5m])
            ) * 100
          ) > 80
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Instance {{ $labels.instance }} high CPU usage"
          description: "CPU usage is {{ $value }}% for more than 2 minutes."
```

### 磁盘空间告警

```yaml
      - alert: DiskSpaceLow
        expr: |
          (
            node_filesystem_avail_bytes{mountpoint="/"}
            /
            node_filesystem_size_bytes{mountpoint="/"}
          ) * 100 < 20
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Disk space low on {{ $labels.instance }}"
          description: "Available disk space is {{ $value }}%."
```

### Prometheus 配置加载规则

```yaml
# prometheus.yml
rule_files:
  - "alerts.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
```

---

## 🔧 配置说明

| 文件 | 作用 |
|------|------|
| `configs/prometheus.yml` | Prometheus 主配置 |
| `configs/alerts.yml` | 告警规则文件 |
| `configs/alertmanager.yml` | Alertmanager 路由配置 |
| `docker-compose.yml` | 服务编排 |

---

## 🧪 验证测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 1. 检查 Prometheus 是否加载规则
curl -s http://localhost:9090/api/v1/rules | python3 -m json.tool

# 2. 手动触发一个告警（模拟高 CPU）
curl -s http://localhost:9090/api/v1/query?query='up'

# 3. 查看当前告警
curl -s http://localhost:9090/api/v1/alerts | python3 -m json.tool
```

---

## 📊 运行结果

在 Prometheus UI 的 Alerts 页面可以看到：

- `HighCPUUsage` 规则（状态：pending / firing）
- `DiskSpaceLow` 规则（状态：pending / firing）

如果配置了 Alertmanager，可以在 http://localhost:9093 看到告警列表。

---

## 🐛 常见问题

### Q1：告警规则语法错误？

**A**：使用 Prometheus UI 的 Status → Rules 查看解析错误，或检查日志。

### Q2：告警一直处于 pending 不触发 firing？

**A**：检查 `for` 字段设置，告警需要持续满足条件达到该时长才会 firing。

### Q3：Alertmanager 没有收到告警？

**A**：检查 `alerting.alertmanagers` 配置中的地址是否正确，以及网络是否可达。

---

## 📚 扩展学习

- [Prometheus 指标收集演示](../prometheus-metrics-collection/)
- [Grafana 告警通知演示](../grafana-alerting/)
- [Prometheus Alerting 官方文档](https://prometheus.io/docs/alerting/latest/overview/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
