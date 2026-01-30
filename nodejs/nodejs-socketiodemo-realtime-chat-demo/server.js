// 导入Express框架，用于创建HTTP服务器
const express = require('express');
// 创建Express应用实例
const app = express();
// 创建HTTP服务器，基于Express应用
const server = require('http').createServer(app);
// 导入Socket.io并绑定到HTTP服务器
const io = require('socket.io')(server);

// 设置静态文件目录，将public文件夹暴露给客户端访问
app.use(express.static('public'));

// 监听客户端连接事件
io.on('connection', (socket) => {
  console.log('用户已连接');

  // 监听客户端发送的'chat message'事件
  socket.on('chat message', (msg) => {
    // 将消息广播给所有连接的客户端（包括发送者）
    io.emit('chat message', msg);
  });

  // 监听客户端断开连接事件
  socket.on('disconnect', () => {
    console.log('用户已断开连接');
  });
});

// 设置服务器监听端口
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`服务器运行在 http://localhost:${PORT}`);
});