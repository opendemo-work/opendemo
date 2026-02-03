package main

import (
	"cobra-demo/cmd"
)

// 主程序入口
// 调用 cmd 包的 Execute 函数启动 CLI 应用
func main() {
	cmd.Execute()
}
