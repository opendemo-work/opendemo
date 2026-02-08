# Monitoring 技术栈命名大全

本文件定义了监控系统中各类指标、告警、仪表板等的标准命名规范，特别针对生产环境中的问题排查和解决方案场景。

## 一、监控指标命名规范

### 1.1 系统指标命名
```prometheus
# CPU相关指标
system_cpu_usage_percentage{instance="web-server-01", mode="user"}  # 系统-CPU-使用率-百分比
system_cpu_usage_percentage{instance="web-server-01", mode="system"}
system_cpu_usage_percentage{instance="web-server-01", mode="idle"}
system_cpu_cores_total{instance="web-server-01"}  # 系统-CPU-核心-总数

# 内存相关指标
system_memory_usage_bytes{instance="web-server-01", type="used"}  # 系统-内存-使用-字节
system_memory_usage_bytes{instance="web-server-01", type="free"}
system_memory_usage_bytes{instance="web-server-01", type="cached"}
system_memory_total_bytes{instance="web-server-01"}  # 系统-内存-总计-字节

# 磁盘相关指标
system_disk_usage_percentage{instance="web-server-01", device="/dev/sda1", mountpoint="/"}  # 系统-磁盘-使用率-百分比
system_disk_io_reads_total{instance="web-server-01", device="sda"}  # 系统-磁盘-IO-读取-总计
system_disk_io_writes_total{instance="web-server-01", device="sda"}  # 系统-磁盘-IO-写入-总计
system_disk_space_available_bytes{instance="web-server-01", mountpoint="/var/log"}  # 系统-磁盘空间-可用-字节

# 网络相关指标
system_network_receive_bytes_total{instance="web-server-01", interface="eth0"}  # 系统-网络-接收-字节-总计
system_network_transmit_bytes_total{instance="web-server-01", interface="eth0"}  # 系统-网络-发送-字节-总计
system_network_packets_received_total{instance="web-server-01", interface="eth0"}  # 系统-网络-数据包-接收-总计
system_network_packets_transmitted_total{instance="web-server-01", interface="eth0"}  # 系统-网络-数据包-发送-总计
```

### 1.2 应用指标命名
```prometheus
# HTTP请求指标
http_requests_total{service="web-app", method="GET", endpoint="/api/users", status="200"}  # HTTP-请求-总计
http_requests_total{service="web-app", method="POST", endpoint="/api/users", status="400"}
http_request_duration_seconds{service="web-app", method="GET", endpoint="/api/users", quantile="0.5"}  # HTTP-请求-持续时间-秒
http_request_duration_seconds{service="web-app", method="GET", endpoint="/api/users", quantile="0.95"}
http_request_duration_seconds{service="web-app", method="GET", endpoint="/api/users", quantile="0.99"}

# 应用性能指标
application_response_time_seconds{service="web-app", operation="user_lookup"}  # 应用-响应时间-秒
application_throughput_requests_per_second{service="web-app", endpoint="/api/users"}  # 应用-吞吐量-每秒请求数
application_error_rate_percentage{service="web-app", endpoint="/api/users"}  # 应用-错误率-百分比
application_concurrent_users_total{service="web-app"}  # 应用-并发用户-总计

# 数据库指标
database_connections_active_total{service="web-app", database="postgresql"}  # 数据库-连接-活跃-总计
database_queries_executed_total{service="web-app", database="postgresql", query_type="select"}  # 数据库-查询-执行-总计
database_query_duration_seconds{service="web-app", database="postgresql", query_type="select", quantile="0.95"}  # 数据库-查询-持续时间-秒
database_connection_pool_usage_percentage{service="web-app", pool="primary"}  # 数据库-连接池-使用率-百分比

# 缓存指标
cache_hits_total{service="web-app", cache="redis", operation="get"}  # 缓存-命中-总计
cache_misses_total{service="web-app", cache="redis", operation="get"}  # 缓存-未命中-总计
cache_hit_rate_percentage{service="web-app", cache="redis"}  # 缓存-命中率-百分比
cache_memory_usage_bytes{service="web-app", cache="redis"}  # 缓存-内存使用-字节
```

