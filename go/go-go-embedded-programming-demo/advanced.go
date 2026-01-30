package main

import "fmt"

// Speaker 定义发声行为的接口
type Speaker interface {
	Speak()
}

// User 表示系统用户
type User struct {
	Username string
}

// SayHello 实现基本问候
func (u User) SayHello() {
	fmt.Printf("欢迎用户: %s\n", u.Username)
}

// AdminRole 表示管理员角色
type AdminRole struct {
	Role string
}

// Permissions 返回权限列表
func (a AdminRole) Permissions() string {
	return "读写执行"
}

// AdminUser 管理员用户，嵌入多个类型
type AdminUser struct {
	User       // 嵌入用户信息
	AdminRole  // 嵌入管理员角色
	// 如果需要覆盖Name等字段，可以显式声明
	// Name string // 会遮蔽User.Name
}

// Greet 重写问候方法
func (a AdminUser) Greet() {
	a.SayHello()
	fmt.Printf("高级员工: %s, 角色: %s, 权限: %s\n", a.Username, a.Role, a.Permissions())
}

// 演示如何处理字段遮蔽
func demonstrateFieldShadowing() {
	admin := AdminUser{
		User:      User{Username: "李四"},
		AdminRole: AdminRole{Role: "管理员"},
	}

	// 即使没有遮蔽，也可以通过类型名访问
	fmt.Println("通过类型访问:", admin.User.Username)

	admin.Greet()
}

func main() {
	demonstrateFieldShadowing()
}