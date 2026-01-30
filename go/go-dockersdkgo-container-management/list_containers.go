package main

import (
	"context"
	"fmt"

	"github.com/docker/docker/client"
	"github.com/docker/docker/api/types"
)

// list_containers.go：列出当前所有运行中的容器
func main() {
	// 创建 Docker 客户端
	cli, err := client.NewClientWithOpts(client.FromEnv)
	if err != nil {
		panic(err)
	}
	defer cli.Close()

	// 查询运行中的容器
	containers, err := cli.ContainerList(
		context.Background(),
		types.ContainerListOptions{All: false}, // 仅运行中
	)
	if err != nil {
		panic(err)
	}

	fmt.Println("📦 当前运行中的容器：")
	for _, c := range containers {
		image := c.Image
		cmd := "unknown"
		if len(c.Command) > 0 {
			cmd = c.Command
		}
		fmt.Printf("- ID: %s, Image: %s, Command: %s\n", 
            c.ID[:8], image, cmd)
	}
}