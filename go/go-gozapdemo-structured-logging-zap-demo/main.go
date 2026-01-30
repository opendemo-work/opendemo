package main

import (
	"go.uber.org/zap"
)

// 示例1: 使用 Zap 生产模式快速开始
func main() {
	// 创建生产级日志记录器（自动输出 JSON 到 stdout）
	logger, err := zap.NewProduction()
	if err != nil {
		panic(err) // 初始化失败直接中断
	}
	defer logger.Sync() // 确保所有日志写入

	// 使用 SugaredLogger 提供更灵活的日志 API（支持格式化）
	sugar := logger.Sugar()

	// 记录结构化信息日志
	sugar.Infow("用户登录成功",
		"user_id", 1001,
		"ip", "192.168.1.100",
	)

	// 记录错误事件
	sugar.Errorw("数据库连接失败",
		"error", "connection timeout",
		"attempts", 3,
	)

	// 格式化日志（兼容传统 Printf 风格）
	sugar.Infof("处理了 %d 个请求", 42)

	// 使用原生 Logger（更高性能，类型安全）
	logger.Info("服务已启动", zap.Int("port", 8080))
	logger.Warn("即将弃用的API被调用", zap.String("endpoint", "/v1/old"))
}