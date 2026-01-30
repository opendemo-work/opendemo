package main

import (
	"context"
	"fmt"
	"time"

	"github.com/docker/docker/api/types"
	"github.com/docker/docker/api/types/container"
	"github.com/docker/docker/client"
	"github.com/docker/docker/pkg/stdcopy"
)

// 主函数：演示完整容器生命周期管理
func main() {
	fmt.Println("🚀 开始容器管理演示...")

	// 创建 Docker 客户端，使用默认环境配置（如 DOCKER_HOST）
	cli, err := client.NewClientWithOpts(client.FromEnv)
	if err != nil {
		panic(err)
	}
	defer cli.Close()

	// 步骤1：创建容器
	containerConfig := container.Config{
		Image: "nginx:alpine", // 使用轻量级 Nginx 镜像
		Cmd:   []string{"nginx", "-g", "daemon off;"}, // 后台运行 Nginx
		ExposedPorts: map[string]struct{}{
			"80/tcp": {},
		},
	}

	resp, err := cli.ContainerCreate(
		context.Background(),
		&containerConfig,
		nil, // HostConfig
		nil, // NetworkingConfig
		nil, // Platform
		"demo-nginx-container",
	)
	if err != nil {
		panic(err)
	}
	fmt.Printf("✅ 成功创建容器：%s\n", resp.ID[:12])

	// 步骤2：启动容器
	err = cli.ContainerStart(context.Background(), resp.ID, types.ContainerStartOptions{})
	if err != nil {
		panic(err)
	}
	fmt.Println("✅ 容器已启动")

	// 步骤3：等待几秒以便观察
	time.Sleep(2 * time.Second)

	// 步骤4：停止容器
	err = cli.ContainerStop(context.Background(), resp.ID, nil)
	if err != nil {
		panic(err)
	}
	fmt.Println("✅ 容器已停止")

	// 步骤5：删除容器
	err = cli.ContainerRemove(
		context.Background(),
		resp.ID,
		types.ContainerRemoveOptions{Force: true},
	)
	if err != nil {
		panic(err)
	}
	fmt.Println("🗑️ 容器已删除")
	fmt.Println("🎉 演示完成！")
}