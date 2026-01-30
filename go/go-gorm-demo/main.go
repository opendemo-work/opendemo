package main

import (
	"fmt"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

// 定义用户模型，对应数据库中的 users 表
type User struct {
	gorm.Model // 内嵌gorm.Model，包含ID、CreatedAt、UpdatedAt、DeletedAt等字段
	Name string // 用户名
	Age  int    // 年龄
}

func main() {
	// 连接到SQLite数据库（文件名为demo.db）
	// 注意：SQLite是轻量级文件数据库，适合本地开发测试
	db, err := gorm.Open(sqlite.Open("demo.db"), &gorm.Config{})
	if err != nil {
		panic("failed to connect database: " + err.Error())
	}
	fmt.Println("已连接到数据库")

	// 自动迁移 schema
	// 如果表不存在则创建；若结构变化，会尝试自动更新（注意：生产环境慎用）
	db.AutoMigrate(&User{})
	fmt.Println("已自动创建表")

	// === Create (增) ===
	user := User{Name: "Alice", Age: 30}
	db.Create(&user)
	fmt.Printf("✅ 创建用户：ID=%d, 名字=%s, 年龄=%d\n", user.ID, user.Name, user.Age)

	// === Read (查) ===
	var users []User
	db.Find(&users)
	fmt.Println("✅ 查询所有用户：")
	for _, u := range users {
		fmt.Printf("- 用户: ID=%d, 名字=%s, 年龄=%d\n", u.ID, u.Name, u.Age)
	}

	// === Update (改) ===
	db.Model(&user).Update("Age", 31)
	fmt.Printf("✅ 更新用户年龄：ID=%d -> 新年龄=%d\n", user.ID, 31)

	// === Delete (删) ===
	db.Delete(&user, user.ID)
	fmt.Printf("✅ 删除用户：ID=%d\n", user.ID)

	// 验证删除结果
	var count int64
	db.Model(&User{}).Count(&count)
	fmt.Printf("✅ 验证删除结果：当前用户总数 = %d\n", count)

	fmt.Println("🎉 所有操作执行完成！")
}