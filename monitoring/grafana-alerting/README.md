# Grafana 告警通知演示

> 通过 Docker 部署 Grafana，配置告警规则、联系点和通知策略，演示当 Prometheus 指标触发阈值时如何通过邮件或 Webhook 发送告警通知。

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

- ✅ 理解 Grafana Alerting 的统一告警模型
- ✅ 配置 Contact Points（联系点）
- ✅ 创建 Alert Rules 并绑定 Notification Policies
- ✅ 使用 Webhook 接收 Grafana 告警

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Grafana Alerting 架构                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Prometheus ──▶ Grafana Alerting ──▶ Contact Points            │
│   (指标源)        (告警评估/路由)      (邮件/Webhook/钉钉)       │
│                                                                 │
│              ┌─────────────────┐                               │
│              │ Alert Rules     │                               │
│              │ Notification    │                               │
│              │ Policies        │                               │
│              └─────────────────┘                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

```bash
cd monitoring/grafana-alerting
./scripts/start.sh
sleep 15
./scripts/check.sh
```

访问 Grafana UI：

```
http://localhost:3000
默认账号：admin/admin
```

---

## 📖 核心概念

### 1. Alert Rules

基于查询条件定义告警。Grafana 支持多种数据源：Prometheus、InfluxDB、Loki、Elasticsearch 等。

### 2. Contact Points

告警通知的接收端，支持：

- Email
- Slack
- Webhook
- DingTalk / WeCom
- PagerDuty

### 3. Notification Policies

决定告警如何路由到不同的 Contact Points，支持基于标签的路由。

---

## 💻 代码示例

### 使用 Provisioning 配置告警

```yaml
# configs/alerting/alert-rules.yaml
apiVersion: 1
groups:
  - orgId: 1
    name: node_alerts
    folder: OpenDemo
    interval: 60s
    rules:
      - uid: high-cpu
        title: High CPU Usage
        condition: B
        data:
          - refId: A
            relativeTimeRange:
              from: 300
              to: 0
            datasourceUid: prometheus
            model:
              expr: 100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        noDataState: NoData
        execErrState: Error
        for: 2m
        annotations:
          summary: High CPU usage detected
        labels:
          severity: warning
```

### Webhook 告警 Payload 示例

```json
{
  "receiver": "webhook-receiver",
  "status": "firing",
  "alerts": [
    {
      "status": "firing",
      "labels": {
        "alertname": "HighCPUUsage",
        "severity": "warning"
      },
      "annotations": {
        "summary": "CPU usage is high"
      },
      "startsAt": "2026-06-27T10:00:00Z"
    }
  ]
}
```

---

## 🧪 验证测试

```bash
# 检查 Grafana 健康状态
curl -s http://localhost:3000/api/health

# 查看已配置的告警规则
curl -s -u admin:admin http://localhost:3000/api/alert-rules | python3 -m json.tool
```

---

## 📚 扩展学习

- [Grafana 自定义仪表盘](../grafana-dashboard-custom/)
- [Prometheus 告警规则](../prometheus-alerting/)
- [Grafana Alerting 文档](https://grafana.com/docs/grafana/latest/alerting/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