### 1.3 业务指标命名
```prometheus
# 用户行为指标
business_user_registrations_total{service="user-service", source="web"}  # 业务-用户-注册-总计
business_user_logins_total{service="auth-service", method="password"}  # 业务-用户-登录-总计
business_user_sessions_active_total{service="session-service"}  # 业务-用户-会话-活跃-总计
business_user_engagement_score{service="analytics-service", user_id="12345"}  # 业务-用户-参与度-分数

# 订单指标
business_orders_created_total{service="order-service", order_type="standard"}  # 业务-订单-创建-总计
business_orders_completed_total{service="order-service", order_type="standard"}  # 业务-订单-完成-总计
business_order_value_usd_total{service="order-service"}  # 业务-订单-价值-美元-总计
business_cart_abandonment_rate_percentage{service="cart-service"}  # 业务-购物车-放弃率-百分比

# 支付费指标
business_payments_processed_total{service="payment-service", payment_method="credit_card"}  # 业务-支付-处理-总计
business_payment_success_rate_percentage{service="payment-service"}  # 业务-支付-成功率-百分比
business_payment_amount_usd_total{service="payment-service"}  # 业务-支付-金额-美元-总计
business_refund_amount_usd_total{service="payment-service"}  # 业务-退款-金额-美元-总计
```

## 二、告警规则命名规范

### 2.1 系统告警规则
```yaml
# CPU告警
- alert: HighCPUUsage
  expr: system_cpu_usage_percentage{mode!="idle"} > 80
  for: 5m
  labels:
    severity: warning
    category: system
    team: operations
  annotations:
    summary: "High CPU usage detected on {{ $labels.instance }}"
    description: "CPU usage is {{ $value }}% on {{ $labels.instance }}"

- alert: CriticalCPUUsage
  expr: system_cpu_usage_percentage{mode!="idle"} > 95
  for: 2m
  labels:
    severity: critical
    category: system
    team: operations
  annotations:
    summary: "Critical CPU usage on {{ $labels.instance }}"
    description: "CPU usage is critically high at {{ $value }}% on {{ $labels.instance }}"

# 内存告警
- alert: HighMemoryUsage
  expr: (system_memory_usage_bytes{type="used"} / system_memory_total_bytes) * 100 > 85
  for: 5m
  labels:
    severity: warning
    category: system
    team: operations
  annotations:
    summary: "High memory usage on {{ $labels.instance }}"
    description: "Memory usage is {{ $value }}% on {{ $labels.instance }}"

# 磁盘告警
- alert: LowDiskSpace
  expr: system_disk_usage_percentage > 90
  for: 5m
  labels:
    severity: warning
    category: system
    team: operations
  annotations:
    summary: "Low disk space on {{ $labels.instance }}:{{ $labels.mountpoint }}"
    description: "Disk usage is {{ $value }}% on {{ $labels.mountpoint }} of {{ $labels.instance }}"

- alert: CriticalDiskSpace
  expr: system_disk_usage_percentage > 95
  for: 2m
  labels:
    severity: critical
    category: system
    team: operations
  annotations:
    summary: "Critical disk space on {{ $labels.instance }}:{{ $labels.mountpoint }}"
    description: "Disk usage is critically high at {{ $value }}% on {{ $labels.mountpoint }} of {{ $labels.instance }}"
```

