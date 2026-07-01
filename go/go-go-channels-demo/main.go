package main

import (
	"fmt"
	"strings"
	"time"

	"channels-demo/pkg/channels"
)

func main() {
	fmt.Println("示例1: 基本 Goroutine 和 Channel 通信")
	printLines(channels.BasicChannel())

	fmt.Println("\n示例2: 使用缓冲 Channel 和关闭机制")
	printLines(channels.BufferedChannel())

	fmt.Println("\n示例3: 安全关闭 Channel")
	printLines(channels.ClosingChannel())

	fmt.Println("\n示例4: 使用 select 处理多个 Channel")
	printLines(channels.SelectChannel(2*time.Second, 3*time.Second))
}

func printLines(lines []string) {
	fmt.Println(strings.Join(lines, "\n"))
}
