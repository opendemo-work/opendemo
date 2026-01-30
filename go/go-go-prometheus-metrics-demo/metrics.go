package main

import "github.com/prometheus/client_golang/prometheus"

// ApiRequestCount 是一个计数器向量，用于统计每个API端点的请求总数
// 标签包括：endpoint（接口路径）、method（HTTP方法）
var ApiRequestCount = prometheus.NewCounterVec(
	prometheus.CounterOpts{
		Name: "api_requests_total",
		Help: "Total number of API requests by endpoint and method",
	},
	[]string{"endpoint", "method"}, // 标签维度
)

// ApiRequestDuration 是一个直方图，用于记录每个API端点的请求延迟分布
// 直方图会自动将观测值归入预定义的桶（buckets）中
var ApiRequestDuration = prometheus.NewHistogramVec(
	prometheus.HistogramOpts{
		Name:    "api_request_duration_seconds",
		Help:    "Latency of API requests by endpoint",
		Buckets: []float64{0.01, 0.05, 0.1, 0.2, 0.5, 1.0}, // 定义延迟桶（秒）
	},
	[]string{"endpoint"}, // 按接口路径区分
)