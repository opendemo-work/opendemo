# Grafana 自定义仪表盘演示

> 通过 Docker 部署 Grafana，连接 Prometheus 数据源，从零构建一个包含多种可视化面板的自定义监控仪表盘。

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

- ✅ 配置 Grafana 数据源
- ✅ 创建自定义 Dashboard 和 Panel
- ✅ 使用 PromQL 查询指标并可视化
- ✅ 导出和导入 Dashboard JSON 配置

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Grafana Dashboard 架构                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Prometheus ──▶ Grafana ──▶ Dashboard                          │
│   (指标源)        (可视化)      (多个 Panel)                     │
│                                                                 │
│              ┌──────────────────────────┐                      │
│              │ CPU 使用率 / 内存使用 /    │                      │
│              │ 磁盘 I/O / 网络流量 /      │                      │
│              │ 自定义业务指标            │                      │
│              └──────────────────────────┘                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

```bash
cd monitoring/grafana-dashboard-custom
./scripts/start.sh
sleep 15
./scripts/check.sh
```

访问 Grafana：

```
http://localhost:3000
admin/admin
```

---

## 📖 核心概念

### 1. Dashboard

一组相关 Panel 的集合，可以按业务、系统或团队组织。

### 2. Panel

单个可视化组件，支持多种类型：

- Time series：时序图
- Stat：单值统计
- Table：表格
- Gauge：仪表盘
- Pie chart：饼图
- Heatmap：热力图

### 3. PromQL 示例

```promql
# CPU 使用率
100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# 内存使用率
100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))

# 磁盘使用率
100 * (1 - node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})
```

---

## 💻 代码示例

### Dashboard JSON 片段

```json
{
  "dashboard": {
    "title": "OpenDemo Node Monitoring",
    "panels": [
      {
        "title": "CPU Usage",
        "type": "timeseries",
        "targets": [
          {
            "expr": "100 - (avg(irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
            "legendFormat": "CPU %"
          }
        ]
      }
    ]
  }
}
```

### 通过 API 导入 Dashboard

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -u admin:admin \
  http://localhost:3000/api/dashboards/db \
  -d @configs/dashboard.json
```

---

## 🔧 配置说明

| 文件 | 作用 |
|------|------|
| `configs/datasources.yml` | 自动配置 Prometheus 数据源 |
| `configs/dashboard.json` | 自定义仪表盘 JSON |
| `docker-compose.yml` | Grafana + Prometheus 服务编排 |

---

## 🧪 验证测试

```bash
# 检查数据源是否配置成功
curl -s -u admin:admin http://localhost:3000/api/datasources | python3 -m json.tool

# 检查 Dashboard 是否导入
curl -s -u admin:admin http://localhost:3000/api/search | python3 -m json.tool
```

---

## 📚 扩展学习

- [Grafana 告警通知](../grafana-alerting/)
- [Prometheus 指标收集](../prometheus-metrics-collection/)
- [Grafana Dashboard 官方文档](https://grafana.com/docs/grafana/latest/dashboards/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
