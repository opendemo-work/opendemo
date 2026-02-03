package main

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/mattn/go-sqlite3" // 导入SQLite驱动
)

// User 表示用户结构体
type User struct {
	ID   int
	Name string
	Age  int
}

func main() {
	// 打开SQLite数据库（文件名为 demo.db）
	sqlDB, err := sql.Open("sqlite3", "./demo.db")
	if err != nil {
		log.Fatal("打开数据库失败:", err)
	}
	defer sqlDB.Close() // 程序结束前关闭数据库连接

	// 创建用户表（如果不存在）
	createTableSQL := `CREATE TABLE IF NOT EXISTS users (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL,
		age INTEGER
	);`
	_, err = sqlDB.Exec(createTableSQL)
	if err != nil {
		log.Fatal("创建表失败:", err)
	}

	// 在事务中执行CRUD操作
	err = performTransaction(sqlDB)
	if err != nil {
		log.Fatal("事务执行失败:", err)
	}

	fmt.Println("所有操作在事务中完成")
}

// performTransaction 执行一系列事务性CRUD操作
func performTransaction(db *sql.DB) error {
	// 开始事务
	tx, err := db.Begin()
	if err != nil {
		return err
	}

	// 确保事务在函数退出时回滚（除非已提交）
	defer func() {
		tx.Rollback() // Rollback是幂等的：如果已提交，则无影响
	}()

	// 1. CREATE: 插入新用户
	result, err := tx.Exec("INSERT INTO users(name, age) VALUES(?, ?)", "Alice", 30)
	if err != nil {
		return fmt.Errorf("插入用户失败: %w", err)
	}

	userID, err := result.LastInsertId()
	if err != nil {
		return fmt.Errorf("获取插入ID失败: %w", err)
	}
	fmt.Printf("用户创建成功，ID: %d\n", userID)

	// 2. READ: 查询刚插入的用户
	var user User
	err = tx.QueryRow("SELECT id, name, age FROM users WHERE id = ?", userID).Scan(&user.ID, &user.Name, &user.Age)
	if err != nil {
		return fmt.Errorf("查询用户失败: %w", err)
	}
	fmt.Printf("事务内查询 - 用户: %s, 年龄: %d\n", user.Name, user.Age)

	// 3. UPDATE: 更新用户年龄
	_, err = tx.Exec("UPDATE users SET age = ? WHERE id = ?", 31, userID)
	if err != nil {
		return fmt.Errorf("更新用户失败: %w", err)
	}
	fmt.Println("更新用户年龄成功")

	// 4. DELETE: 删除用户（此处注释掉保留数据，可取消注释测试删除）
	// _, err = tx.Exec("DELETE FROM users WHERE id = ?", userID)
	// if err != nil {
	// 	return fmt.Errorf("删除用户失败: %w", err)
	// }
	// fmt.Println("删除用户成功")

	// 提交事务：只有到达此处才会真正生效
	if err = tx.Commit(); err != nil {
		return err
	}

	// 取消defer中的Rollback效果（因为已经Commit）
	return nil
}