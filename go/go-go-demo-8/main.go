package main

import (
	"io"
	"log"
	"os"
)

// main 函数演示如何创建文件并写入文本内容
func main() {
	const filename = "sample.txt"
	const content = "这是第一行。\n这是第二行。\n"

	// 使用 os.Create 创建新文件（若存在则覆盖）
	file, err := os.Create(filename)
	if err != nil {
		// 错误处理：记录错误并退出
		log.Fatalf("无法创建文件 %s: %v", filename, err)
	}
	// 使用 defer 确保文件最终被关闭
	defer func() {
		if closeErr := file.Close(); closeErr != nil {
			log.Printf("警告：关闭文件时出错: %v", closeErr)
		}
	}()

	// 将字符串写入文件
	_, err = io.WriteString(file, content)
	if err != nil {
		log.Fatalf("写入文件失败: %v", err)
	}

	// 输出成功提示
	log.Printf("文件已成功写入: %s", filename)
}