### 2.2 应用告警规则
```yaml
# HTTP服务告警
- alert: HighHttpErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
  for: 2m
  labels:
    severity: warning
    category: application
    team: backend
  annotations:
    summary: "High HTTP error rate for {{ $labels.service }}"
    description: "Error rate is {{ $value }} for service {{ $labels.service }}"

- alert: HighLatency
  expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
  for: 1m
  labels:
    severity: warning
    category: application
    team: backend
  annotations:
    summary: "High latency for {{ $labels.service }}"
    description: "95th percentile latency is {{ $value }}s for service {{ $labels.service }}"

# 数据库告警
- alert: DatabaseConnectionExhaustion
  expr: database_connections_active_total / database_connections_max_total > 0.9
  for: 3m
  labels:
    severity: critical
    category: database
    team: database
  annotations:
    summary: "Database connection pool nearly exhausted for {{ $labels.service }}"
    description: "Connection pool usage is {{ $value }}% for service {{ $labels.service }}"

- alert: SlowDatabaseQueries
  expr: histogram_quantile(0.95, rate(database_query_duration_seconds_bucket[5m])) > 2
  for: 2m
  labels:
    severity: warning
    category: database
    team: database
  annotations:
    summary: "Slow database queries detected for {{ $labels.service }}"
    description: "95th percentile query duration is {{ $value }}s for service {{ $labels.service }}"

# 缓存告警
- alert: LowCacheHitRate
  expr: cache_hit_rate_percentage < 70
  for: 5m
  labels:
    severity: warning
    category: cache
    team: backend
  annotations:
    summary: "Low cache hit rate for {{ $labels.service }}"
    description: "Cache hit rate is {{ $value }}% for service {{ $labels.service }}"
```

### 2.3 业务告警规则
```yaml
# 业务指标告警
- alert: UnusualUserRegistrationDrop
  expr: business_user_registrations_total - business_user_registrations_total offset 1d > 0.3 * business_user_registrations_total offset 1d
  for: 15m
  labels:
    severity: warning
    category: business
    team: growth
  annotations:
    summary: "Significant drop in user registrations"
    description: "User registrations dropped by {{ $value }}% compared to yesterday"

- alert: PaymentProcessingIssues
  expr: business_payment_success_rate_percentage < 95
  for: 5m
  labels:
    severity: critical
    category: business
    team: payments
  annotations:
    summary: "Payment processing issues detected"
    description: "Payment success rate is {{ $value }}%, below threshold of 95%"

- alert: HighOrderCancellationRate
  expr: (business_orders_cancelled_total / business_orders_created_total) * 100 > 15
  for: 10m
  labels:
    severity: warning
    category: business
    team: operations
  annotations:
    summary: "High order cancellation rate"
    description: "Order cancellation rate is {{ $value }}%, unusually high"
```

## 三、仪表板命名规范

### 3.1 系统仪表板
```json
{
  "dashboard": {
    "title": "System Overview Dashboard",
    "uid": "system-overview-main",
    "tags": ["system", "infrastructure", "overview"],
    "panels": [
      {
        "title": "CPU Usage by Instance",
        "type": "graph",
        "targets": [
          {
            "expr": "system_cpu_usage_percentage{mode!='idle'}",
            "legendFormat": "{{instance}} - {{mode}}"
          }
        ]
      },
      {
        "title": "Memory Usage Trend",
        "type": "graph",
        "targets": [
          {
            "expr": "system_memory_usage_bytes",
            "legendFormat": "{{instance}} - {{type}}"
          }
        ]
      },
      {
        "title": "Disk Space Usage",
        "type": "gauge",
        "targets": [
          {
            "expr": "system_disk_usage_percentage",
            "legendFormat": "{{instance}}:{{mountpoint}}"
          }
        ]
      }
    ]
  }
}
```

### 3.2 应用仪表板
```json
{
  "dashboard": {
    "title": "Web Application Performance Dashboard",
    "uid": "web-app-performance",
    "tags": ["application", "performance", "web"],
    "panels": [
      {
        "title": "HTTP Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{service}} - {{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Response Time Percentiles",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.5, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "{{service}} - p50"
          },
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "{{service}} - p95"
          },
          {
            "expr": "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "{{service}} - p99"
          }
        ]
      },
      {
        "title": "Error Rate by Service",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m]) * 100",
            "legendFormat": "{{service}} Error Rate %"
          }
        ]
      }
    ]
  }
}
```

