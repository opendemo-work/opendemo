package main

import (
	"fmt"
	"strings"

	"channels-demo/pkg/channels"
)

func main() {
	fmt.Println("=== 带缓冲 Channel 生产者-消费者 ===")
	fmt.Println(strings.Join(channels.BufferedChannel(), "\n"))
}
