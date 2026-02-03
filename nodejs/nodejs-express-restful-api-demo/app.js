// 导入 express 模块
const express = require('express');

// 创建 express 应用实例
const app = express();

// 设置中间件：解析 JSON 格式的请求体
// 这是处理 POST/PUT 请求中 JSON 数据的关键步骤
app.use(express.json());

// 引入用户路由模块
const userRoutes = require('./routes/users');

// 将用户路由挂载到 '/users' 路径下
// 所有在 users.js 中定义的路由都会以 '/users' 为前缀
app.use('/users', userRoutes);

// 定义服务器监听端口
const PORT = process.env.PORT || 3000;

// 启动服务器并监听指定端口
app.listen(PORT, () => {
  console.log(`✅ 服务器正在运行在 http://localhost:${PORT}`);
});

// 导出 app 实例（便于测试或其他模块导入）
module.exports = app;