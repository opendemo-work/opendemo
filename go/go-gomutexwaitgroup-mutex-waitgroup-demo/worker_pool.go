package main

import (
	"fmt"
	"sync"
)

func worker(id int, task string, wg *sync.WaitGroup) {
	defer wg.Done() // 任务完成时通知
	fmt.Printf("工作者 %d 正在处理任务: %s\n", id, task)
	// 模拟工作耗时（无需真实sleep）
}

func workerPoolExample() {
	var wg sync.WaitGroup
	tasks := []string{"清洗数据", "生成报告", "发送邮件", "备份文件", "优化索引"}

	for i, task := range tasks {
		wg.Add(1)
		go worker(i+1, task, &wg)
	}

	wg.Wait() // 等待所有任务完成
	fmt.Println("所有工作任务已完成")
}