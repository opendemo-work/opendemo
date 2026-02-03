package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"
)

// LogEntry 表示一条日志记录的结构
type LogEntry struct {
	Timestamp string                 `json:"@timestamp"`
	Level     string                 `json:"level"`
	Message   string                 `json:"message"`
	Service   string                 `json:"service"`
	Fields    map[string]interface{} `json:"fields,omitempty"`
}

// sendLogToLogstash 将日志条目发送到Logstash HTTP输入
func sendLogToLogstash(entry LogEntry) error {
	logstashURL := "http://localhost:8080"
	data, err := json.Marshal(entry)
	if err != nil {
		return fmt.Errorf("序列化日志失败: %v", err)
	}

	resp, err := http.Post(logstashURL, "application/json", bytes.NewBuffer(data))
	if err != nil {
		return fmt.Errorf("发送日志失败: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode >= 200 && resp.StatusCode < 300 {
		log.Printf("发送日志成功: %v", string(data))
	} else {
		log.Printf("Logstash返回错误状态码: %d", resp.StatusCode)
	}

	return nil
}

// generateLogEntry 构建一个日志条目
func generateLogEntry(level, message, service string, fields map[string]interface{}) LogEntry {
	return LogEntry{
		Timestamp: time.Now().UTC().Format(time.RFC3339),
		Level:     level,
		Message:   message,
		Service:   service,
		Fields:    fields,
	}
}

func main() {
	// 模拟两条不同类型的日志
	loginLog := generateLogEntry(
		"info",
		"用户登录成功",
		"go-auth",
		map[string]interface{}{"user_id": 1001, "ip": "192.168.1.10"},
	)

	errLog := generateLogEntry(
		"error",
		"订单创建失败",
		"go-order",
		map[string]interface{}{"order_id": "ORD-2025", "user_id": 1002, "amount": 299.9},
	)

	// 发送日志
	if err := sendLogToLogstash(loginLog); err != nil {
		log.Printf("发送日志失败: %v", err)
	}
	time.Sleep(time.Second)

	if err := sendLogToLogstash(errLog); err != nil {
		log.Printf("发送日志失败: %v", err)
	}
}