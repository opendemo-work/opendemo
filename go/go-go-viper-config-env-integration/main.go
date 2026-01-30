package main

import (
	"fmt"

	"github.com/spf13/viper"
)

func main() {
	// 设置配置文件名称（无扩展名）
	viper.SetConfigName("config")
	// 设置配置文件类型
	viper.SetConfigType("yaml")
	// 添加配置搜索路径
	viper.AddConfigPath(".")

	// 读取配置文件
	if err := viper.ReadInConfig(); err != nil {
		// 如果配置文件不存在，我们仍允许运行（仅依赖环境变量）
		fmt.Printf("未找到配置文件，使用环境变量: %v\n", err)
	}

	// 启用环境变量自动绑定
	viper.AutomaticEnv()

	// 可选：设置环境变量前缀，例如 SERVER_HOST
	// 这样 Viper 会优先查找以 SERVER_ 开头的变量
	viper.SetEnvPrefix("SERVER")
	// 绑定特定字段到环境变量（即使没有前缀也能工作）
	viper.BindEnv("server.host", "SERVER_HOST")
	viper.BindEnv("server.port", "SERVER_PORT")
	viper.BindEnv("database.url", "DATABASE_URL")

	// 获取配置值，支持层级结构
	host := viper.GetString("server.host")
	port := viper.GetInt("server.port")
	dbURL := viper.GetString("database.url")

	// 输出结果
	fmt.Printf("服务器将在 %s:%d 启动\n", host, port)
	fmt.Printf("数据库连接: %s\n", dbURL)
}