### 3.3 业务仪表板
```json
{
  "dashboard": {
    "title": "Business Metrics Dashboard",
    "uid": "business-metrics-overview",
    "tags": ["business", "metrics", "kpi"],
    "panels": [
      {
        "title": "Daily User Registrations",
        "type": "graph",
        "targets": [
          {
            "expr": "increase(business_user_registrations_total[1d])",
            "legendFormat": "Registrations"
          }
        ]
      },
      {
        "title": "Revenue Trend",
        "type": "graph",
        "targets": [
          {
            "expr": "business_order_value_usd_total",
            "legendFormat": "Daily Revenue"
          }
        ]
      },
      {
        "title": "Conversion Rate",
        "type": "singlestat",
        "targets": [
          {
            "expr": "(business_orders_completed_total / business_orders_created_total) * 100",
            "legendFormat": "Conversion Rate %"
          }
        ]
      }
    ]
  }
}
```

## 四、日志监控命名规范

### 4.1 日志指标命名
```prometheus
# 应用日志级别计数
logs_error_total{service="web-app", level="error"}  # 日志-错误-总计
logs_warning_total{service="web-app", level="warning"}  # 日志-警告-总计
logs_info_total{service="web-app", level="info"}  # 日志-信息-总计

# 特定错误模式计数
logs_specific_error_total{service="web-app", error_type="database_connection"}  # 日志-特定错误-总计
logs_specific_error_total{service="web-app", error_type="authentication_failure"}

# 日志聚合指标
logs_lines_processed_total{service="log-processor"}  # 日志-行-处理-总计
logs_parse_errors_total{service="log-processor"}  # 日志-解析错误-总计
logs_export_success_total{service="log-exporter"}  # 日志-导出成功-总计
```

### 4.2 日志告警规则
```yaml
# 日志错误告警
- alert: HighErrorLogRate
  expr: rate(logs_error_total[5m]) > 10
  for: 2m
  labels:
    severity: warning
    category: logs
    team: operations
  annotations:
    summary: "High error log rate for {{ $labels.service }}"
    description: "Error log rate is {{ $value }} errors/second for service {{ $labels.service }}"

- alert: CriticalLogError
  expr: logs_specific_error_total{error_type="database_connection"} > 0
  for: 1m
  labels:
    severity: critical
    category: logs
    team: database
  annotations:
    summary: "Database connection errors detected"
    description: "Database connection errors occurring at rate of {{ $value }}/second"
```

## 五、分布式追踪命名规范

### 5.1 追踪跨度命名
```json
{
  "spans": [
    {
      "name": "http.request.process",  # HTTP-请求-处理
      "service": "web-app",
      "operation": "GET /api/users"
    },
    {
      "name": "database.query.execute",  # 数据库-查询-执行
      "service": "user-service",
      "operation": "SELECT * FROM users WHERE id = ?"
    },
    {
      "name": "cache.get.operation",  # 缓存-获取-操作
      "service": "user-service",
      "operation": "GET user:12345"
    },
    {
      "name": "external.api.call",  # 外部-API-调用
      "service": "payment-service",
      "operation": "POST https://payment-gateway.com/process"
    }
  ]
}
```

### 5.2 追踪指标命名
```prometheus
# 追踪延迟指标
tracing_span_duration_seconds{service="web-app", operation="http.request.process", quantile="0.5"}  # 追踪-跨度-持续时间-秒
tracing_span_duration_seconds{service="web-app", operation="http.request.process", quantile="0.95"}
tracing_span_duration_seconds{service="web-app", operation="http.request.process", quantile="0.99"}

# 追踪错误指标
tracing_span_errors_total{service="web-app", operation="http.request.process"}  # 追踪-跨度-错误-总计
tracing_trace_errors_total{service="web-app"}  # 追踪-跟踪-错误-总计

# 追踪采样指标
tracing_spans_sampled_total{service="web-app", sampled="true"}  # 追踪-跨度-采样-总计
tracing_traces_sampled_total{service="web-app", sampled="true"}  # 追踪-跟踪-采样-总计
```

