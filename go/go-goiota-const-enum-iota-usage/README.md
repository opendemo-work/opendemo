# Go常量枚举与iota使用示例

## 简介
本示例演示了在Go语言中如何使用`iota`关键字创建枚举类型的多种常见模式，包括基础枚举、位掩码枚举和自定义值枚举。通过本Demo，你将掌握Go中模拟枚举的最佳实践。

## 学习目标
- 理解Go中没有原生枚举类型的特点
- 掌握`iota`的工作原理和使用场景
- 学会使用常量组创建类型安全的枚举
- 了解位运算在枚举中的应用

## 环境要求
- Go 1.16 或更高版本
- 支持的操作系统：Windows、Linux、macOS

## 安装依赖的详细步骤
本项目无需外部依赖，只需安装Go语言环境：

1. 访问 [https://golang.org/dl/](https://golang.org/dl/) 下载对应操作系统的Go安装包
2. 按照官方指南完成安装
3. 验证安装：
   ```bash
   go version
   ```
   预期输出：`go version go1.xx.x os/arch`

## 文件说明
- `main.go`：主程序，展示基础枚举用法
- `bitmask_enum.go`：展示位掩码枚举（权限系统示例）
- `custom_enum.go`：展示自定义值的枚举模式

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir go-enum-demo && cd go-enum-demo
```

### 步骤2：创建并运行主程序
```bash
# 创建main.go文件（内容见下方）
# 然后执行
go run main.go
```
预期输出：
```
状态：Pending
状态字符串：PENDING
```

### 步骤3：运行位掩码枚举示例
```bash
# 创建bitmask_enum.go文件
# 然后执行
go run bitmask_enum.go
```
预期输出：
```
用户权限：READ|WRITE
有读权限：true
有执行权限：false
```

### 步骤4：运行自定义值枚举示例
```bash
# 创建custom_enum.go文件
# 然后执行
go run custom_enum.go
```
预期输出：
```
HTTP状态码：200
状态文本：OK
```

## 代码解析

### main.go 关键代码段
```go
const (
	StatusPending = iota // 值为0
	StatusApproved         // 值为1
	StatusRejected         // 值为2
)
```
- 使用`iota`从0开始自动递增赋值
- 每行定义一个常量，iota在每行后自动加1

### bitmask_enum.go 关键代码段
```go
const (
	PermissionRead  = 1 << iota // 1 (二进制: 001)
	PermissionWrite               // 2 (二进制: 010)
	PermissionExecute             // 4 (二进制: 100)
)
```
- 使用左移位运算创建2的幂次方值
- 可以通过按位或组合权限，按位与检查权限

### custom_enum.go 关键代码段
```go
const (
	HTTPStatusOK = iota + 200 // 从200开始
	_                           // 跳过下一个值
	HTTPStatusCreated           // 201
)
```
- 通过`iota + value`设置起始值
- 使用`_`跳过不需要的值

## 预期输出示例
完整运行三个文件的预期输出已在"逐步实操指南"中列出。

## 常见问题解答

**Q: 为什么Go没有原生的枚举类型？**
A: Go设计哲学强调简单性，通过const和iota已经能很好满足枚举需求，无需额外语言特性。

**Q: iota从什么时候重置？**
A: 在每个const声明块开始时，iota重置为0。

**Q: 如何为枚举添加String()方法？**
A: 可以为枚举类型定义String() string方法，如示例中所示，实现优雅的字符串输出。

## 扩展学习建议
- 学习Go的`stringer`工具来自动生成String()方法
- 研究标准库中如`net/http`包的状态码定义方式
- 探索使用iota实现更复杂的模式，如环形枚举