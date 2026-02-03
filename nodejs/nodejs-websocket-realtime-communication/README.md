# WebSocket实时通信演示

## 简介
本项目展示了如何使用 `ws` 和 `socket.io` 两个流行的 Node.js 库实现 WebSocket 实时双向通信。包含两个独立场景：基础 WebSocket 服务（使用 `ws`）和增强型实时应用（使用 `socket.io`），适合学习实时数据推送、聊天功能等应用场景。

## 学习目标
- 理解 WebSocket 协议的基本原理
- 掌握 `ws` 库创建轻量级 WebSocket 服务器的方法
- 学会使用 `socket.io` 构建支持事件广播、房间管理的实时应用
- 了解前后端 WebSocket 连接与消息交互流程

## 环境要求
- Node.js 版本：v16.x 或更高（推荐 v18+）
- npm 包管理工具（随 Node.js 自动安装）
- 浏览器（用于测试 socket.io 示例）

## 安装依赖的详细步骤

1. 打开终端，进入项目根目录：
```bash
npm init -y
```

2. 安装所需依赖包：
```bash
npm install ws socket.io express
```

3. 确认安装成功：
```bash
npm list ws socket.io express
```
预期输出应显示三个库及其版本信息。

## 文件说明
- `server-ws.js`：基于 `ws` 的简单 WebSocket 服务器，回显客户端消息
- `server-socketio.js`：基于 `socket.io` 的实时通信服务器，支持网页客户端连接和广播
- `public/index.html`：Socket.IO 的前端测试页面

## 逐步实操指南

### 场景一：运行 ws 基础服务器

1. 启动 ws 服务器：
```bash
node server-ws.js
```

2. 预期输出：
```bash
WebSocket 服务器已启动在端口 8080
```

3. 使用命令行测试（新开终端窗口）：
```bash
npx wscat -c ws://localhost:8080
> Hello
< Hello
```
（若未安装 wscat：`npm install -g wscat`）

4. 输入任意消息，服务器将原样返回。

### 场景二：运行 socket.io 实时聊天服务

1. 启动 socket.io 服务器：
```bash
node server-socketio.js
```

2. 预期输出：
```bash
Express 服务器运行在 http://localhost:3000
```

3. 打开浏览器访问：[http://localhost:3000](http://localhost:3000)

4. 多个浏览器标签页打开该地址，输入消息并发送，所有客户端将实时收到广播。

## 代码解析

### server-ws.js 关键点
- 使用 `ws` 创建 WebSocket 服务器，监听 8080 端口
- 每当有客户端连接时，监听其 `message` 事件，并将收到的消息原样回传
- 简洁高效，适用于高性能、低延迟的基础通信场景

### server-socketio.js 关键点
- 使用 Express 提供静态 HTML 页面
- Socket.IO 自动处理连接、断线重连、心跳等复杂逻辑
- 支持通过 `io.emit()` 向所有客户端广播消息
- 前端通过 `<script>` 引入 socket.io 客户端库即可连接

## 预期输出示例

**server-ws.js 输出**：
```
WebSocket 服务器已启动在端口 8080
收到消息: Hello
```

**server-socketio.js 输出**：
```
Express 服务器运行在 http://localhost:3000
用户已连接: socket_id_abc123
广播消息: 用户说：Hi everyone!
```

## 常见问题解答

**Q: 访问 http://localhost:3000 显示无法连接？**
A: 确保 `server-socketio.js` 正在运行，并检查控制台是否有报错。

**Q: wscat 提示 'command not found'？**
A: 需要全局安装：`npm install -g wscat`

**Q: 如何让 socket.io 支持跨域？**
A: 在 `new Server(httpServer, { cors: { origin: '*' } })` 中配置 CORS。

**Q: 可以同时运行两个服务器吗？**
A: 可以，它们监听不同端口（8080 和 3000），互不冲突。

## 扩展学习建议
- 尝试为 socket.io 添加“房间”功能，实现私聊或群组聊天
- 使用 JWT 实现 WebSocket 连接认证
- 结合数据库记录聊天历史
- 探索 WebSocket 与 HTTPS/TLS 加密传输（wss://）
- 对比 ws 与 socket.io 的性能与适用场景