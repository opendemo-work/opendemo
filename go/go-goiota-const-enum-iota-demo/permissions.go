package main

import "fmt"

// Permission 表示用户权限的位掩码枚举
type Permission int

const (
	// 使用位移操作结合iota定义权限标志
	Read    Permission = 1 << iota // Read = 1 (0001)
	Write                          // Write = 2 (0010)
	Execute                        // Execute = 4 (0100)
	Delete                         // Delete = 8 (1000)
)

// String 方法为Permission提供可读输出
func (p Permission) String() string {
	var parts []string
	if p&Read == Read {
		parts = append(parts, "READ")
	}
	if p&Write == Write {
		parts = append(parts, "WRITE")
	}
	if p&Execute == Execute {
		parts = append(parts, "EXECUTE")
	}
	if p&Delete == Delete {
		parts = append(parts, "DELETE")
	}
	if len(parts) == 0 {
		return "NONE"
	}
	return fmt.Sprintf("%s", parts)
}