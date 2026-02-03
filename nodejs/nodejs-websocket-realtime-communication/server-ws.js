// server-ws.js - 使用 ws 库搭建基础 WebSocket 服务器
// 适合轻量级实时通信场景，如游戏状态同步、传感器数据推送等

const WebSocket = require('ws');

// 创建 WebSocket 服务器，监听 8080 端口
const wss = new WebSocket.Server({ port: 8080 });

console.log('WebSocket 服务器已启动在端口 8080');

// 监听客户端连接事件
wss.on('connection', (ws) => {
  console.log('新客户端已连接');

  // 监听来自客户端的消息
  ws.on('message', (data) => {
    const message = data.toString();
    console.log('收到消息:', message);

    // 将消息原样广播给所有连接的客户端
    wss.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(message);
      }
    });
  });

  // 客户端断开连接时触发
  ws.on('close', () => {
    console.log('客户端已断开连接');
  });
});