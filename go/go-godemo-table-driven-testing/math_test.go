package main

import (
	"math"
	"testing"
)

// IsPerfectSquare 判断一个非负整数是否为完全平方数
func IsPerfectSquare(n int) bool {
	if n < 0 {
		return false
	}
	sqrt := int(math.Sqrt(float64(n)))
	return sqrt*sqrt == n
}

// TestIsPerfectSquare 使用表驱动方式测试完全平方数判断函数
func TestIsPerfectSquare(t *testing.T) {
	// 定义测试用例：输入值和预期结果
	tests := []struct {
		input    int
		expected bool
	}{
		{input: 4, expected: true},   // 2^2
		{input: 8, expected: false},  // 不是完全平方数
		{input: 0, expected: true},   // 边界情况：0 是 0^2
		{input: 1, expected: true},   // 1^2
		{input: 25, expected: true},  // 5^2
		{input: 26, expected: false}, // 接近但不是
	}

	// 遍历每个测试用例
	for _, tc := range tests {
		// 使用 t.Run 创建子测试，便于识别失败用例
		t.Run(
			// 子测试名称，通常描述输入数据
			"Input_"+string(rune(tc.input+'0')), 
			func(t *testing.T) {
				got := IsPerfectSquare(tc.input)
				if got != tc.expected {
					// 报告错误，显示期望与实际值
					t.Errorf("IsPerfectSquare(%d) = %v; 期望 %v", tc.input, got, tc.expected)
				}
			},
		)
	}
}