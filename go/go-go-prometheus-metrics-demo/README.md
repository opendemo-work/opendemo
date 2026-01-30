# Go Prometheus Metrics 监控 Demo

## 简介
本项目是一个完整的 Go 应用程序，演示如何使用 Prometheus client_golang 库暴露自定义和内置的监控指标。它包含一个简单的 HTTP 服务，定期生成业务指标（如请求计数、处理延迟），并通过 `/metrics` 接口供 Prometheus 抓取。

## 学习目标
- 理解 Prometheus 指标的基本类型（Counter, Gauge, Histogram）
- 掌握在 Go 服务中集成 Prometheus 指标的最佳实践
- 学会暴露 metrics 端点并验证其格式
- 了解如何模拟业务指标并观察变化

## 环境要求
- Go 1.20 或更高版本
- Git（用于拉取依赖）
- curl 或浏览器（用于查看指标）

## 安装依赖的详细步骤
```bash
# 克隆项目（如果需要）
# git clone https://github.com/example/go-prometheus-demo.git
# cd go-prometheus-demo

# 初始化模块并下载依赖
go mod init prometheus-demo
go get github.com/prometheus/client_golang/prometheus
go get github.com/prometheus/client_golang/prometheus/promhttp
```

## 文件说明
- `main.go`: 主程序，启动 HTTP 服务器并注册指标
- `metrics.go`: 定义和管理自定义业务指标
- `README.md`: 本指南

## 逐步实操指南

### 步骤1: 创建项目目录并进入
```bash
dir demo && cd demo
```

### 步骤2: 创建代码文件
创建 `main.go` 和 `metrics.go`，内容见代码部分。

### 步骤3: 运行程序
```bash
go run main.go
```

**预期输出**：
```text
Starting server at :8080
```

### 步骤4: 访问服务以生成指标
在另一个终端运行：
```bash
curl http://localhost:8080/api/data
curl http://localhost:8080/api/status
curl http://localhost:8080/api/data
```

### 步骤5: 查看暴露的指标
```bash
curl http://localhost:8080/metrics
```

你将看到类似以下的输出（节选）：
```text
# HELP api_requests_total Total number of API requests by endpoint and method
# TYPE api_requests_total counter
api_requests_total{endpoint="/api/data",method="GET"} 2
api_requests_total{endpoint="/api/status",method="GET"} 1

# HELP api_request_duration_seconds Latency of API requests by endpoint
# TYPE api_request_duration_seconds histogram
api_request_duration_seconds_bucket{endpoint="/api/data",le="0.1"} 2
api_request_duration_seconds_bucket{endpoint="/api/status",le="0.1"} 1
...
```

## 代码解析

### `metrics.go` 关键代码段
```go
var ApiRequestCount = prometheus.NewCounterVec(
	prometheus.CounterOpts{
		Name: "api_requests_total",
		Help: "Total number of API requests by endpoint and method",
	},
	[]string{"endpoint", "method"},
)
```
- 使用 `NewCounterVec` 创建带标签的计数器，按接口和方法维度统计请求数
- 标签（labels）允许 Prometheus 按维度查询和聚合

```go
histogram.WithLabelValues(r.URL.Path).Observe(duration.Seconds())
```
- `Observe()` 记录一次请求耗时，自动归入对应的桶（bucket）

### `main.go` 中的路由处理
```go
http.Handle("/metrics", promhttp.Handler())
```
- 使用 `promhttp.Handler()` 自动暴露所有已注册的指标，符合 Prometheus 文本格式规范

## 预期输出示例
成功运行后，访问 `/metrics` 应返回标准 Prometheus 格式的指标文本，包含 `HELP`、`TYPE` 注释及指标值。

## 常见问题解答

**Q: 启动时报错找不到包？**
A: 确保已运行 `go mod tidy` 下载依赖。

**Q: /metrics 页面返回 404？**
A: 检查是否正确注册了 `http.Handle("/metrics", ...)` 路由。

**Q: 指标没有更新？**
A: 确保调用了 `Inc()` 或 `Observe()` 方法，并且有实际请求触发逻辑。

## 扩展学习建议
- 将此服务部署到 Kubernetes 并配置 Prometheus 抓取
- 添加 Grafana 面板可视化指标
- 实现自定义 Collector 采集复杂状态
- 使用 `Summary` 类型替代 `Histogram` 对比差异
- 集成日志与 tracing 形成可观测性闭环