package main

import (
	"context"
	"fmt"
	"time"
)

// 场景一：使用 WithTimeout 实现超时控制
func timeoutExample() {
	fmt.Println("--- 场景一：超时控制 ---")
	// 创建一个 2 秒后自动取消的上下文
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel() // 确保释放资源

	// 模拟长时间运行的任务
	go func(ctx context.Context) {
		for {
			select {
			case <-ctx.Done():
				// 当上下文被取消时，Done() 通道关闭
				fmt.Printf("任务在 %v 后被取消（%s）\n", 2*time.Second, ctx.Err())
				return
			default:
				fmt.Println("任务执行中...")
				time.Sleep(500 * time.Millisecond)
			}
		}
	}(ctx)

	// 等待足够时间让超时生效
	time.Sleep(3 * time.Second)
}

// 场景二：使用 WithCancel 主动取消 goroutine
func cancelExample() {
	fmt.Println("\n--- 场景二：手动取消 ---")
	ctx, cancel := context.WithCancel(context.Background())

	// 启动一个监控 goroutine
	go func(ctx context.Context) {
		ticker := time.NewTicker(1 * time.Second)
		for {
			select {
			case <-ctx.Done():
				fmt.Println("收到取消信号，停止监控")
				return
			case <-ticker.C:
				fmt.Println("监控运行中...")
			}
		}
	}(ctx)

	// 在另一个 goroutine 中模拟条件满足后取消
	go func() {
		time.Sleep(5 * time.Second)
		cancel() // 触发取消
	}()

	// 等待取消完成
	time.Sleep(6 * time.Second)
}

// 场景三：使用 WithValue 传递请求数据
func valueExample() {
	fmt.Println("\n--- 场景三：上下文传值 ---")
	// 创建带值的上下文（通常用于传递请求元数据）
	ctx := context.WithValue(context.Background(), "userID", "user123")
	processRequest(ctx)
}

// 模拟处理请求的函数，从 context 获取用户 ID
func processRequest(ctx context.Context) {
	// 从上下文中提取用户 ID
	if userID, ok := ctx.Value("userID").(string); ok {
		fmt.Printf("处理用户请求：%s\n", userID)
	} else {
		fmt.Println("未找到用户 ID")
	}
}

func main() {
	timeoutExample()
	cancelExample()
	valueExample()
}