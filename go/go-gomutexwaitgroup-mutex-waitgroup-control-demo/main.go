package main

import (
	"fmt"
	"sync"
)

// 共享变量
var counter int
// 互斥锁，用于保护共享变量的并发访问
var mu sync.Mutex
// WaitGroup，用于等待所有goroutine完成
var wg sync.WaitGroup

func main() {
	const numGoroutines = 1000

	// 启动1000个goroutine，每个增加counter一次
	for i := 0; i < numGoroutines; i++ {
		wg.Add(1) // 增加WaitGroup计数
		go func() {
			defer wg.Done() // goroutine结束时通知

			// 使用Mutex加锁，保证对counter的访问是原子的
			mu.Lock()
			counter++ // 安全地增加共享变量
			mu.Unlock()
		}()
	}

	// 等待所有goroutine完成
	wg.Wait()

	// 输出最终结果
	fmt.Printf("最终计数器值: %d\n", counter)

	// 演示银行账户并发操作
	demoBankAccount()
}

// demoBankAccount 展示更复杂的应用场景：银行账户并发转账
func demoBankAccount() {
	fmt.Println("执行银行账户并发转账...")

	account := &Account{balance: 1000}
	var wg sync.WaitGroup
	const numTransfers = 100

	// 并发执行100次转账操作（每次转10元）
	for i := 0; i < numTransfers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			account.deposit(10)
		}()
		wg.Add(1)
		go func() {
			defer wg.Done()
			account.withdraw(10)
		}()
	}

	wg.Wait()
	fmt.Printf("转账完成后账户余额: %d\n", account.getBalance())
}