## 六、基础设施监控命名

### 6.1 容器监控指标
```prometheus
# Docker容器指标
container_cpu_usage_percentage{container="web-app-container"}  # 容器-CPU-使用率-百分比
container_memory_usage_bytes{container="web-app-container"}  # 容器-内存-使用-字节
container_network_receive_bytes_total{container="web-app-container"}  # 容器-网络-接收-字节-总计
container_network_transmit_bytes_total{container="web-app-container"}  # 容器-网络-发送-字节-总计
container_disk_io_reads_total{container="web-app-container"}  # 容器-磁盘-IO-读取-总计
container_disk_io_writes_total{container="web-app-container"}  # 容器-磁盘-IO-写入-总计

# Kubernetes指标
kubernetes_pod_status_ready{pod="web-app-7d5b8c9f4-xl2v9", namespace="production"}  # Kubernetes-Pod-状态-就绪
kubernetes_pod_status_phase{pod="web-app-7d5b8c9f4-xl2v9", namespace="production", phase="Running"}  # Kubernetes-Pod-状态-阶段
kubernetes_deployment_replicas_available{deployment="web-app", namespace="production"}  # Kubernetes-部署-副本-可用
kubernetes_node_status_condition{node="worker-node-01", condition="Ready", status="true"}  # Kubernetes-节点-状态-条件
```

### 6.2 网络监控指标
```prometheus
# 网络设备指标
network_interface_up{device="eth0", instance="router-01"}  # 网络-接口-上线
network_interface_speed_bps{device="eth0", instance="router-01"}  # 网络-接口-速度-bps
network_packets_dropped_total{device="eth0", instance="router-01", direction="in"}  # 网络-数据包-丢弃-总计
network_packets_dropped_total{device="eth0", instance="router-01", direction="out"}

# 负载均衡器指标
loadbalancer_connections_active_total{instance="lb-01"}  # 负载均衡器-连接-活跃-总计
loadbalancer_request_rate_requests_per_second{instance="lb-01"}  # 负载均衡器-请求率-每秒请求数
loadbalancer_backend_health_status{backend="web-app-backend", status="healthy"}  # 负载均衡器-后端-健康-状态
```

## 七、自定义监控集成

