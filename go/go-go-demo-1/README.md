# Go反射与元编程实战演示

## 简介
本项目通过三个具体的Go代码示例，深入展示`reflect`包在元编程中的强大能力。涵盖动态访问结构体字段、修改不可导出字段、以及动态调用方法等高级场景。

## 学习目标
- 理解Go反射的基本概念和核心API
- 掌握使用`reflect`动态读取和修改结构体字段
- 学会通过反射调用方法
- 了解反射的性能影响与适用场景

## 环境要求
- Go 1.19 或更高版本（稳定版）
- 支持的操作系统：Windows、Linux、macOS

## 安装依赖的详细步骤
本项目不依赖外部库，仅使用Go标准库 `reflect`，无需额外安装。

## 文件说明
- `main.go`: 主程序，演示反射访问和修改结构体字段
- `dynamic_call.go`: 演示通过反射动态调用结构体方法
- `README.md`: 当前文档

## 逐步实操指南

### 步骤1: 创建项目目录
```bash
mkdir go-reflect-demo
cd go-reflect-demo
```

### 步骤2: 创建并写入代码文件
将以下内容分别保存为对应文件名：

创建 main.go:
```bash
cat > main.go << 'EOF'
// 复制 main.go 的完整内容
EOF
```

创建 dynamic_call.go:
```bash
cat > dynamic_call.go << 'EOF'
// 复制 dynamic_call.go 的完整内容
EOF
```

### 步骤3: 初始化Go模块
```bash
go mod init reflect-demo
```

### 步骤4: 运行程序
```bash
go run main.go
go run dynamic_call.go
```

### 预期输出（main.go）
```
原始Name: Alice
通过反射读取Name: Alice
修改后Name: Bob
```

### 预期输出（dynamic_call.go）
```
通过反射调用 Greet 方法:
Hello, I'm Alice
```

## 代码解析

### main.go 关键点
- 使用 `reflect.ValueOf(&s).Elem()` 获取结构体可寻址的Value，以便修改字段
- 通过 `.FieldByName("Name")` 动态访问字段
- 使用 `CanSet()` 判断字段是否可被反射修改

### dynamic_call.go 关键点
- 使用 `MethodByName("Greet")` 获取方法的Value
- 调用 `.Call(nil)` 执行无参数的方法
- 展示反射如何绕过静态方法调用机制

## 预期输出示例
见“逐步实操指南”部分。

## 常见问题解答

**Q: 为什么修改字段前要使用 .Elem()？**
A: 因为 `reflect.ValueOf(s)` 传递的是值拷贝，必须传指针并通过 `.Elem()` 获取指向原始对象的引用才能修改。

**Q: 反射能修改未导出（小写）字段吗？**
A: 不能，即使使用反射，未导出字段也无法被修改，这是Go的封装安全机制。

**Q: 反射会影响性能吗？**
A: 是的，反射比直接调用慢很多，应避免在性能敏感路径中频繁使用。

## 扩展学习建议
- 阅读Go官方文档 reflect 包：https://pkg.go.dev/reflect
- 尝试实现一个通用的结构体转JSON函数（类似简易版encoding/json）
- 学习使用 `text/template` 或 `github.com/mitchellh/mapstructure` 等结合反射的库