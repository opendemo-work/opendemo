package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"math/rand"
	"time"
)

// 模拟用户密码存储的安全哈希
func main() {
	password := "mySecurePassword123"
	salt := generateSalt()

	// 创建加盐哈希
	hash := sha256.New()
	hash.Write([]byte(password + salt))
	hashedPassword := hex.EncodeToString(hash.Sum(nil))

	fmt.Printf("密码哈希成功: %s\n", hashedPassword)

	// 验证密码（模拟登录）
	isValid := verifyPassword(password, salt, hashedPassword)
	fmt.Printf("密码验证通过: %t\n\n", isValid)
}

// generateSalt 生成随机盐值
func generateSalt() string {
	rand.Seed(time.Now().UnixNano())
	const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	salt := make([]byte, 16)
	for i := range salt {
		salt[i] = chars[rand.Intn(len(chars))]
	}
	return string(salt)
}

// verifyPassword 验证原始密码是否匹配哈希值
func verifyPassword(password, salt, hashedPassword string) bool {
	hash := sha256.New()
	hash.Write([]byte(password + salt))
	return hex.EncodeToString(hash.Sum(nil)) == hashedPassword
}