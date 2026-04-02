# SLI/SLO Management

服务级别指标(SLI)与服务级别目标(SLO)管理实践。

## 核心概念

```
服务水平层次:
┌─────────────────────────────────────────────────────────┐
│  SLA - Service Level Agreement                          │
│  服务级别协议 - 对用户的承诺，具有法律效力                │
├─────────────────────────────────────────────────────────┤
│  SLO - Service Level Objective                          │
│  服务级别目标 - 内部目标，驱动可靠性工作                  │
├─────────────────────────────────────────────────────────┤
│  SLI - Service Level Indicator                          │
│  服务级别指标 - 可量化的可靠性度量                        │
└─────────────────────────────────────────────────────────┘
```

## SLI定义方法

### 四大黄金指标
```yaml
# 黄金指标定义
golden_signals:
  latency:
    description: 请求处理时间
    types:
      - p50: 中位数延迟
      - p95: 95分位延迟
      - p99: 99分位延迟
    collection: |
      histogram_quantile(0.95, 
        sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
      )
  
  traffic:
    description: 系统负载/请求量
    metrics:
      - requests_per_second
      - concurrent_connections
      - bandwidth_usage
  
  errors:
    description: 错误率
    calculation: |
      rate(http_requests_total{status=~"5.."}[5m]) / 
      rate(http_requests_total[5m])
  
  saturation:
    description: 资源饱和度
    metrics:
      - cpu_utilization
      - memory_utilization
      - disk_io_utilization
```

## SLO目标设定

### 分级策略
```yaml
# SLO分级定义
tiers:
  critical:
    services: [payment, auth]
    availability: 99.99%
    latency_p99: 100ms
    error_rate: 0.01%
    
  standard:
    services: [catalog, search]
    availability: 99.9%
    latency_p99: 500ms
    error_rate: 0.1%
    
  best_effort:
    services: [analytics, reporting]
    availability: 99%
    latency_p99: 2000ms
    error_rate: 1%
```

## 实现与监控

### Prometheus规则
```yaml
groups:
  - name: slo_recording_rules
    rules:
      # 可用性SLI
      - record: slo:availability:ratio_rate5m
        expr: |
          sum(rate(http_requests_total{status!~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))
      
      # 错误预算消耗
      - record: slo:error_budget:burn_rate
        expr: |
          (
            1 - slo:availability:ratio_rate1h
          ) / (1 - 0.9995)
```

## 学习要点

1. SLI选择的四个黄金信号
2. SLO目标设定的实践经验
3. 错误预算计算方法
4. 多窗口告警策略
