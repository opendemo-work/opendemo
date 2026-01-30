package main

import (
	"bytes"
	"encoding/json"
	"log"
	"net/http"
	"time"
)

// StructuredLogger 提供结构化日志发送功能
type StructuredLogger struct {
	ServiceName string
	LogstashURL string
}

// NewStructuredLogger 创建一个新的结构化日志器
func NewStructuredLogger(service, url string) *StructuredLogger {
	return &StructuredLogger{
		ServiceName: service,
		LogstashURL: url,
	}
}

// Info 记录一条info级别的日志
func (s *StructuredLogger) Info(message string, fields map[string]interface{}) {
	s.sendLog("info", message, fields)
}

// Error 记录一条error级别的日志
func (s *StructuredLogger) Error(message string, fields map[string]interface{}) {
	s.sendLog("error", message, fields)
}

// sendLog 发送日志到Logstash
func (s *StructuredLogger) sendLog(level, message string, fields map[string]interface{}) {
	entry := map[string]interface{}{
		"@timestamp": time.Now().UTC().Format(time.RFC3339),
		"level":      level,
		"message":    message,
		"service":    s.ServiceName,
		"trace_id":   generateTraceID(), // 模拟唯一追踪ID
	}

	// 合并附加字段
	for k, v := range fields {
		entry[k] = v
	}

	data, _ := json.Marshal(entry)
	resp, err := http.Post(s.LogstashURL, "application/json", bytes.NewBuffer(data))
	if err != nil {
		log.Printf("发送日志失败: %v", err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode == 200 {
		log.Printf("✅ 成功发送日志: %s", message)
	} else {
		log.Printf("❌ Logstash响应失败: %d", resp.StatusCode)
	}
}

// generateTraceID 生成简单trace_id（实际应用中应使用UUID）
func generateTraceID() string {
	return fmt.Sprintf("trace-%d", time.Now().UnixNano())
}

// 示例用法（不会被执行，仅作展示）
/*
func exampleUsage() {
	logger := NewStructuredLogger("go-payment", "http://localhost:8080")
	logger.Info("支付开始", map[string]interface{}{
		"user_id": 1003,
		"amount":  99.9,
	})
	logger.Error("支付超时", map[string]interface{}{
		"order_id": "PAY-999",
		"duration": 30000,
	})
}
*/