### 7.1 业务自定义指标
```java
// Java应用自定义指标示例
@Component
public class BusinessMetricsCollector {
    
    private final MeterRegistry meterRegistry;
    
    // 用户行为指标
    private final Counter userRegistrations;
    private final Counter userLogins;
    private final Timer userSessionDuration;
    
    // 订单指标
    private final Counter ordersCreated;
    private final Counter ordersCompleted;
    private final DistributionSummary orderValue;
    
    // 支付费指标
    private final Counter paymentsProcessed;
    private final Counter paymentSuccesses;
    private final Counter paymentFailures;
    private final DistributionSummary paymentAmount;
    
    public BusinessMetricsCollector(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        
        // 用户指标初始化
        this.userRegistrations = Counter.builder("business.user.registrations.total")
                .description("Total number of user registrations")
                .tags("source", "web")
                .register(meterRegistry);
                
        this.userLogins = Counter.builder("business.user.logins.total")
                .description("Total number of user logins")
                .tags("method", "password")
                .register(meterRegistry);
                
        this.userSessionDuration = Timer.builder("business.user.session.duration.seconds")
                .description("User session duration")
                .register(meterRegistry);
        
        // 订单指标初始化
        this.ordersCreated = Counter.builder("business.orders.created.total")
                .description("Total number of orders created")
                .tags("order_type", "standard")
                .register(meterRegistry);
                
        this.ordersCompleted = Counter.builder("business.orders.completed.total")
                .description("Total number of orders completed")
                .tags("order_type", "standard")
                .register(meterRegistry);
                
        this.orderValue = DistributionSummary.builder("business.order.value.usd")
                .description("Order value in USD")
                .baseUnit("dollars")
                .register(meterRegistry);
        
        // 支付费指标初始化
        this.paymentsProcessed = Counter.builder("business.payments.processed.total")
                .description("Total number of payments processed")
                .tags("payment_method", "credit_card")
                .register(meterRegistry);
                
        this.paymentSuccesses = Counter.builder("business.payments.success.total")
                .description("Total number of successful payments")
                .register(meterRegistry);
                
        this.paymentFailures = Counter.builder("business.payments.failure.total")
                .description("Total number of failed payments")
                .register(meterRegistry);
                
        this.paymentAmount = DistributionSummary.builder("business.payment.amount.usd")
                .description("Payment amount in USD")
                .baseUnit("dollars")
                .register(meterRegistry);
    }
    
    // 业务方法示例
    public void recordUserRegistration(String source) {
        userRegistrations.tags("source", source).increment();
    }
    
    public void recordOrderCompletion(double orderValueUsd) {
        ordersCompleted.increment();
        orderValue.record(orderValueUsd);
    }
    
    public void recordPayment(double amountUsd, boolean success) {
        paymentsProcessed.increment();
        paymentAmount.record(amountUsd);
        
        if (success) {
            paymentSuccesses.increment();
        } else {
            paymentFailures.increment();
        }
    }
}
```

### 7.2 健康检查端点
```java
@RestController
@RequestMapping("/health")
public class HealthController {
    
    @Autowired
    private HealthIndicator healthIndicator;
    
    @GetMapping
    public ResponseEntity<HealthResponse> getHealth() {
        Health health = healthIndicator.health();
        
        HealthResponse response = HealthResponse.builder()
                .status(health.getStatus().getCode())
                .checks(health.getDetails())
                .timestamp(Instant.now())
                .build();
                
        HttpStatus status = health.getStatus() == Status.UP ? 
                HttpStatus.OK : HttpStatus.SERVICE_UNAVAILABLE;
                
        return ResponseEntity.status(status).body(response);
    }
    
    @GetMapping("/metrics")
    public ResponseEntity<Map<String, Object>> getMetrics() {
        Map<String, Object> metrics = new HashMap<>();
        
        // 添加关键业务指标
        metrics.put("user_registrations_24h", getUserRegistrationsLast24h());
        metrics.put("orders_completed_24h", getOrdersCompletedLast24h());
        metrics.put("payment_success_rate", getPaymentSuccessRate());
        metrics.put("average_response_time_ms", getAverageResponseTime());
        
        return ResponseEntity.ok(metrics);
    }
}
```

## 八、最佳实践示例

### 8.1 监控配置管理
```yaml
# 监控配置文件结构
monitoring/
├── prometheus/
│   ├── rules/
│   │   ├── system-alerts.yml           # 系统告警规则
│   │   ├── application-alerts.yml      # 应用告警规则
│   │   └── business-alerts.yml         # 业务告警规则
│   ├── targets/
│   │   ├── production-targets.yml      # 生产环境监控目标
│   │   └── staging-targets.yml         # 预发布环境监控目标
│   └── recording-rules.yml             # 记录规则
│
├── grafana/
│   ├── dashboards/
│   │   ├── system-overview.json        # 系统概览仪表板
│   │   ├── application-performance.json # 应用性能仪表板
│   │   └── business-metrics.json       # 业务指标仪表板
│   └── datasources.yml                 # 数据源配置
│
└── alertmanager/
    ├── alertmanager.yml                # 告警管理配置
    └── templates/                      # 告警模板
        └── default.tmpl                # 默认告警模板
```

