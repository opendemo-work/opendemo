package main

import (
	"fmt"
	"strings"

	"channels-demo/pkg/channels"
)

func main() {
	fmt.Println("=== 无缓冲 Channel 基本通信 ===")
	fmt.Println(strings.Join(channels.BasicChannel(), "\n"))
}
