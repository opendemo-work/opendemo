package main

import (
	"fmt"
	"os"
)

// writeFile 演示使用 defer 安全地处理文件资源
func writeFile(filename string) error {
	// 创建或截断文件
	file, err := os.Create(filename)
	if err != nil {
		return err
	}

	// 确保文件最终被关闭
	defer func() {
		if closeErr := file.Close(); closeErr != nil {
			fmt.Printf("警告：无法关闭文件 %s: %v\n", filename, closeErr)
		} else {
			fmt.Println("文件已成功写入并关闭")
		}
	}()

	// 模拟写入操作
	fmt.Println("正在写入文件...")
	_, err = file.WriteString("Hello, Go defer!\n")
	return err // 如果写入失败，defer 仍会关闭文件
}

func main() {
	err := writeFile("output.txt")
	if err != nil {
		fmt.Printf("写入文件失败: %v\n", err)
	}
	// output.txt 将被自动清理
}