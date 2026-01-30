package main

import (
	"log"

	"github.com/hashicorp/consul/api"
)

func main() {
	// 创建 Consul 客户端配置
	config := api.DefaultConfig()
	config.Address = "127.0.0.1:8500"

	// 初始化客户端
	client, err := api.NewClient(config)
	if err != nil {
		log.Fatalf("无法创建 Consul 客户端: %v", err)
	}

	// 查询指定服务的健康实例
	// 参数说明: Service(服务名, 标签过滤, 仅返回通过检查的实例, 查询选项)
	serviceEntries, _, err := client.Health().Service("demo-service", "", true, nil)
	if err != nil {
		log.Fatalf("服务发现失败: %v", err)
	}

	// 输出发现的服务实例信息
	if len(serviceEntries) == 0 {
		log.Println("未发现健康的服务实例")
		return
	}

	for _, entry := range serviceEntries {
		// 打印服务实例详情
		status := entry.Checks.AggregatedStatus() // 获取综合健康状态
		fmt.Printf("发现服务实例: %s @ %s:%d, 状态: %s\n",
			entry.Service.Service,
			entry.Node.Address,
			entry.Service.Port,
			status)
	}
}

// 注意：需要导入 fmt 包
import "fmt"