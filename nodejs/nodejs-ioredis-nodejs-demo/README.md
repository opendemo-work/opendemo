# ioredis Node.js 缓存客户端实战演示

## 简介
本项目是一个基于 Node.js 和 ioredis 的 Redis 缓存操作演示。通过三个具体场景展示如何连接 Redis、进行基本数据操作、设置过期缓存以及处理哈希结构数据。

## 学习目标
- 掌握 ioredis 客户端的基本初始化与连接方式
- 学会使用 Redis 进行字符串和哈希类型的读写操作
- 理解缓存过期机制及其应用场景
- 提升对异步操作（async/await）在实际项目中的运用能力

## 环境要求
- Node.js 版本：v14 或更高（推荐 v16+）
- Redis 服务器：本地或远程运行，端口默认为 6379
- 操作系统：Windows、Linux、macOS 均支持

> 注意：本项目不依赖 Python 或 Java

## 安装依赖的详细步骤

1. 确保已安装 Node.js 和 npm
   ```bash
   node -v
   npm -v
   ```

2. 克隆项目或创建项目目录并进入
   ```bash
   mkdir ioredis-demo && cd ioredis-demo
   npm init -y
   ```

3. 安装 ioredis 依赖
   ```bash
   npm install ioredis
   ```

## 文件说明
- `basic-operations.js`：基础字符串读写与过期设置
- `hash-operations.js`：Redis 哈希结构的操作示例
- `connection-pool.js`：使用连接池配置提高性能

## 逐步实操指南

### 步骤 1：启动 Redis 服务
确保 Redis 正在运行。若未安装，请先下载并启动：
```bash
redis-server
```

### 步骤 2：保存代码文件
将以下三个文件放入项目根目录：
- basic-operations.js
- hash-operations.js
- connection-pool.js

### 步骤 3：运行每个示例

运行基础操作：
```bash
node basic-operations.js
```
**预期输出**：
```
✅ 设置用户 john 成功
🔍 获取用户数据: { name: 'John Doe', age: '30' }
⏳ 2秒后缓存将过期...
🗑️ 缓存已过期，获取结果: null
```

运行哈希操作：
```bash
node hash-operations.js
```
**预期输出**：
```
🧩 使用 HSET 写入用户信息
🔍 使用 HGETALL 获取完整用户信息: { name: 'Alice', email: 'alice@example.com' }
📧 单独获取邮箱: alice@example.com
```

运行连接池示例：
```bash
node connection-pool.js
```
**预期输出**：
```
📦 创建带连接池的 Redis 实例
🚀 执行并发请求...
✅ 请求 1 完成: PONG
✅ 请求 2 完成: PONG
✅ 请求 3 完成: PONG
```

## 代码解析

### basic-operations.js
- 使用 `new Redis()` 创建连接
- `set(key, value, 'EX', seconds)` 实现带过期时间的缓存
- 利用 `setTimeout` 模拟延迟验证过期效果

### hash-operations.js
- 使用 `hset` 和 `hgetall` 操作哈希类型，适合存储对象
- 高效读取字段子集，减少网络传输

### connection-pool.js
- ioredis 默认启用连接池，无需额外配置
- 展示并发请求下的稳定表现，适用于高负载场景

## 预期输出示例
见“逐步实操指南”部分。

## 常见问题解答

**Q: 报错 `Error: connect ECONNREFUSED 127.0.0.1:6379`？**
A: 表示无法连接 Redis 服务，请确认是否已启动 `redis-server`。

**Q: 如何连接远程 Redis？**
A: 修改构造函数参数：`new Redis({ host: 'your-host', port: 6379, password: 'your-pass' })`

**Q: 是否需要手动关闭连接？**
A: 生产环境中建议在程序退出时调用 `redis.quit()` 关闭连接。

## 扩展学习建议
- 学习 Redis 事务（MULTI/EXEC）
- 探索 Lua 脚本在 Redis 中的使用
- 结合 Express/Koa 构建带缓存的 Web API
- 使用 Redis Cluster 模式实现分布式缓存
- 尝试 ioredis 的哨兵和主从模式支持