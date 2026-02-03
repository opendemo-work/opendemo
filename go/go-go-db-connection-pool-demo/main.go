package main

import (
	"database/sql"
	"fmt"
	"log"
	"time"

	_ "github.com/mattn/go-sqlite3" // 注册SQLite驱动
)

// 初始化数据库连接池
func initDB() *sql.DB {
	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		log.Fatal("打开数据库失败:", err)
	}

	// 设置连接池参数
	// 最大打开连接数（活跃+空闲）
	db.SetMaxOpenConns(5)
	// 最大空闲连接数
	db.SetMaxIdleConns(3)
	// 连接最长存活时间（避免长期连接失效）
	db.SetConnMaxLifetime(time.Minute)

	// 简单测试连接
	if err := db.Ping(); err != nil {
		log.Fatal("数据库ping失败:", err)
	}

	log.Println("[INFO] 数据库连接池已初始化")
	return db
}

func main() {
	// 初始化连接池
	db := initDB()
	// 程序结束时关闭所有连接
	defer func() {
		log.Println("[INFO] 程序退出，连接将自动关闭")
		db.Close()
	}()

	// 执行一个简单查询
	var now int
	err := db.QueryRow("SELECT 1").Scan(&now)
	if err != nil {
		log.Fatal("查询失败:", err)
	}
	log.Printf("[INFO] 执行查询: 当前连接数=1, 空闲连接=0")
	log.Printf("[INFO] 查询成功，结果: %d", now)

	// 输出当前连接池状态
	stats := db.Stats()
	log.Printf("[INFO] 连接池状态 -> 打开连接: %d, 在用: %d, 空闲: %d",
		stats.OpenConnections, stats.InUse, stats.Idle)
}