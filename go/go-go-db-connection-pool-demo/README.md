# Go数据库连接池管理演示

## 简介
本项目演示了如何在Go语言中使用`database/sql`包进行数据库连接池的配置与管理，重点展示连接池的最佳实践，包括最大连接数控制、空闲连接管理、生命周期设置以及并发访问下的资源安全性。

## 学习目标
- 理解数据库连接池的作用和重要性
- 掌握Go中`sql.DB`的连接池配置方法
- 学会合理设置连接池参数以优化性能
- 了解连接泄漏的风险及防范措施

## 环境要求
- Go 1.19 或更高版本
- 操作系统：Windows / Linux / macOS（均支持）

## 安装依赖步骤
```bash
# 克隆项目（假设已创建目录）
go mod init dbpool-demo
go get github.com/mattn/go-sqlite3
```

> 注意：`mattn/go-sqlite3` 是纯Go驱动，无需外部C库，跨平台兼容性好。

## 文件说明
- `main.go`: 主程序，演示基础连接池配置和使用
- `advanced_pool.go`: 高级用法，展示连接池调优和监控
- `utils/db.go`: 数据库初始化工具函数

## 逐步实操指南

### 步骤1: 创建项目目录并初始化模块
```bash
mkdir dbpool-demo && cd dbpool-demo
go mod init dbpool-demo
```

**预期输出**:
```
go: creating new go.mod: module dbpool-demo
```

### 步骤2: 创建代码文件
将示例中的三个Go文件内容分别写入对应路径。

### 步骤3: 下载依赖
```bash
go mod tidy
```

**预期输出**:
```
go: downloading github.com/mattn/go-sqlite3 v1.14.16
...
go: added github.com/mattn/go-sqlite3 v1.14.16
```

### 步骤4: 运行程序
```bash
go run main.go
```

**预期输出**:
```
[INFO] 数据库连接池已初始化
[INFO] 执行查询: 当前连接数=1, 空闲连接=0
[INFO] 查询成功，结果: 1
[INFO] 连接池状态 -> 打开连接: 1, 在用: 0, 空闲: 1
[INFO] 程序退出，连接将自动关闭
```

## 代码解析

### main.go - 基础连接池配置
```go
// 设置最大连接数
db.SetMaxOpenConns(5)
// 设置最大空闲连接
db.SetMaxIdleConns(3)
// 设置连接最长存活时间
db.SetConnMaxLifetime(time.Minute)
```
这些设置防止连接过多或过久导致资源浪费。

### advanced_pool.go - 并发压测模拟
通过启动多个goroutine并发访问数据库，验证连接池的并发控制能力，并定期打印状态防止连接泄漏。

## 预期输出示例
见“逐步实操指南”中的运行结果部分。

## 常见问题解答

**Q: 为什么需要连接池？**
A: 避免频繁创建/销毁连接带来的性能开销，提升响应速度和系统稳定性。

**Q: 如何避免连接泄漏？**
A: 确保每次`Query`后调用`rows.Close()`，使用`defer`保障执行；同时设置`SetConnMaxLifetime`强制回收长连接。

**Q: SetMaxIdleConns 和 SetMaxOpenConns 的区别？**
A: `MaxOpenConns`是总共最多打开的连接数，包含正在使用的和空闲的；`MaxIdleConns`只是其中保持复用的空闲连接上限。

## 扩展学习建议
- 阅读官方文档：https://pkg.go.dev/database/sql
- 实践MySQL/PostgreSQL驱动替换SQLite
- 结合Prometheus监控连接池指标
- 使用`sqlmock`进行单元测试