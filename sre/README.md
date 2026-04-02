# Site Reliability Engineering (SRE)

包含10个案例：SRE基础、SLO/SLI管理、错误预算、混沌工程、事件管理、容量规划

## SRE核心领域

```
SRE知识体系:
┌─────────────────────────────────────────────────────────┐
│                    SRE Practices                         │
├─────────────────────────────────────────────────────────┤
│  Observability    │ Chaos Engineering │ Incident Mgmt  │
│  (可观测性)        │   (混沌工程)       │  (事件管理)     │
├─────────────────────────────────────────────────────────┤
│  Capacity Planning │ Error Budgets    │ Automation      │
│  (容量规划)        │   (错误预算)      │  (自动化)       │
├─────────────────────────────────────────────────────────┤
│  SLI/SLO/SLA      │ Postmortems      │ Release Eng     │
│  (服务级别)        │   (事后分析)      │  (发布工程)     │
└─────────────────────────────────────────────────────────┘
```

## 目录结构

| 案例 | 描述 | 难度 |
|------|------|------|
| sre-fundamentals | SRE基础与核心原则 | 入门 |
| slo-sli-management | 服务级别目标管理 | 中级 |
| error-budget | 错误预算与发布策略 | 中级 |
| chaos-engineering | 混沌工程实践 | 高级 |
| incident-management | 事件管理与响应 | 中级 |
| postmortem-analysis | 事后分析与复盘 | 中级 |
| capacity-planning | 容量规划与预测 | 高级 |
| runbook-automation | 运行手册自动化 | 中级 |
| canary-deployment | 金丝雀发布策略 | 高级 |
| feature-flags | 特性开关管理 | 中级 |

## 与现有内容的关系

- **monitoring/**: 基础监控工具使用
- **kubernetes/**: 云原生可观测性 (Prometheus, Grafana, Jaeger, Loki)
- **sre/**: SRE方法论与实践流程

