/**
 * 用于集群模式的Express应用
 * 由PM2在cluster模式下启动多个实例
 */

const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// 中间件：记录请求日志
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.url} | PID: ${process.pid}`);
  next();
});

// API路由返回实例信息
app.get('/info', (req, res) => {
  res.json({
    message: 'Running in cluster mode',
    instance: process.env.instance_id || 'unknown',
    processId: process.env.pm_id,
    workerId: process.env.NODE_UNIQUE_ID || 'standalone',
    pid: process.pid,
    uptime: process.uptime()
  });
});

// 根路径
app.get('/', (req, res) => {
  res.send(`Instance ${process.env.pm_id || 0} (PID: ${process.pid}) handling request.`);
});

// 启动服务
app.listen(PORT, () => {
  console.log(`[Cluster Mode] Worker ${process.pid} is listening on port ${PORT}`);
});

// 错误处理
process.on('unhandledRejection', (err) => {
  console.error(`Worker ${process.pid} unhandled rejection:`, err);
  process.exit(1);
});

process.on('uncaughtException', (err) => {
  console.error(`Worker ${process.pid} uncaught exception:`, err);
  process.exit(1);
});