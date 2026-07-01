# Kibana 日志分析演示

> 使用 Docker Compose 部署 Elasticsearch + Kibana，导入 Nginx 访问日志，演示日志搜索、过滤、字段提取和分析。

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

- ✅ 使用 Docker 部署 Elasticsearch 和 Kibana
- ✅ 创建 Index Pattern 并导入日志数据
- ✅ 使用 KQL（Kibana Query Language）搜索日志
- ✅ 进行日志聚合分析，发现异常模式

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    ELK 日志分析架构                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   日志文件 ──▶ Elasticsearch ──▶ Kibana                         │
│   (nginx.log)     (索引/搜索)      (可视化分析)                  │
│                                                                 │
│              ┌──────────────────────┐                          │
│              │ Index: nginx-logs-*  │                          │
│              │ 分词/字段映射         │                          │
│              └──────────────────────┘                          │
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
cd monitoring/kibana-log-analysis
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

### 1. Index 和 Index Pattern

- **Index**：Elasticsearch 中存储数据的逻辑空间
- **Index Pattern**：Kibana 中用于匹配多个 Index 的模式，如 `nginx-logs-*`

### 2. KQL

Kibana Query Language，简化版查询语法：

```kql
status:200 AND path:/api
method:GET
response_time > 100
```

### 3. 字段提取

通过 Ingest Pipeline 或 Logstash 对原始日志进行解析，提取结构化字段：

```json
{
  "timestamp": "2026-06-27T10:00:00Z",
  "client_ip": "192.168.1.1",
  "method": "GET",
  "path": "/api/users",
  "status": 200,
  "response_time": 45
}
```

---

## 💻 代码示例

### 创建索引并导入数据

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 创建索引
curl -X PUT "localhost:9200/nginx-logs-2026.06.27" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "timestamp": { "type": "date" },
      "client_ip": { "type": "ip" },
      "method": { "type": "keyword" },
      "path": { "type": "keyword" },
      "status": { "type": "integer" },
      "response_time": { "type": "integer" }
    }
  }
}'

# 插入示例日志
curl -X POST "localhost:9200/nginx-logs-2026.06.27/_doc" -H 'Content-Type: application/json' -d'
{
  "timestamp": "2026-06-27T10:00:00Z",
  "client_ip": "192.168.1.1",
  "method": "GET",
  "path": "/api/users",
  "status": 200,
  "response_time": 45
}'
```

### KQL 查询示例

```kql
status >= 500
method:POST AND path:/api/orders
response_time > 1000
```

---

## 🔧 配置说明

| 文件 | 作用 |
|------|------|
| `docker-compose.yml` | Elasticsearch + Kibana 服务编排 |
| `data/nginx.log` | 示例 Nginx 访问日志 |
| `code/import.py` | 日志导入脚本 |

---

## 🧪 验证测试

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 检查 Elasticsearch 健康状态
curl -s http://localhost:9200/_cluster/health

# 查看索引
curl -s http://localhost:9200/_cat/indices?v

# 搜索日志
curl -s http://localhost:9200/nginx-logs-*/_search?q=status:500
```

---

## 📚 扩展学习

- [Kibana 可视化图表](../kibana-visualization/)
- [Grafana 自定义仪表盘](../grafana-dashboard-custom/)
- [Elasticsearch 官方文档](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
