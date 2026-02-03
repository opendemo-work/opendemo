package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

// HealthResponse 定义健康检查的返回结构
type HealthResponse struct {
	Status    string            `json:"status"`     // 总体状态：healthy, degraded, unhealthy
	Timestamp string            `json:"timestamp"`  // 检查时间
	Details   map[string]string `json:"details"`    // 各组件详细状态
}

// healthChecker 是健康检查接口，便于扩展
type healthChecker interface {
	Check() (map[string]string, string) // 返回详情和总体状态
}

// mockHealthChecker 模拟一个简单的健康检查实现
type mockHealthChecker struct{}

// Check 实现健康检查逻辑，模拟多个组件状态
func (m *mockHealthChecker) Check() (map[string]string, string) {
	details := make(map[string]string)

	// 模拟数据库检查
	if time.Now().Unix()%13 == 0 {
		// 偶尔模拟数据库故障（用于测试）
		details["database"] = "failed: connection timeout"
	} else {
		details["database"] = "ok"
	}

	// 模拟缓存检查
	if time.Now().Unix()%17 == 0 {
		details["cache"] = "failed: redis unreachable"
	} else {
		details["cache"] = "ok"
	}

	// 聚合状态判断
	for _, status := range details {
		if status != "ok" {
			return details, "degraded" // 至少一个失败
		}
	}
	return details, "healthy" // 全部正常
}

// healthHandler 处理 /health 请求
func healthHandler(w http.ResponseWriter, r *http.Request) {
	checker := &mockHealthChecker{}
	// 执行健康检查
	details, overallStatus := checker.Check()

	// 构造响应
	response := HealthResponse{
		Status:    overallStatus,
		Timestamp: time.Now().UTC().Format(time.RFC3339),
		Details:   details,
	}

	// 设置Content-Type为application/json
	w.Header().Set("Content-Type", "application/json")

	// 根据整体状态设置HTTP状态码
	if overallStatus == "healthy" {
		w.WriteHeader(http.StatusOK)
	} else {
		w.WriteHeader(http.StatusServiceUnavailable) // 503
	}

	// 返回JSON响应
	if err := json.NewEncoder(w).Encode(response); err != nil {
		log.Printf("写入响应失败: %v", err)
		return
	}
}

// 主函数：启动HTTP服务器
func main() {
	http.HandleFunc("/health", healthHandler)
	log.Println("服务启动在 :8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}