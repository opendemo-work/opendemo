# Go数据库SQL事务操作演示

本项目是一个完整的Go语言示例，用于演示如何使用标准库`database/sql`执行SQL数据库的CRUD（创建、读取、更新、删除）操作，并重点展示事务（Transaction）的正确使用方式。

## 学习目标

- 理解Go中`database/sql`包的基本用法
- 掌握数据库连接的初始化与关闭
- 实践CRUD操作在事务中的安全执行
- 学会使用事务确保数据一致性
- 避免常见的资源泄漏和错误处理疏漏

## 环境要求

- Go 1.18 或更高版本
- 操作系统：Windows、Linux、macOS（均支持）

## 安装依赖的详细步骤

1. 确保已安装Go环境：
   ```bash
   go version
   # 预期输出：go version go1.18+ ...
   ```

2. 初始化Go模块（如果尚未初始化）：
   ```bash
   go mod init db-demo
   ```

3. 添加SQLite驱动依赖：
   ```bash
   go get github.com/mattn/go-sqlite3
   ```

## 文件说明

- `main.go`：主程序文件，包含数据库初始化、事务性CRUD操作演示
- `go.mod`：Go模块依赖声明文件

## 逐步实操指南

1. 创建项目目录并进入：
   ```bash
   mkdir db-demo && cd db-demo
   ```

2. 将以下内容保存为 `main.go`

3. 创建 `go.mod` 文件（或运行 `go mod init db-demo`）

4. 运行程序：
   ```bash
   go run main.go
   ```

### 预期输出

```
用户创建成功，ID: 1
事务内查询 - 用户: Alice, 年龄: 30
更新用户年龄成功
删除用户成功
所有操作在事务中完成
```

## 代码解析

### 打开数据库连接
```go
sqlDB, err := sql.Open("sqlite3", "./demo.db")
```
使用SQLite3驱动打开一个本地数据库文件。`sql.Open`并不立即建立连接，而是在第一次需要时才连接。

### 开启事务
```go
tx, err := db.Begin()
```
通过`Begin()`启动一个新事务。后续操作都应在`*sql.Tx`上执行以保证原子性。

### 事务回滚与提交
使用`defer tx.Rollback()`确保即使出错也能回滚；仅当所有操作成功后才调用`tx.Commit()`。

### CRUD操作
- Create: 使用`Tx.Exec`插入记录
- Read: 使用`Tx.QueryRow`读取单行
- Update: 更新字段值
- Delete: 删除记录
所有操作都在同一事务中完成，保障一致性。

## 常见问题解答

**Q: 为什么使用 defer tx.Rollback()？**
A: 因为初始时事务处于“未提交”状态。若后续失败，`Rollback()`会撤销所有更改；若成功，在`Commit()`后再次`Rollback()`无副作用。

**Q: 可以不用事务吗？**
A: 可以，但无法保证多步操作的原子性。例如中途失败会导致数据不一致。

**Q: Windows下编译报错：_cgo_export.c?**
A: 确保安装了GCC（推荐使用MinGW或MSYS2），或使用预编译二进制方式运行。

## 扩展学习建议

- 尝试将SQLite替换为PostgreSQL或MySQL
- 使用`sqlx`或`gorm`等高级ORM库重写本示例
- 添加单元测试验证事务行为
- 实现连接池配置与监控
- 学习Context超时控制在数据库操作中的应用