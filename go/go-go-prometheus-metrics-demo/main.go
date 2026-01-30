package main

import (
	"log"
	"net/http"
	"time"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

// 初始化 Prometheus 指标注册表（使用默认注册表）
func init() {
	prometheus.MustRegister(ApiRequestCount)
	prometheus.MustRegister(ApiRequestDuration)
}

// handler 模拟一个业务处理函数，记录请求次数和延迟
func handler(w http.ResponseWriter, r *http.Request) {
	// 开始计时
	start := time.Now()

	// 模拟业务逻辑处理（随机延迟）
	duration := time.Duration(10+randInt(0, 100)) * time.Millisecond
	time.Sleep(duration)

	// 更新计数器
	ApiRequestCount.WithLabelValues(r.URL.Path, r.Method).Inc()

	// 更新直方图（记录耗时）
	ApiRequestDuration.WithLabelValues(r.URL.Path).Observe(time.Since(start).Seconds())

	// 返回响应
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("OK\n"))
}

// randInt 生成指定范围内的随机整数
func randInt(min, max int) int {
	return min + (int(time.Now().UnixNano())%(max-min+1))
}

func main() {
	// 注册业务路由
	http.HandleFunc("/api/data", handler)
	http.HandleFunc("/api/status", handler)

	// 注册 Prometheus 指标暴露端点
	http.Handle("/metrics", promhttp.Handler())

	log.Println("Starting server at :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatalf("Server failed to start: %v", err)
	}
}