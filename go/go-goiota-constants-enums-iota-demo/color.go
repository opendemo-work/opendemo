package main

import "fmt"

// Color 类型的 String 方法实现
// 为枚举类型添加可读的字符串表示
// 这是Go中增强类型可用性的常见做法
func (c Color) String() string {
	switch c {
	case Red:
		return "Red"
	case Green:
		return "Green"
	case Blue:
		return "Blue"
	default:
		return "Unknown"
	}
}

// 注意：String() 方法必须返回string类型
// 当使用 fmt 包（如 Println, Printf）输出 Color 类型时，会自动调用此方法