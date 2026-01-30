package main

import (
	"fmt"
	"log"

	//go:embed version.txt
	versionContent string

	"embed-demo/assets"
)

func main() {
	// 输出嵌入的版本信息
	fmt.Println("--- 嵌入的版本信息 ---")
	fmt.Println(versionContent)

	// 从assets包读取嵌入的模板和配置
	templateContent, err := assets.ReadTemplate()
	if err != nil {
		log.Fatal("读取模板失败:", err)
	}
	fmt.Println("\n--- 嵌入的HTML模板 ---")
	fmt.Println(templateContent)

	configContent, err := assets.ReadConfig()
	if err != nil {
		log.Fatal("读取配置失败:", err)
	}
	fmt.Println("\n--- 嵌入的JSON配置 ---")
	fmt.Println(configContent)
}