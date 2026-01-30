package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

// 定义存储 flag 值的变量
var name string

// helloCmd represents the hello command
// 用于向用户打招呼
var helloCmd = &cobra.Command{
	Use:   "hello",
	Short: "打印问候语", // 简短描述，在 help 列表中显示
	Long:  `这是一个简单的示例命令，用于展示如何接收用户输入并输出响应`, // 详细描述
	Run: func(cmd *cobra.Command, args []string) {
		// 核心逻辑：根据 name 变量值输出不同问候语
		fmt.Printf("Hello, %s!\n", name)
	},
}

// init 函数在包加载时自动注册命令
func init() {
	// 将 helloCmd 添加到 rootCmd
	rootCmd.AddCommand(helloCmd)

	// 添加本地标志（仅在当前命令可用）
	// 使用 StringVarP 允许绑定变量、设置长选项、短选项和默认值
	helloCmd.Flags().StringVarP(&name, "name", "n", "World", "要问候的人名")
}
