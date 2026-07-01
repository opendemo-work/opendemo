package main

import (
	"fmt"
	"strings"
	"time"

	"channels-demo/pkg/channels"
)

func main() {
	fmt.Println("=== select 多路复用与超时控制 ===")
	fmt.Println(strings.Join(channels.SelectChannel(2*time.Second, 3*time.Second), "\n"))
}
