# Go并发原语实战演示

## 简介
本示例演示了Go语言中`sync`包提供的三种重要同步原语：`WaitGroup`、`Once`和`Pool`的实际使用场景。通过三个独立但完整的代码文件，帮助开发者理解如何高效安全地处理并发任务、确保单次初始化和对象复用。

## 学习目标
- 掌握 WaitGroup 如何协调多个 goroutine 的完成
- 理解 Once 在单例初始化等场景中的作用
- 学会使用 Pool 减少内存分配开销，提升性能
- 熟悉 Go 并发编程的最佳实践

## 环境要求
- Go 1.19 或更高版本（推荐稳定版）
- 支持终端命令行操作（Windows/Linux/Mac 均可）

## 安装依赖的详细步骤
本项目不依赖外部库，仅使用标准库，无需额外安装依赖。

## 文件说明
- `waitgroup_demo.go`：使用 WaitGroup 等待多个并发任务完成
- `once_demo.go`：演示 Once 保证某段代码只执行一次
- `pool_demo.go`：展示 Pool 如何缓存和复用临时对象

## 逐步实操指南

### 步骤 1: 创建项目目录
```bash
mkdir go-sync-demo && cd go-sync-demo
```

### 步骤 2: 创建并写入代码文件
将以下内容分别保存为对应文件名：

创建 waitgroup_demo.go：
```bash
cat > waitgroup_demo.go << EOF
// 内容粘贴自 waitgroup_demo.go 示例
EOF
```

创建 once_demo.go：
```bash
cat > once_demo.go << EOF
// 内容粘贴自 once_demo.go 示例
EOF
```

创建 pool_demo.go：
```bash
cat > pool_demo.go << EOF
// 内容粘贴自 pool_demo.go 示例
EOF
```

### 步骤 3: 运行每个示例

运行 WaitGroup 示例：
```bash
go run waitgroup_demo.go
```
**预期输出**：
```
Worker 0 开始工作...
Worker 1 开始工作...
Worker 2 开始工作...
所有 worker 已完成
```

运行 Once 示例：
```bash
go run once_demo.go
```
**预期输出**：
```
第一次调用：初始化开始
初始化完成
第二次调用：无操作（已初始化）
```

运行 Pool 示例：
```bash
go run pool_demo.go
```
**预期输出**：
```
获取对象: 数据 A
归还对象: 数据 A
获取对象: 数据 B
从池中重用对象: 数据 A
```

## 代码解析

### waitgroup_demo.go
使用 `sync.WaitGroup` 来等待三个并发 worker 完成任务。`Add(3)` 设置需等待的 goroutine 数量，每个 goroutine 结束时调用 `Done()`，主函数通过 `Wait()` 阻塞直到全部完成。

### once_demo.go
利用 `sync.Once` 确保 `initialize()` 函数无论被调用多少次，都只执行一次。常用于配置加载、单例初始化等场景。

### pool_demo.go
`sync.Pool` 缓存临时对象以减少 GC 压力。`Get` 获取对象（若为空则新建），`Put` 归还对象供后续复用。注意 Pool 不保证一定命中。

## 预期输出示例
见各运行步骤下的输出说明。

## 常见问题解答

**Q: WaitGroup 是否可以重复使用？**
A: 不建议。WaitGroup 必须在 `Wait()` 返回后重新 `Add` 才能再次使用，否则可能引发 panic。应确保生命周期清晰。

**Q: Once 能否跨 goroutine 保证唯一性？**
A: 可以。`sync.Once` 是线程安全的，多个 goroutine 同时调用也只会执行一次。

**Q: Pool 中的对象会被自动清理吗？**
A: 会。Go 的运行时会在适当时候清除 Pool 中的对象以减少内存占用，因此不能依赖其长期存在。

## 扩展学习建议
- 阅读官方文档：https://pkg.go.dev/sync
- 学习 `Mutex` 和 `Cond` 等其他 sync 原语
- 实践 context 包与 goroutine 生命周期管理结合使用