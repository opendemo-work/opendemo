package main

import (
	"bufio"
	"log"
	"os"
	"fmt"
)

// main 函数演示两种读取文件的方式：直接读取和缓冲读取
func main() {
	const filename = "sample.txt"

	log.Printf("正在读取文件: %s", filename)

	// 方法一：使用 ioutil.ReadAll 进行一次性读取（适合小文件）
	file, err := os.Open(filename)
	if err != nil {
		log.Fatalf("无法打开文件: %v", err)
	}
	defer file.Close()

	// 读取全部内容
	content, err := os.ReadFile(filename)
	if err != nil {
		log.Fatalf("读取文件内容失败: %v", err)
	}
	fmt.Println("--- 普通读取 ---")
	fmt.Print(string(content))

	// 方法二：使用 bufio.Scanner 逐行读取（推荐用于大文件）
	file2, err := os.Open(filename)
	if err != nil {
		log.Fatalf("无法重新打开文件以进行缓冲读取: %v", err)
	}
	defer file2.Close()

	scanner := bufio.NewScanner(file2)
	fmt.Println("\n--- 缓冲读取 ---")
	for scanner.Scan() {
		fmt.Println(scanner.Text()) // 输出每一行
	}

	// 检查扫描过程中是否发生错误
	if err := scanner.Err(); err != nil {
		log.Printf("读取文件时发生错误: %v", err)
	}
}