package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

// versionCmd 显示应用版本信息
var versionCmd = &cobra.Command{
	Use:   "version",
	Short: "打印版本信息",
	Long:  `显示当前程序的版本号和构建时间`,
	Run: func(cmd *cobra.Command, args []string) {
		// 简单硬编码版本信息（生产中可通过 -ldflags 注入）
		fmt.Println("Version: v1.0.0")
		fmt.Println("Build Time: 2023-01-01")
	},
}

func init() {
	// 将 version 命令注册为 root 命令的子命令
	rootCmd.AddCommand(versionCmd)
}