### 8.2 监控自动化脚本
```bash
#!/bin/bash
# monitoring_setup.sh - 监控系统自动化部署脚本

set -euo pipefail

# 配置变量
MONITORING_NAMESPACE="monitoring"
PROMETHEUS_VERSION="2.40.0"
GRAFANA_VERSION="9.3.0"
ALERTMANAGER_VERSION="0.25.0"

# 日志函数
log_info() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $1"; }
log_error() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" >&2; }

# 部署Prometheus
deploy_prometheus() {
    log_info "Deploying Prometheus ${PROMETHEUS_VERSION}"
    
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo update
    
    helm install prometheus prometheus-community/kube-prometheus-stack \
        --namespace ${MONITORING_NAMESPACE} \
        --create-namespace \
        --version ${PROMETHEUS_VERSION} \
        --values ./monitoring/prometheus/values.yaml \
        --set prometheus.prometheusSpec.retention=30d \
        --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=100Gi
}

# 部署Grafana
deploy_grafana() {
    log_info "Deploying Grafana ${GRAFANA_VERSION}"
    
    helm install grafana grafana/grafana \
        --namespace ${MONITORING_NAMESPACE} \
        --version ${GRAFANA_VERSION} \
        --values ./monitoring/grafana/values.yaml \
        --set persistence.enabled=true \
        --set persistence.size=10Gi \
        --set adminPassword=admin123
}

# 部署AlertManager
deploy_alertmanager() {
    log_info "Deploying AlertManager ${ALERTMANAGER_VERSION}"
    
    helm install alertmanager prometheus-community/alertmanager \
        --namespace ${MONITORING_NAMESPACE} \
        --version ${ALERTMANAGER_VERSION} \
        --values ./monitoring/alertmanager/values.yaml
}

# 配置告警规则
configure_alert_rules() {
    log_info "Configuring alert rules"
    
    kubectl apply -f ./monitoring/prometheus/rules/
    
    # 验证规则
    kubectl -n ${MONITORING_NAMESPACE} exec prometheus-prometheus-0 -- \
        promtool check rules /etc/prometheus/rules/*.yml
}

# 配置仪表板
configure_dashboards() {
    log_info "Configuring Grafana dashboards"
    
    # 创建配置映射包含仪表板JSON
    kubectl create configmap grafana-dashboards \
        --from-file=./monitoring/grafana/dashboards/ \
        --namespace ${MONITORING_NAMESPACE}
    
    # 重启Grafana以加载新仪表板
    kubectl rollout restart deployment/grafana -n ${MONITORING_NAMESPACE}
}

# 主函数
main() {
    log_info "Starting monitoring system deployment"
    
    deploy_prometheus
    deploy_grafana
    deploy_alertmanager
    configure_alert_rules
    configure_dashboards
    
    log_info "Monitoring system deployment completed"
    log_info "Access Grafana at: http://grafana.monitoring.svc.cluster.local"
    log_info "Access Prometheus at: http://prometheus.monitoring.svc.cluster.local"
}

# 执行
main "$@"
```

