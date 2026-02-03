package main

import (
	"fmt"
	"time"
)

// timerExample 演示定时器和打点器的使用
func timerExample() {
	// 创建一个2秒后触发的定时器
	timer := time.NewTimer(2 * time.Second)
	fmt.Println("等待定时器触发...")

	// 阻塞直到定时器触发
	<-timer.C
	fmt.Println("定时器触发: 2秒后执行")

	// 创建一个每1秒触发一次的打点器
	ticker := time.NewTicker(1 * time.Second)
	defer ticker.Stop() // 确保释放资源

	// 打点3次后退出
	for i := 1; i <= 3; i++ {
		<-ticker.C
		fmt.Printf("打点器: 第%d次打点\n", i)
	}
}