# Go JSON处理实战演示

## 简介
本示例演示了在Go语言中如何使用标准库 `encoding/json` 进行JSON的序列化（marshal）和反序列化（unmarshal）。通过两个具体场景：结构体转JSON和JSON转结构体，帮助初学者掌握Go中处理JSON数据的基本技能。

## 学习目标
- 理解Go结构体与JSON之间的映射关系
- 掌握 `json.Marshal` 和 `json.Unmarshal` 的使用
- 学会使用结构体标签（struct tags）控制JSON字段名
- 了解常见JSON处理的最佳实践

## 环境要求
- Go 1.16 或更高版本（推荐使用最新稳定版）
- 操作系统：Windows、Linux、macOS 均可

## 安装依赖
本项目仅使用Go标准库，无需额外安装依赖。

## 文件说明
- `main.go`: 主程序，演示结构体与JSON互转
- `advanced.go`: 高级用法，演示嵌套结构和自定义字段处理

## 逐步实操指南

### 步骤1：检查Go环境
```bash
go version
```
**预期输出**：
```bash
go version go1.21.0 darwin/amd64
```

### 步骤2：创建项目目录并进入
```bash
mkdir go-json-demo && cd go-json-demo
```

### 步骤3：复制代码文件
将 `main.go` 和 `advanced.go` 的内容分别保存到对应文件中。

### 步骤4：运行主程序
```bash
go run main.go
```
**预期输出**：
```json
序列化后的JSON: {"name":"张三","age":25,"email":"zhangsan@example.com"}

反序列化成功:
姓名: 张三
年龄: 25
邮箱: zhangsan@example.com
```

### 步骤5：运行高级示例
```bash
go run advanced.go
```
**预期输出**：
```json
带嵌套的JSON: {"user":{"name":"李四","profile":{"age":30,"city":"北京"}},"active":true}
用户姓名: 李四
用户年龄: 30
所在城市: 北京
账户状态: true
```

## 代码解析

### main.go 关键代码段
```go
// 使用 json 标签指定JSON字段名
type Person struct {
    Name  string `json:"name"`
    Age   int    `json:"age"`
    Email string `json:"email"`
}
```
> 解释：结构体字段后的 `json:"xxx"` 是结构体标签，用于指定该字段在JSON中的名称。

```go
// 将结构体编码为JSON字符串
jsonData, err := json.Marshal(person)
```
> 解释：`json.Marshal` 将Go值转换为JSON格式的字节切片。

```go
// 将JSON字符串解码回结构体
var decodedPerson Person
err = json.Unmarshal(jsonData, &decodedPerson)
```
> 解释：`json.Unmarshal` 需要传入目标变量的指针，以便修改其值。

## 预期输出示例
见“逐步实操指南”中的输出示例。

## 常见问题解答

### Q1：为什么结构体字段必须大写开头？
A：Go语言中只有首字母大写的字段才是导出的（exported），`json` 包只能访问导出字段。

### Q2：如何忽略空字段？
A：使用 `,omitempty` 标签，如：`json:"email,omitempty"`。

### Q3：中文乱码怎么办？
A：`json.Marshal` 默认会转义中文，若要保留中文，使用 `json.MarshalIndent` 并设置编码器：`encoder.SetEscapeHTML(false)`。

## 扩展学习建议
- 学习使用 `json.Decoder` 和 `json.Encoder` 处理流式JSON数据
- 探索第三方库如 `ffjson` 或 `easyjson` 提升性能
- 实践从HTTP请求中读取和返回JSON数据