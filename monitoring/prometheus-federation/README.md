# Prometheus 联邦集群演示

> 使用 Prometheus Federation 将多个 Prometheus 实例的指标聚合到全局 Prometheus，演示分级监控架构和指标聚合查询。

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

- ✅ 理解 Prometheus Federation 的使用场景
- ✅ 部署多个 Prometheus 实例并配置联邦抓取
- ✅ 使用 `honor_labels` 和 `metrics_path` 控制指标聚合行为
- ✅ 设计分级监控架构

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Prometheus 联邦架构                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐         ┌──────────────┐                    │
│   │ Prometheus A │         │ Prometheus B │                    │
│   │  (华东机房)   │         │  (华北机房)   │                    │
│   │  抓取本地指标 │         │  抓取本地指标 │                    │
│   └──────┬───────┘         └──────┬───────┘                    │
│          │                        │                             │
│          └────────┬───────────────┘                             │
│                   │ federation                                   │
│                   ▼                                              │
│          ┌──────────────┐                                       │
│          │ Global Prom  │                                       │
│          │  (全局聚合)   │                                       │
│          └──────────────┘                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd monitoring/prometheus-federation
./scripts/start.sh
sleep 10
./scripts/check.sh
```

访问：
- Prometheus A: http://localhost:9091
- Prometheus B: http://localhost:9092
- Global Prometheus: http://localhost:9090

---

## 📖 核心概念

### 1. Federation 使用场景

- **可扩展性**：避免单个 Prometheus 抓取过多目标
- **多租户/多区域**：每个区域独立部署，全局统一查看
- **数据汇总**：将多个实例的关键指标聚合到全局视图

### 2. Federation 抓取配置

```yaml
scrape_configs:
  - job_name: 'federate'
    scrape_interval: 15s
    honor_labels: true
    metrics_path: '/federate'
    params:
      'match[]':
        - '{job="prometheus"}'
        - '{__name__=~"job:.*"}'
    static_configs:
      - targets:
        - 'prometheus-a:9090'
        - 'prometheus-b:9090'
```

### 3. match[] 参数

控制要聚合的指标：

- `{job="prometheus"}`：抓取所有 job 为 prometheus 的指标
- `{__name__=~"job:.*"}`：抓取名称匹配正则的指标
- `{__name__=~"up|prometheus_build_info"}`：只抓取指定指标

---

## 💻 代码示例

### 全局 Prometheus 配置

```yaml
# configs/prometheus-global.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'federate'
    scrape_interval: 15s
    honor_labels: true
    metrics_path: '/federate'
    params:
      'match[]':
        - '{job="node"}'
    static_configs:
      - targets:
        - 'prometheus-a:9090'
        - 'prometheus-b:9090'
```

### 区域 Prometheus 配置

```yaml
# configs/prometheus-a.yml
scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter-a:9100']
```

---

## 🧪 验证测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 查询全局 Prometheus 是否能获取各区域指标
curl -s "http://localhost:9090/api/v1/query?query=up"

# 查看 federation 目标状态
curl -s http://localhost:9090/api/v1/targets | python3 -m json.tool
```

---

## 📊 运行结果

在 Global Prometheus 中查询 `up`，可以看到来自多个区域的 target 状态。

---

## 🐛 常见问题

### Q1：联邦抓取没有数据？

**A**：检查 `match[]` 参数是否正确匹配了被联邦实例中的指标。

### Q2：标签冲突？

**A**：使用 `honor_labels: true` 保留原始标签，或配置 `relabel_configs` 添加区域前缀。

---

## 📚 扩展学习

- [Prometheus 指标收集演示](../prometheus-metrics-collection/)
- [Prometheus Federation 官方文档](https://prometheus.io/docs/prometheus/latest/federation/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
