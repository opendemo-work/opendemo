# Go嵌入式编程示例

本项目演示了Go语言中通过结构体嵌入（embedding）实现代码复用和组合的设计模式。与传统面向对象的继承不同，Go推荐使用组合优于继承，而嵌入是实现组合的核心机制。

## 学习目标

- 理解Go中的结构体嵌入机制
- 掌握匿名字段的使用方法
- 学会通过嵌入实现行为复用
- 区分嵌入与继承的概念差异

## 环境要求

- Go 1.19 或更高版本
- 支持终端操作的系统（Windows / Linux / macOS）

## 安装依赖的详细步骤

1. 确保已安装Go环境：
   ```bash
   go version
   ```
   预期输出类似：`go version go1.21.0 darwin/amd64`

2. 克隆或创建项目目录并进入：
   ```bash
   mkdir go-embedding-demo && cd go-embedding-demo
   ```

3. 初始化Go模块：
   ```bash
   go mod init embedding-demo
   ```

## 文件说明

- `main.go`: 演示基本结构体嵌入和方法提升
- `advanced.go`: 展示嵌入中的字段遮蔽与接口组合
- `go.mod`: Go模块依赖声明文件

## 逐步实操指南

1. 创建 `main.go`:
   ```bash
   touch main.go
   # 将main.go内容复制进去
   ```

2. 创建 `advanced.go`:
   ```bash
   touch advanced.go
   # 将advanced.go内容复制进去
   ```

3. 运行程序：
   ```bash
   go run .
   ```

### 预期输出
```
员工姓名: 张三, 职位: 开发工程师, 部门: 技术部
动物名称: 小黑, 种类: 狗, 发出声音: 汪汪！
高级员工: 李四, 角色: 管理员, 权限: 读写执行
```

## 代码解析

### main.go 解析

- `Person` 结构体被嵌入到 `Employee` 中，使得 `Employee` 自动获得 `Name` 字段和 `Greet` 方法
- Go的“方法提升”机制允许直接调用嵌入类型的方法
- 使用命名字段 `Position` 和嵌入 `Department` 实现多层组合

### advanced.go 解析

- 嵌入接口 `Speaker` 实现行为抽象
- `AdminUser` 同时嵌入结构体和接口，展示灵活组合能力
- 演示了当外层结构定义同名字段时，会遮蔽内层嵌入字段

## 常见问题解答

**Q: Go中有继承吗？**
A: Go没有传统意义上的继承。它使用结构体嵌入来实现类似功能，但本质是组合而非继承。

**Q: 如何调用被遮蔽的嵌入字段？**
A: 可以通过类型名显式访问，如 `e.Person.Name` 即使 `Employee` 有 `Name` 字段。

**Q: 嵌入必须是结构体吗？**
A: 不是，也可以嵌入接口，这在构建可扩展API时非常有用。

## 扩展学习建议

- 阅读《Effective Go》中的“Embedding”章节
- 学习标准库中 `net/http.Request` 和 `http.ResponseWriter` 的使用
- 尝试实现一个带有日志功能的嵌入式服务结构