# Socket.io实时聊天室Demo

## 简介
本项目是一个简单的实时多人聊天室应用，使用Node.js和Socket.io实现客户端与服务器之间的双向实时通信。用户可以在浏览器中打开多个窗口模拟不同用户，发送消息并即时看到他人消息。

## 学习目标
- 理解Socket.io的基本工作原理
- 掌握WebSocket在Node.js中的使用方式
- 学会搭建基础的实时通信应用
- 熟悉Express与Socket.io的集成

## 环境要求
- Node.js v16 或更高版本（推荐v18+）
- npm（随Node.js自动安装）
- 浏览器（Chrome/Firefox/Safari/Edge）

> 注意：本项目为Node.js项目，无需Python或Java环境。

## 安装依赖的详细步骤

1. 打开终端（命令行工具）
2. 进入项目目录：
   ```bash
   cd socket-chat-demo
   ```
3. 安装所需依赖包：
   ```bash
   npm install
   ```
   > 预期输出：`added X packages in Ys`，无报错即成功。

## 文件说明
- `server.js`：核心服务器文件，使用Express提供HTTP服务，Socket.io处理实时通信
- `public/index.html`：前端页面，包含聊天界面和Socket.io客户端脚本
- `package.json`：项目依赖和启动脚本声明

## 逐步实操指南

### 步骤1：创建项目结构
```bash
mkdir socket-chat-demo
cd socket-chat-demo
npm init -y
npm install express socket.io
mkdir public
```

### 步骤2：启动服务器
```bash
node server.js
```
预期输出：
```
服务器运行在 http://localhost:3000
```

### 步骤3：打开浏览器访问
在浏览器中访问：
```
http://localhost:3000
```

### 步骤4：测试聊天功能
- 打开两个浏览器标签页访问同一地址
- 在一个页面输入消息并发送
- 观察另一个页面是否实时收到消息

## 代码解析

### server.js 关键代码段
```js
io.on('connection', (socket) => {
  console.log('用户已连接');

  // 监听客户端发来的聊天消息
  socket.on('chat message', (msg) => {
    io.emit('chat message', msg); // 广播给所有连接的客户端
  });

  // 用户断开连接
  socket.on('disconnect', () => {
    console.log('用户已断开连接');
  });
});
```
- `io.on('connection')`：监听新客户端连接
- `socket.on('chat message')`：接收客户端发送的消息
- `io.emit()`：将消息广播给所有客户端（包括发送者）

## 预期输出示例
### 终端输出
```
服务器运行在 http://localhost:3000
用户已连接
用户已断开连接
```

### 浏览器行为
- 页面显示输入框和发送按钮
- 输入文字点击发送后，消息出现在聊天区域
- 其他客户端也同步显示该消息

## 常见问题解答

**Q1: 访问 http://localhost:3000 显示无法连接？**
A: 检查是否已运行 `node server.js`，并确认端口3000未被占用。

**Q2: 消息不能实时同步？**
A: 确保浏览器控制台无报错，且Socket.io客户端正确加载（检查网络请求是否有/socket.io路径）。

**Q3: 如何部署到公网？**
A: 可使用Ngrok进行本地穿透测试，或部署到VPS/云平台（如Heroku、Vercel、阿里云等）。

## 扩展学习建议
- 添加用户名登录功能
- 实现私聊消息（一对一通信）
- 使用Redis实现多实例间消息同步
- 增加消息持久化（保存到数据库）
- 添加表情符号和图片发送支持
- 实现在线用户列表显示