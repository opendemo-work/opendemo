/**
 * 基础Express应用 - 单进程示例
 * 用于PM2部署演示
 */

const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// 健康检查路由
app.get('/health', (req, res) => {
  res.status(200).send('OK');
});

// 主路由：返回进程信息
app.get('/', (req, res) => {
  res.json({
    message: 'Hello from PM2 demo',
    processId: process.env.pm_id !== undefined ? parseInt(process.env.pm_id) : 'N/A', // PM2分配的进程ID
    pid: process.pid, // 当前进程系统PID
    hostname: require('os').hostname(), // 服务器主机名
    timestamp: new Date().toISOString()
  });
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`App is running on port ${PORT}, PID: ${process.pid}`);
});

// 捕获未处理的异常，防止崩溃
process.on('unhandledRejection', (err) => {
  console.error('Unhandled Rejection:', err);
  process.exit(1);
});

process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err);
  process.exit(1);
});