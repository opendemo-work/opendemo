/**
 * server.js - 基础优雅关闭示例
 * 
 * 功能：启动一个Express服务器，监听SIGTERM/SIGINT信号
 * 实现服务器关闭前等待当前请求完成
 */

const express = require('express');

const app = express();
const PORT = process.env.PORT || 3000;

// 模拟中间件：记录请求
app.use((req, res, next) => {
  console.log(`[GET] ${req.path} 请求开始`);
  next();
});

// 健康检查路由
app.get('/', (req, res) => {
  res.send('Hello World! 服务正常运行中。');
});

// 模拟耗时请求（5秒）
app.get('/slow', (req, res) => {
  setTimeout(() => {
    res.send('慢请求已完成。');
  }, 5000);
});

// 启动HTTP服务器
const server = app.listen(PORT, () => {
  console.log(`✅ 服务器正在运行于 http://localhost:${PORT}`);
  console.log('💡 发送 SIGINT (Ctrl+C) 或 SIGTERM 以触发优雅关闭');
});

// 优雅关闭逻辑
const shutdown = () => {
  console.log('\n⏹ 正在关闭服务器...');

  // 停止接收新请求
  server.close(() => {
    console.log('✅ HTTP服务器已关闭');
    // 实际项目中可关闭数据库连接、缓存客户端等
    process.exit(0);
  });
};

// 监听系统信号
process.on('SIGTERM', shutdown); // Kubernetes等环境常用
process.on('SIGINT', shutdown);  // Ctrl+C

// 处理未捕获异常（防止崩溃时不触发优雅关闭）
process.on('uncaughtException', (err) => {
  console.error('❌ 未捕获异常:', err);
  shutdown();
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('❌ 未处理的Promise拒绝:', reason);
  shutdown();
});