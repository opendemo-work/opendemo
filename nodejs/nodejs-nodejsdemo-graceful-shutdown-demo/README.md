# Node.js优雅关闭实践Demo

## 简介
本示例展示了在Node.js中如何实现**优雅关闭（Graceful Shutdown）**，即当接收到系统终止信号（如SIGTERM、SIGINT）时，停止接收新请求，但允许正在进行的请求完成后再退出进程。这在生产环境中至关重要，可避免服务中断导致的数据丢失或客户端错误。

## 学习目标
- 理解优雅关闭的重要性
- 掌握监听系统信号（SIGTERM/SIGINT）的方法
- 学会安全关闭HTTP服务器并释放资源
- 实践Node.js进程生命周期管理

## 环境要求
- Node.js 14.x 或更高版本（推荐 v16+）
- npm（随Node.js自动安装）
- 操作系统：Windows、Linux、macOS 均支持

## 安装依赖的详细步骤
1. 打开终端（命令行工具）
2. 进入项目目录：`cd graceful-shutdown-demo`
3. 安装依赖：`npm install`

## 文件说明
- `server.js`: 主HTTP服务器，模拟正常请求和延迟请求
- `cleanup.js`: 演示带资源清理的优雅关闭
- `package.json`: 项目配置和依赖声明

## 逐步实操指南

### 步骤1: 初始化项目（可选）
```bash
mkdir graceful-shutdown-demo
cd graceful-shutdown-demo
npm init -y
```

### 步骤2: 创建代码文件
将以下内容保存为 `server.js` 和 `cleanup.js`，并创建 `package.json`。

### 步骤3: 启动服务器
```bash
node server.js
```

### 预期输出：
```
✅ 服务器正在运行于 http://localhost:3000
💡 发送 SIGINT (Ctrl+C) 或 SIGTERM 以触发优雅关闭
```

### 步骤4: 测试优雅关闭
打开另一个终端，发送请求：
```bash
# 正常请求
curl http://localhost:3000/

# 模拟长请求
curl http://localhost:3000/slow
```

然后在服务器终端按下 `Ctrl+C`（发送SIGINT）。

### 预期行为：
- 服务器停止接受新连接
- 已开始的 `/slow` 请求将继续执行完成（5秒）
- 所有活动请求完成后，打印清理日志并退出

## 代码解析

### server.js 关键逻辑
```js
// 监听终止信号
process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);

// 关闭服务器前，拒绝新连接，等待现有请求完成
const shutdown = () => {
  console.log('\n⏹ 正在关闭服务器...');
  server.close(() => {
    console.log('✅ HTTP服务器已关闭');
    // 可在此处关闭数据库连接等
    process.exit(0);
  });
};
```

### cleanup.js 特点
- 模拟数据库连接池
- 在关闭前调用 `.close()` 方法释放资源
- 展示真实应用中的清理模式

## 预期输出示例
```bash
✅ 服务器正在运行于 http://localhost:3000
💡 发送 SIGINT (Ctrl+C) 或 SIGTERM 以触发优雅关闭

[GET] /slow 请求开始

^C
⏹ 正在关闭服务器...
🔌 模拟清理数据库连接
✅ HTTP服务器已关闭
```

## 常见问题解答

### Q1: 为什么需要优雅关闭？
A: 避免正在处理的请求被强制中断，提升系统稳定性和用户体验，尤其在Kubernetes等容器编排环境中是最佳实践。

### Q2: SIGTERM 和 SIGINT 有什么区别？
A: SIGTERM 是标准终止信号（如 `kill` 命令），建议用于优雅关闭；SIGINT 是终端中断（Ctrl+C），两者都应处理。

### Q3: 如果请求长时间不结束怎么办？
A: 可添加超时机制，例如：
```js
setTimeout(() => {
  console.error('⚠️ 强制退出：请求超时');
  process.exit(1);
}, 10000);
```

## 扩展学习建议
- 学习使用 `cluster` 模块实现多进程优雅关闭
- 结合 PM2 或 Docker 实现生产级部署
- 阅读 Express 官方文档关于错误处理和中间件顺序的内容
- 探索 `AbortController` 在请求取消中的应用