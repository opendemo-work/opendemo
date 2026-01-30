package main

import "sync"

// Account 表示一个银行账户，包含余额和保护它的互斥锁
type Account struct {
	balance int
	mu      sync.Mutex // 保护balance字段
}

// deposit 向账户存款
func (a *Account) deposit(amount int) {
	a.mu.Lock()
	defer a.mu.Unlock()
	a.balance += amount
}

// withdraw 从账户取款
func (a *Account) withdraw(amount int) {
	a.mu.Lock()
	defer a.mu.Unlock()
	if a.balance >= amount {
		a.balance -= amount
	}
}

// getBalance 返回账户余额
func (a *Account) getBalance() int {
	a.mu.Lock()
	defer a.mu.Unlock()
	return a.balance
}