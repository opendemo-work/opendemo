package main

import (
	"fmt"
	"sync"
)

// generate 将整数切片发送到channel —— 生产者
func generate(nums ...int) <-chan int {
	out := make(chan int)
	go func() {
		for _, n := range nums {
			out <- n
		}
		close(out)
	}()
	return out
}

// square 多个goroutine从in读取数据并计算平方，结果发送到out —— 扇出(Fan-out)
func square(in <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		for n := range in {
			out <- n * n
		}
		close(out)
	}()
	return out
}

// merge 将多个输入channel合并为一个输出channel —— 扇入(Fan-in)
func merge(cs ...<-chan int) <-chan int {
	var wg sync.WaitGroup
	out := make(chan int)

	// 启动一个goroutine将每个输入channel的内容复制到out
	output := func(c <-chan int) {
		for n := range c {
			out <- n
		}
		wg.Done()
	}

	wg.Add(len(cs))
	for _, c := range cs {
		go output(c)
	}

	// 所有输入channel处理完毕后关闭out
	go func() {
		wg.Wait()
		close(out)
	}()
	return out
}

func main() {
	// 构建并发流水线: generate -> square -> merge
	in := generate(1, 2, 3, 4, 5)

	// 扇出：启动两个square goroutine处理数据
	c1 := square(in)
	c2 := square(in)

	// 扇入：合并两个结果channel
	for v := range merge(c1, c2) {
		fmt.Println("平方结果:", v)
	}
	fmt.Println("所有计算完成")
}

/*
关键知识点：
- 并发流水线模式：将任务分解为多个阶段
- Fan-out: 多个goroutine处理同一数据源提升吞吐量
- Fan-in: 合并多个结果流
- channel作为第一类对象可被传递和返回
*/