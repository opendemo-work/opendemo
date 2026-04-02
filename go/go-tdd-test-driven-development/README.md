# Go Test-Driven Development (TDD)

Go测试驱动开发实践。

## TDD循环

```
Red -> Green -> Refactor
  │       │         │
  ▼       ▼         ▼
 写测试   写代码    重构
(失败)   (通过)   (优化)
```

## TDD示例

```go
package calculator

import "testing"

// 1. 先写测试 (Red)
func TestAdd(t *testing.T) {
    calc := NewCalculator()
    result := calc.Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2, 3) = %d; want 5", result)
    }
}

// 2. 最小实现 (Green)
type Calculator struct{}

func NewCalculator() *Calculator {
    return &Calculator{}
}

func (c *Calculator) Add(a, b int) int {
    return a + b
}

// 3. 重构优化
func (c *Calculator) Add(numbers ...int) int {
    sum := 0
    for _, n := range numbers {
        sum += n
    }
    return sum
}
```

## 测试表格

```go
func TestAddTableDriven(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 2, 3, 5},
        {"negative", -2, -3, -5},
        {"zero", 0, 5, 5},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            calc := NewCalculator()
            got := calc.Add(tt.a, tt.b)
            if got != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d", tt.a, tt.b, got, tt.expected)
            }
        })
    }
}
```

## 学习要点

1. TDD循环
2. 测试先行
3. 小步快跑
4. 重构技巧
5. 测试覆盖
