package main

import (
	"fmt"
	"strings"

	"channels-demo/pkg/channels"
)

func main() {
	fmt.Println("=== 安全关闭 Channel ===")
	fmt.Println(strings.Join(channels.ClosingChannel(), "\n"))
}
