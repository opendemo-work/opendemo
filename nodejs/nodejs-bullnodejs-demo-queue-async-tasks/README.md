# Bull队列异步任务处理Node.js Demo

## 简介
本示例演示如何使用 Bull 队列在 Node.js 中处理异步任务。Bull 是基于 Redis 构建的高性能、可靠的任务队列库，适用于邮件发送、数据处理等耗时操作。

## 学习目标
- 理解 Bull 队列的基本概念（生产者、消费者）
- 掌握如何定义和处理异步任务
- 学会使用 Redis 作为消息中间件
- 实践任务重试、失败处理机制

## 环境要求
- Node.js 版本：v16 或更高
- Redis 服务器：v6.0+（本地或远程）
- 操作系统：Windows / Linux / macOS（跨平台兼容）

## 安装依赖的详细步骤
1. 确保已安装 Node.js 和 npm
   ```bash
   node -v
   npm -v
   ```
   预期输出：v16.x.x 或更高

2. 安装项目依赖
   ```bash
   npm install
   ```

3. 启动本地 Redis 服务（如未运行）
   - 下载地址：https://redis.io/download
   - 启动命令（Linux/macOS）：`redis-server`
   - Windows 用户可使用 WSL 或 Redis for Windows

## 文件说明
- `producer.js`：任务生产者，向队列添加任务
- `consumer.js`：任务消费者，从队列中取出并处理任务
- `.env`：环境变量配置文件
- `package.json`：项目依赖声明

## 逐步实操指南

### 第一步：启动消费者（监听任务）
```bash
node consumer.js
```
预期输出：
```
✅ 消费者已启动，正在监听 'emailQueue' 队列...
```

### 第二步：启动生产者（发送任务）
打开新终端窗口，运行：
```bash
node producer.js
```
预期输出：
```
✅ 任务已加入队列，任务ID: 1
```

### 第三步：观察消费者输出
消费者终端将显示：
```
📨 正在处理任务 #1: 发送邮件给 example@example.com
✅ 任务 #1 处理完成
```

## 代码解析

### producer.js 关键代码段
```javascript
const job = await emailQueue.add({ to, subject }, { attempts: 3 });
```
- `add()` 方法将任务推入队列
- `{ attempts: 3 }` 表示失败后自动重试最多3次

### consumer.js 关键代码段
```javascript
emailQueue.process(async (job) => { ... });
```
- `process()` 注册任务处理器
- 所有加入队列的任务都会被此函数处理

## 预期输出示例
### 生产者输出：
```
✅ 任务已加入队列，任务ID: 1
```

### 消费者输出：
```
✅ 消费者已启动，正在监听 'emailQueue' 队列...
📨 正在处理任务 #1: 发送邮件给 example@example.com
✅ 任务 #1 处理完成
```

## 常见问题解答

**Q1: 报错 `Redis connection failed`？**
A: 请确保 Redis 服务正在运行，并检查 `.env` 中的连接配置。

**Q2: 任务没有被消费？**
A: 确保消费者先于生产者启动，且两者使用相同的队列名称。

**Q3: 如何查看队列中的任务？**
A: 使用 Redis CLI：`redis-cli` → `KEYS *` 查看所有键。

## 扩展学习建议
- 学习 Bull Board：为 Bull 提供可视化界面
- 实现优先级队列（priority 选项）
- 添加任务超时和延迟执行功能
- 结合 Express 构建 REST API 触发任务
- 使用 Docker 部署 Redis 和应用