// server-socketio.js - 使用 socket.io 构建功能丰富的实时应用
// 支持自动重连、广播、事件系统，适合聊天室、通知系统等

const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: '*', // 允许所有来源，生产环境应限制
    methods: ['GET', 'POST']
  }
});

// 提供静态文件（HTML 页面）
app.use(express.static('public'));

// 监听 HTTP 请求，启动服务器
server.listen(3000, () => {
  console.log('Express 服务器运行在 http://localhost:3000');
});

// 处理 Socket.IO 连接
io.on('connection', (socket) => {
  console.log('用户已连接:', socket.id);

  // 监听客户端发送的 chatMessage 事件
  socket.on('chatMessage', (msg) => {
    console.log('广播消息:', msg);
    // 向所有连接的客户端广播该消息
    io.emit('chatMessage', msg);
  });

  // 用户断开连接时触发
  socket.on('disconnect', () => {
    console.log('用户断开连接:', socket.id);
  });
});