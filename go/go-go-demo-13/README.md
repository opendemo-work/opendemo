# Go语言结构体实战演示

## 简介
本演示项目展示了Go语言中`struct`（结构体）的基本用法，包括结构体的定义、字段访问、匿名结构体、结构体方法等核心概念。适合初学者理解Go如何通过结构体实现数据建模。

## 学习目标
- 掌握Go中结构体的定义与初始化方式
- 理解结构体字段的访问控制
- 学会为结构体定义方法
- 了解匿名结构体和嵌套结构体的应用场景

## 环境要求
- 操作系统：Windows / Linux / macOS（任意）
- Go版本：1.19 或更高版本（推荐使用稳定版）

## 安装依赖的详细步骤
本项目不依赖外部库，仅使用Go标准库，无需额外安装依赖。

1. 下载并安装Go：
   访问 [https://golang.org/dl/](https://golang.org/dl/) 下载对应系统的安装包并安装。

2. 验证安装：
   打开终端或命令行，运行以下命令：
   ```bash
   go version
   ```
   **预期输出**：
   ```
   go version go1.19.x os/arch
   ```

## 文件说明
- `main.go`：主程序文件，演示结构体的基础用法
- `person.go`：定义Person结构体及其相关方法
- `vehicle.go`：演示嵌套结构体和匿名结构体的使用

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir go-struct-demo && cd go-struct-demo
```

### 步骤2：创建代码文件
将以下三个文件内容分别保存到对应路径：
- `main.go`
- `person.go`
- `vehicle.go`

### 步骤3：运行程序
在项目根目录执行：
```bash
go run *.go
```

**预期输出**：
```text
姓名: 张三, 年龄: 25, 是否成年: true
汽车品牌: Tesla, 型号: Model 3
匿名车辆: BMW X5
```

## 代码解析

### `person.go`
```go
type Person struct {
    Name string
    Age  int
}
```
定义了一个包含姓名和年龄的结构体。Go中没有类，但可通过结构体+方法模拟面向对象行为。

```go
func (p Person) IsAdult() bool {
    return p.Age >= 18
}
```
为Person定义了`IsAdult`方法，接收者为值类型，适用于小型结构体。

### `vehicle.go`
```go
type Vehicle struct {
    Brand string
    Model string
}

type Car struct {
    Person  // 嵌入式结构体，实现类似“继承”的效果
    Vehicle // 匿名字段，可直接访问其字段
}
```
展示了组合优于继承的设计理念，Car包含了Person和Vehicle的能力。

## 常见问题解答

**Q: 结构体字段首字母必须大写吗？**
A: 是的，首字母大写表示导出（public），小写为包内私有（private）。

**Q: 方法可以修改结构体内容吗？**
A: 可以，需使用指针接收者：`func (p *Person) SetAge(age int)`。

**Q: Go中有构造函数吗？**
A: 没有，但通常约定使用`NewXxx()`函数返回实例，如`func NewPerson(name string, age int) Person`。

## 扩展学习建议
- 学习JSON序列化：尝试使用`encoding/json`将结构体转为JSON
- 实践接口（interface）：定义`Stringer`接口来自定义输出
- 阅读官方Effective Go文档中的“Structs”章节