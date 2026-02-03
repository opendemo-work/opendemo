package main

import (
	"log"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/hashicorp/consul/api"
)

func main() {
	// 创建默认的 Consul 客户端配置
	config := api.DefaultConfig()
	config.Address = "127.0.0.1:8500" // 指向本地 Consul 代理

	// 初始化 Consul 客户端
	client, err := api.NewClient(config)
	if err != nil {
		log.Fatalf("无法创建 Consul 客户端: %v", err)
	}

	// 定义要注册的服务
	registration := &api.AgentServiceRegistration{
		ID:      "demo-service-1",           // 服务实例唯一ID
		Name:    "demo-service",            // 服务名称
		Address: "127.0.0.1",               // 服务监听地址
		Port:    8080,                      // 服务端口
		Tags:    []string{"primary"},       // 可选标签，用于分类或路由
		Check: &api.AgentServiceCheck{
			HTTP:     "http://127.0.0.1:8080/health", // 健康检查端点
			Interval: "5s",                           // 每5秒检查一次
			Timeout:  "3s",                           // 超时时间
		},
	}

	// 向 Consul 注册服务
	err = client.Agent().ServiceRegister(registration)
	if err != nil {
		log.Fatalf("服务注册失败: %v", err)
	}

	log.Println("服务 'demo-service' 已成功注册到 Consul")

	// 设置中断信号监听，用于优雅退出
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)

	// 模拟周期性健康维护（实际中由 Consul 主动检查）
	ticker := time.NewTicker(3 * time.Second)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			log.Println("正在发送健康检查... (按 Ctrl+C 停止)")
		case <-c:
			// 优雅注销服务
			client.Agent().ServiceDeregister("demo-service-1")
			log.Println("服务已从 Consul 注销")
			return
		}
	}
}