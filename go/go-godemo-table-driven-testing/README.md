# Go单元测试：表驱动测试Demo

## 简介
本项目是一个用于学习Go语言中**表驱动测试（Table-Driven Tests）** 的完整示例。通过多个实际场景，演示如何用简洁、可维护的方式编写高效的单元测试。

## 学习目标
- 理解什么是表驱动测试及其优势
- 掌握在Go中编写表驱动测试的最佳实践
- 学会组织测试用例并提高测试覆盖率
- 熟悉Go标准库`testing`的基本使用

## 环境要求
- Go 1.19 或更高版本（推荐稳定版）
- 支持命令行操作的系统（Windows / Linux / macOS）

## 安装依赖
本项目仅使用Go标准库，无需额外依赖。

确保已安装Go环境：
```bash
go version
```
预期输出：
```
go version go1.19+ darwin/amd64  # 或 linux/windows
```

## 文件说明
- `math_test.go`: 演示对数学函数（如平方根判断）进行表驱动测试
- `validator_test.go`: 演示对字符串验证逻辑进行多场景测试
- `README.md`: 当前文档

## 逐步实操指南

### 步骤1: 创建项目目录
```bash
mkdir go-table-test-demo && cd go-table-test-demo
```

### 步骤2: 创建测试文件
将以下两个文件内容复制到对应路径：
- 创建文件 `math_test.go`
- 创建文件 `validator_test.go`

### 步骤3: 运行所有测试
```bash
go test -v
```

### 预期输出示例
```
=== RUN   TestIsPerfectSquare
--- PASS: TestIsPerfectSquare (0.00s)
=== RUN   TestValidateEmail
--- PASS: TestValidateEmail (0.00s)
PASS
ok      command-line-arguments  0.001s
```

## 代码解析

### math_test.go
```go
func TestIsPerfectSquare(t *testing.T) {
    tests := []struct{ Input, Expected int }{
        {4, true},
        {8, false},
        {0, true},
        {1, true},
        {25, true},
    }
```
定义一个匿名结构体切片，每个元素代表一个测试用例，包含输入和期望输出。

使用 `t.Run()` 提供子测试名称，便于定位失败用例：
```go
for _, tc := range tests {
    t.Run(fmt.Sprintf("Input_%d", tc.Input), func(t *testing.T) {
        got := IsPerfectSquare(tc.Input)
        if got != tc.Expected {
            t.Errorf("期望 %v, 实际 %v", tc.Expected, got)
        }
    })
}
```

### validator_test.go
展示了如何测试字符串验证函数，包括有效和无效邮箱格式，利用子测试命名清晰表达意图。

## 常见问题解答

**Q: 为什么使用表驱动测试？**
A: 可以集中管理测试用例，减少重复代码，易于添加新用例，提升可读性和可维护性。

**Q: 如何查看具体哪个测试失败？**
A: 使用 `go test -v` 显示详细日志，结合 `t.Run()` 的名称快速定位。

**Q: 能否共享测试前的设置逻辑？**
A: 可以，在 `t.Run()` 外部执行公共 setup，或使用辅助函数。

## 扩展学习建议
- 阅读《The Go Programming Language》第11章关于测试的内容
- 尝试使用 `testify/assert` 第三方库增强断言能力
- 学习基准测试（benchmark）和性能分析
- 实践在真实项目中为函数添加覆盖率接近100%的表驱动测试