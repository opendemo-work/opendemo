package main

import (
	"fmt"
	"sync"
)

// Account 表示一个银行账户
type Account struct {
	Balance int
	mu      sync.Mutex // 每个账户有自己的锁
}

// Transfer 从from账户向to账户转账amount金额
func Transfer(from, to *Account, amount int) {
	// 为避免死锁，总是先锁余额较小的账户
	first, second := from, to
	if fmt.Sprintf("%p", from) > fmt.Sprintf("%p", to) {
		first, second = to, from
	}

	first.mu.Lock()
	defer first.mu.Unlock()

	second.mu.Lock()
	defer second.mu.Unlock()

	if from.Balance >= amount {
		from.Balance -= amount
		to.Balance += amount
	}
}

func bankTransferExample() {
	accountA := &Account{Balance: 1000}
	accountB := &Account{Balance: 0}

	var wg sync.WaitGroup
	const transfers = 500

	for i := 0; i < transfers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			Transfer(accountA, accountB, 1) // 并发转账
		}()
	}

	wg.Wait()
	fmt.Printf("账户A余额: %d, 账户B余额: %d\n", accountA.Balance, accountB.Balance)
}