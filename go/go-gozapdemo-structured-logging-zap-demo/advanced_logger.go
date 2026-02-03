package main

import (
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	"os"
)

// 示例2: 自定义日志配置，支持多输出和级别控制
func newAdvancedLogger() *zap.Logger {
	// 配置日志编码：JSON 格式
	config := zap.NewProductionConfig()
	config.OutputPaths = []string{"stdout", "app.log"} // 同时输出到控制台和文件
	config.Level = zap.NewAtomicLevelAt(zap.DebugLevel)  // 启用 debug 级别

	// 自定义编码器配置（可选美化）
	config.EncoderConfig.TimeKey = "ts"
	config.EncoderConfig.CallerKey = "caller"
	config.EncoderConfig.LevelKey = "level"
	config.EncoderConfig.MessageKey = "msg"

	// 构建 logger
	logger, err := config.Build()
	if err != nil {
		panic(err)
	}

	return logger
}

func exampleAdvancedUsage() {
	logger := newAdvancedLogger()
	defer logger.Sync()

	// 使用高级日志器记录各种事件
	logger.Debug("调试信息：进入函数处理", zap.String("func", "exampleAdvancedUsage"))
	logger.Info("定时任务开始执行", zap.String("task", "cleanup"), zap.Int("timeout_sec", 30))

	// 模拟错误
	err := os.ErrNotExist
	logger.Error("文件读取失败", zap.String("file", "config.json"), zap.Error(err))
}