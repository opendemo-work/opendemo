# Go Redis缓存操作演示

## 简介
本项目是一个完整的Go语言示例，展示如何使用`go-redis`库与Redis服务器进行交互，实现常见的缓存操作，包括字符串读写、哈希操作和过期策略管理。

## 学习目标
- 掌握Go中连接Redis的基本方法
- 学会使用Redis作为缓存存储数据
- 理解键值过期机制在缓存中的应用
- 实践结构化数据（如用户信息）的序列化与反序列化

## 环境要求
- Go 1.20 或更高版本
- Redis 6.0+ 服务正在运行（本地或远程）
- 支持 Windows / Linux / macOS

## 安装依赖步骤

1. 克隆或创建项目目录：
```bash
mkdir go-redis-demo && cd go-redis-demo
```

2. 初始化Go模块：
```bash
go mod init go-redis-demo
```

3. 添加 go-redis 依赖：
```bash
go get github.com/redis/go-redis/v9
```

4. 将以下代码保存为 `main.go` 和 `user_cache.go`

## 文件说明
- `main.go`: 主程序入口，演示基本字符串缓存操作
- `user_cache.go`: 演示复杂对象（用户）的缓存处理，使用JSON序列化和哈希操作

## 逐步实操指南

### 第一步：启动Redis服务
确保你已安装并启动Redis。例如在终端运行：
```bash
redis-server
```

### 第二步：运行主程序
```bash
go run main.go
```

**预期输出**：
```
✅ 设置缓存成功: key=welcome, value=Hello from Redis!
✅ 获取缓存成功: Hello from Redis!
✅ 缓存带过期时间设置成功
💤 等待5秒让键过期...
❌ 键已过期或不存在: key=expiring_key
```

### 第三步：运行用户缓存示例
```bash
go run user_cache.go
```

**预期输出**：
```
✅ 用户信息已缓存: user:1001
👤 从缓存读取用户: {ID:1001 Name:Alice Age:30}
✅ 使用HSet缓存用户字段: user:profile:1001
📊 HGetAll 获取用户资料: map[age:30 name:Alice]
```

## 代码解析

### main.go 关键点
- 使用 `rdb.Set()` 写入带TTL的键值对
- 使用 `rdb.Get()` 读取字符串值，并检查 `redis.Nil` 判断键是否存在
- `context.Background()` 提供上下文控制

### user_cache.go 关键点
- 使用 `json.Marshal` 将结构体转为JSON字符串存储
- 使用 `rdb.HSet` 和 `rdb.HGetAll` 对哈希类型进行操作
- 展示了复合键命名约定（如 `user:1001`）

## 预期输出示例
见上文“预期输出”部分。

## 常见问题解答

**Q: 连接被拒绝？**
A: 请确认Redis服务是否运行，默认端口是6379。可通过 `redis-cli ping` 测试连接。

**Q: 如何更改Redis地址？**
A: 修改 `NewClient` 中的 `Addr` 字段，如 `"localhost:6380"`。

**Q: 能否使用TLS连接？**
A: 可以，在Options中设置 `TLSConfig` 字段。

## 扩展学习建议
- 尝试使用Redis管道（Pipelining）提升性能
- 实现分布式锁（`SETNX` 或 `Redlock`）
- 集成到Web服务中作为会话存储
- 使用Redis Streams 实现消息队列