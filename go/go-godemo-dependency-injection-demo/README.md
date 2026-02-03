# Go依赖注入设计模式实战Demo

## 简介
本项目通过两个典型场景展示Go语言中依赖注入（Dependency Injection, DI）设计模式的实践应用。DI帮助我们实现松耦合、可测试和可维护的代码结构。

## 学习目标
- 理解依赖注入的核心思想
- 掌握Go中通过接口和构造函数实现DI的方法
- 学会编写可测试的服务组件
- 提升代码的模块化与扩展性

## 环境要求
- Go 1.19 或更高版本
- 操作系统：Windows / Linux / macOS（均支持）

## 安装依赖的详细步骤
1. 确保已安装Go环境：
   ```bash
   go version
   ```
   预期输出示例：`go version go1.21.0 darwin/amd64`

2. 克隆或创建项目目录并进入：
   ```bash
   mkdir di-demo && cd di-demo
   ```

3. 初始化Go模块：
   ```bash
   go mod init di-demo
   ```

## 文件说明
- `main.go`：主程序入口，演示基础依赖注入
- `service.go`：定义服务逻辑与接口抽象
- `mock_service.go`：模拟服务用于测试场景（扩展用途）

## 逐步实操指南

### 步骤1：创建 service.go
```bash
cat > service.go <<EOF
// 代码内容由生成器提供，粘贴即可
EOF
```

### 步骤2：创建 main.go
```bash
cat > main.go <<EOF
// 代码内容由生成器提供
EOF
```

### 步骤3：运行程序
```bash
go run main.go
```

**预期输出**：
```
用户服务正在处理: Alice
邮件服务发送消息到: alice@example.com, 内容: 欢迎注册！
通知中心完成通知流程
```

## 代码解析

### service.go 中的关键点
- 定义了 `UserService` 和 `EmailService` 接口，实现抽象解耦
- 使用结构体组合具体实现，便于替换
- 构造函数接受接口类型，体现控制反转

### main.go 中的关键点
- 在 `main` 函数中显式创建依赖实例并注入
- 不在内部 new 对象，而是由外部传入，符合DI原则
- 易于替换为 mock 实现进行单元测试

## 常见问题解答

**Q: 为什么不用全局变量直接调用？**
A: 全局调用导致强耦合，难以测试和替换实现；DI提升可维护性和可测试性。

**Q: 是否必须使用接口？**
A: 在Go中，接口是实现DI的关键机制，它允许不同实现互换而不影响调用方。

**Q: 如何做单元测试？**
A: 可以创建 mock 实现（如 MockEmailService），在测试中注入以验证行为。

## 扩展学习建议
- 尝试使用 Wire（Google出品的DI工具）来自动生成依赖图
- 学习 Hexagonal Architecture（六边形架构）如何结合DI构建清晰边界
- 阅读 Uber Go Style Guide 进一步规范编码风格