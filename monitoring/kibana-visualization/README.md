# Kibana 可视化图表演示

> 在 Elasticsearch + Kibana 基础上，创建柱状图、饼图、折线图等多种可视化图表，构建日志分析 Dashboard。

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

- ✅ 在 Kibana 中创建多种类型的可视化
- ✅ 配置聚合（Aggregation）和分桶（Bucket）
- ✅ 将多个可视化组合成 Dashboard
- ✅ 保存和分享可视化结果

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Kibana 可视化架构                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Elasticsearch ──▶ Kibana Lens/Viz ──▶ Dashboard              │
│   (日志数据)         (可视化配置)         (仪表盘)               │
│                                                                 │
│              ┌────────────────────────┐                        │
│              │ 状态码分布 / 响应时间   │                        │
│              │ Top URL / 时间趋势     │                        │
│              │ 地理分布 / 热力图       │                        │
│              └────────────────────────┘                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

```bash
cd monitoring/kibana-visualization
./scripts/start.sh
sleep 30
./scripts/check.sh
```

访问 Kibana：

```
http://localhost:5601
```

---

## 📖 核心概念

### 1. Lens

Kibana 7.12+ 引入的可视化编辑器，支持拖拽式创建图表。

### 2. Aggregation

- **Metrics Aggregation**：对字段进行计算，如 Count、Average、Sum、Max、Min
- **Bucket Aggregation**：对数据进行分组，如 Date Histogram、Terms、Range

### 3. Dashboard

多个 Visualization 的集合，支持：

- 时间范围筛选
- 全局搜索过滤
- 图表联动

---

## 💻 代码示例

### 使用 Aggregation API 查询

```bash
# 按状态码统计请求数
curl -s -X POST "localhost:9200/nginx-logs-*/_search" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "status_codes": {
      "terms": {
        "field": "status"
      }
    }
  }
}' | python3 -m json.tool
```

### 可视化配置要点

| 图表类型 | 用途 | 典型配置 |
|----------|------|----------|
| Vertical Bar | 状态码分布 | X: status Terms, Y: Count |
| Line | 请求趋势 | X: timestamp Date Histogram, Y: Count |
| Pie | 方法占比 | Split slices: method Terms |
| Data Table | Top URL | Rows: path Terms, Metrics: Count/Avg response_time |

---

## 🧪 验证测试

```bash
# 检查 Kibana 状态
curl -s http://localhost:5601/api/status

# 查看已保存的可视化对象
curl -s http://localhost:5601/api/saved_objects/_find?type=visualization | python3 -m json.tool
```

---

## 📚 扩展学习

- [Kibana 日志分析](../kibana-log-analysis/)
- [Grafana 自定义仪表盘](../grafana-dashboard-custom/)
- [Kibana 可视化文档](https://www.elastic.co/guide/en/kibana/current/visualize.html)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*


---

## 📊 Kibana 可视化类型选择指南

| 场景 | 推荐图表 | 说明 |
|------|----------|------|
| 时间趋势 | Line / Area | 展示指标随时间变化 |
| 占比分布 | Pie / Donut | 展示各部分占总体的比例 |
| 排名对比 | Horizontal Bar | 展示 Top N 数据 |
| 明细查看 | Data Table | 展示原始数据或聚合明细 |
| 地理分布 | Maps | 展示地理位置相关数据 |
| 异常检测 | Heatmap | 通过颜色深浅发现异常 |

选择合适的可视化类型能够更清晰地传达数据洞察。
