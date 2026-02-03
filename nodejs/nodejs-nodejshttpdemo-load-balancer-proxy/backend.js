// backend.js - 模拟后端服务实例
const express = require('express');

/**
 * 创建并启动后端服务
 * @param {number} port - 服务监听端口
 */
function startBackend(port) {
  const app = express();

  // 返回简单的文本响应，包含当前端口号
  app.get('*', (req, res) => {
    res.send(`响应来自后端端口 ${port}\n`);
  });

  // 启动HTTP服务器
  app.listen(port, () => {
    console.log(`后端服务器运行在端口 ${port}`);
  });

  // 优雅关闭
  process.on('SIGINT', () => {
    console.log(`\n正在关闭后端服务 ${port}...`);
    process.exit(0);
  });
}

// 从命令行参数读取端口号，默认3001
const port = parseInt(process.argv[2], 10) || 3001;
if (isNaN(port)) {
  console.error('错误：端口号必须是数字');
  process.exit(1);
}

startBackend(port);