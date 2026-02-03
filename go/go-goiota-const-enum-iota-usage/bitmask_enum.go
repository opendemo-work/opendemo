package main

import "fmt"

// 权限枚举使用位掩码模式
// 每个权限是2的幂次方，可以组合使用

type Permission int

const (
	PermissionRead  = 1 << iota // 1 (二进制: 001)
	PermissionWrite               // 2 (二进制: 010)
	PermissionExecute             // 4 (二进制: 100)
)

// 检查是否包含指定权限
// 使用按位与运算
func (p Permission) Has(permission Permission) bool {
	return p&permission != 0
}

// 为Permission类型实现String方法
func (p Permission) String() string {
	var permissions []string
	if p.Has(PermissionRead) {
		permissions = append(permissions, "READ")
	}
	if p.Has(PermissionWrite) {
		permissions = append(permissions, "WRITE")
	}
	if p.Has(PermissionExecute) {
		permissions = append(permissions, "EXECUTE")
	}
	
	if len(permissions) == 0 {
		return "NONE"
	}
	return join(permissions, "|")
}

// 简单的字符串连接函数（避免导入strings包）
func join(parts []string, sep string) string {
	if len(parts) == 0 {
		return ""
	}
	result := parts[0]
	for i := 1; i < len(parts); i++ {
		result += sep + parts[i]
	}
	return result
}

func main() {
	// 组合权限：读+写
	userPerm := PermissionRead | PermissionWrite
	
	fmt.Printf("用户权限：%s\n", userPerm)
	fmt.Printf("有读权限：%t\n", userPerm.Has(PermissionRead))
	fmt.Printf("有执行权限：%t\n", userPerm.Has(PermissionExecute))
}