### 8.3 监控数据验证脚本
```python
#!/usr/bin/env python3
# monitoring_validator.py - 监控数据验证和告警测试脚本

import requests
import time
import json
from datetime import datetime, timedelta

class MonitoringValidator:
    def __init__(self, prometheus_url, alertmanager_url):
        self.prometheus_url = prometheus_url
        self.alertmanager_url = alertmanager_url
        self.test_results = []
    
    def test_metric_availability(self, metric_name, expected_labels=None):
        """测试指标是否可用"""
        query = f"{metric_name}"
        if expected_labels:
            label_filters = ",".join([f'{k}="{v}"' for k, v in expected_labels.items()])
            query += f"{{{label_filters}}}"
        
        url = f"{self.prometheus_url}/api/v1/query"
        params = {"query": query}
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data["status"] == "success" and len(data["data"]["result"]) > 0:
                self.test_results.append({
                    "test": f"Metric availability: {metric_name}",
                    "status": "PASS",
                    "timestamp": datetime.now().isoformat()
                })
                return True
            else:
                self.test_results.append({
                    "test": f"Metric availability: {metric_name}",
                    "status": "FAIL",
                    "reason": "No data returned",
                    "timestamp": datetime.now().isoformat()
                })
                return False
                
        except Exception as e:
            self.test_results.append({
                "test": f"Metric availability: {metric_name}",
                "status": "FAIL",
                "reason": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def test_alert_rules(self):
        """测试告警规则配置"""
        url = f"{self.prometheus_url}/api/v1/rules"
        
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data["status"] == "success":
                rules_count = sum(len(group["rules"]) for group in data["data"]["groups"])
                self.test_results.append({
                    "test": "Alert rules configuration",
                    "status": "PASS",
                    "details": f"{rules_count} rules loaded",
                    "timestamp": datetime.now().isoformat()
                })
                return True
            else:
                self.test_results.append({
                    "test": "Alert rules configuration",
                    "status": "FAIL",
                    "reason": "Failed to retrieve rules",
                    "timestamp": datetime.now().isoformat()
                })
                return False
                
        except Exception as e:
            self.test_results.append({
                "test": "Alert rules configuration",
                "status": "FAIL",
                "reason": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def test_alert_firing(self):
        """测试活动告警"""
        url = f"{self.alertmanager_url}/api/v2/alerts"
        
        try:
            response = requests.get(url, timeout=10)
            alerts = response.json()
            
            firing_alerts = [alert for alert in alerts if alert["status"]["state"] == "firing"]
            
            self.test_results.append({
                "test": "Active alerts check",
                "status": "INFO",
                "details": f"{len(firing_alerts)} firing alerts",
                "alerts": firing_alerts[:5],  # 只显示前5个告警
                "timestamp": datetime.now().isoformat()
            })
            
            return len(firing_alerts)
            
        except Exception as e:
            self.test_results.append({
                "test": "Active alerts check",
                "status": "FAIL",
                "reason": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return -1
    
    def generate_report(self):
        """生成测试报告"""
        passed = sum(1 for result in self.test_results if result["status"] == "PASS")
        failed = sum(1 for result in self.test_results if result["status"] == "FAIL")
        total = len(self.test_results)
        
        report = {
            "summary": {
                "total_tests": total,
                "passed": passed,
                "failed": failed,
                "pass_rate": f"{(passed/total)*100:.1f}%" if total > 0 else "0%",
                "generated_at": datetime.now().isoformat()
            },
            "details": self.test_results
        }
        
        return json.dumps(report, indent=2, default=str)
    
    def run_validation_suite(self):
        """运行完整的验证套件"""
        print("Starting monitoring validation suite...")
        
        # 测试核心系统指标
        self.test_metric_availability("up")
        self.test_metric_availability("system_cpu_usage_percentage")
        self.test_metric_availability("system_memory_usage_bytes")
        
        # 测试应用指标
        self.test_metric_availability("http_requests_total")
        self.test_metric_availability("http_request_duration_seconds_count")
        
        # 测试告警配置
        self.test_alert_rules()
        
        # 检查活动告警
        self.test_alert_firing()
        
        # 生成报告
        report = self.generate_report()
        print(report)
        
        # 保存报告到文件
        with open(f"monitoring_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
            f.write(report)

# 使用示例
if __name__ == "__main__":
    validator = MonitoringValidator(
        prometheus_url="http://prometheus.monitoring.svc.cluster.local:9090",
        alertmanager_url="http://alertmanager.monitoring.svc.cluster.local:9093"
    )
    validator.run_validation_suite()
```

---

**注意事项：**
1. 监控指标命名应该遵循层级结构，便于理解和查询
2. 告警规则应该包含足够的上下文信息，便于快速定位问题
3. 仪表板设计应该聚焦关键指标，避免信息过载
4. 生产环境中必须实施适当的监控数据保留策略
5. 定期审查和优化监控配置，确保其有效性和效率