# Go BadgerDB 内存数据库存储Demo

## 简介
本项目演示了如何在Go中使用BadgerDB——一个快速、嵌入式的持久化键值存储数据库。它适用于需要高性能本地存储的应用场景，如缓存、会话存储或轻量级配置管理。

## 学习目标
- 理解BadgerDB的基本概念和优势
- 掌握打开和关闭数据库连接的方法
- 实现基本的CRUD操作（创建、读取、更新、删除）
- 使用事务确保数据一致性
- 安全地遍历键值对

## 环境要求
- Go 1.19 或更高版本
- 操作系统：Windows、Linux、macOS 均支持
- 磁盘空间：至少50MB可用空间（用于数据库文件）

## 安装依赖的详细步骤

1. 确保已安装Go环境：
   ```bash
   go version
   # 预期输出: go version go1.19+ ...
   ```

2. 初始化Go模块并添加BadgerDB依赖：
   ```bash
   mkdir badger-demo && cd badger-demo
   go mod init badger-demo
   go get github.com/dgraph-io/badger/v3@v3.2107.0
   ```

## 文件说明
- `main.go`：主程序，演示基本的Put/Get/Delete操作
- `iterator.go`：演示如何安全遍历所有键值对
- `go.mod`：Go模块依赖声明文件

## 逐步实操指南

### 步骤1：创建 main.go
```bash
cat > main.go <<EOF
// 将自动写入代码内容
EOF
```

### 步骤2：创建 iterator.go
```bash
cat > iterator.go <<EOF
// 将自动写入代码内容
EOF
```

### 步骤3：运行程序
```bash
go run main.go
# 预期输出：成功插入、读取、更新和删除键值对的日志

go run iterator.go
# 预期输出：显示当前数据库中的所有键值对
```

## 代码解析

### main.go 关键点
- `badger.Open()`：以指定目录路径打开数据库，若不存在则自动创建
- `db.NewTransaction()`：开启读写事务，保证原子性
- `txn.Set()` 和 `txn.Get()`：设置与获取键值，值为字节数组
- `view` 与 `update`：分别用于只读和读写事务，避免锁冲突
- `defer db.Close()`：确保程序退出前正确释放资源

### iterator.go 关键点
- `db.NewIterator()`：创建前向迭代器遍历所有键
- `iter.Rewind()`：将迭代器定位到第一个键
- `iter.Next()`：逐个移动到下一个键
- `iter.Item()`：获取当前项，通过 `Key()` 和 `Value()` 提取数据
- `string(item.Value())`：将字节切片转换为字符串输出

## 预期输出示例
```text
✅ 成功写入: name -> Gopher
✅ 成功读取: name = Gopher
✅ 成功更新: visits -> 1
✅ 成功删除: temp_data

🔍 当前数据库内容:
key: name, value: Gopher
key: visits, value: 1
```

## 常见问题解答

**Q: 运行时报错 'permission denied'？**
A: 检查当前用户是否有对运行目录的读写权限，尤其是Windows上防病毒软件可能锁定文件。

**Q: 如何清空数据库？**
A: 删除 `./badger-data` 目录即可彻底重置：`rm -rf badger-data`

**Q: BadgerDB 是纯内存数据库吗？**
A: 不是。它是持久化键值存储，默认将数据写入磁盘，但可通过配置启用纯内存模式（本Demo未使用）。

**Q: 可以多个进程同时访问同一个BadgerDB吗？**
A: 不可以。BadgerDB不支持多进程并发访问，仅允许多goroutine在同一进程中共享实例。

## 扩展学习建议
- 探索BadgerDB的TTL功能实现自动过期缓存
- 结合Gin/Echo框架构建REST API接口操作数据
- 使用`sync=true`选项增强数据安全性
- 尝试批量写入优化性能
- 阅读官方文档了解LSM-tree底层原理