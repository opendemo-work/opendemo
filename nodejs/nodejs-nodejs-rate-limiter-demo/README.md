# NodeJS限流器演示

## 简介
本项目展示了在Node.js中使用`rate-limiter-flexible`库实现三种常见限流策略：基于内存的简单限流、基于IP地址的访问控制，以及结合Redis的分布式限流（模拟）。这些示例帮助开发者理解如何保护API免受滥用。

## 学习目标
- 理解限流的基本概念和应用场景
- 掌握使用 rate-limiter-flexible 实现不同限流策略
- 学会在Express中集成限流中间件
- 了解限流对系统稳定性的重要性

## 环境要求
- Node.js 版本：v16 或更高版本
- npm 包管理工具（随Node.js自动安装）
- 操作系统：Windows、macOS、Linux 均支持

## 安装依赖的详细步骤
1. 打开终端或命令行工具
2. 进入项目根目录
3. 执行以下命令安装依赖：
   ```bash
   npm install
   ```

## 文件说明
- `simple-rate-limiter.js`: 基于内存的简单请求频率限制器
- `ip-based-limiter.js`: 根据客户端IP进行独立限流
- `redis-mock-limiter.js`: 使用模拟Redis存储的分布式限流（无需真实Redis服务）

## 逐步实操指南

### 步骤1: 启动简单限流服务器
```bash
node simple-rate-limiter.js
```
预期输出：
```
Simple Rate Limiter 服务器运行在 http://localhost:3000
```

然后打开浏览器访问 `http://localhost:3000` 多次，第6次起会看到“请求过于频繁”的提示。

### 步骤2: 启动基于IP的限流服务器
```bash
node ip-based-limiter.js
```
预期输出：
```
IP-Based Rate Limiter 服务器运行在 http://localhost:3001
```
同样访问该地址测试限流效果。

### 步骤3: 启动模拟Redis限流服务器
```bash
node redis-mock-limiter.js
```
预期输出：
```
Redis-Mock Rate Limiter 服务器运行在 http://localhost:3002
```

## 代码解析

### `RateLimiterMemory`
使用内存存储计数，适合单实例应用。每秒最多5次请求，超过则拒绝。

### `RateLimiterMemory` + IP提取
通过 `req.ip` 获取客户端IP，并为每个IP独立计数，防止某个用户影响其他用户。

### 自定义StoreWithTTL类
模拟Redis的过期机制，展示在无Redis环境下如何设计可扩展的存储结构，便于将来替换为真实Redis。

## 预期输出示例
成功响应：
```
你好！这是第1次请求。剩余可用次数：4
```

被限流时响应：
```
状态码：429\n错误：请求过于频繁，请稍后再试。
```

## 常见问题解答

**Q: 为什么我重启后还能继续请求？**\nA: 因为内存限流器在进程重启后重置计数，这是正常行为。

**Q: 如何在生产环境使用Redis？**\nA: 将 `store` 替换为 `RateLimiterRedis` 并连接真实Redis实例即可。

**Q: 能否按用户ID限流？**\nA: 可以，在 `keyGenerator` 中返回 `req.userId` 即可。

## 扩展学习建议
- 阅读 [rate-limiter-flexible 官方文档](https://www.npmjs.com/package/rate-limiter-flexible)
- 学习 Redis 在分布式系统中的作用
- 探索 Token Bucket 与 Leaky Bucket 算法原理
- 实践 JWT 认证 + 限流的组合方案