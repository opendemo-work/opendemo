/**
 * 主应用文件 - 演示中间件链的组织与执行
 */
const express = require('express');
const logger = require('./middleware/logger');
const auth = require('./middleware/auth');

// 创建Express应用实例
const app = express();

// 应用全局中间件：日志记录
app.use(logger);

// 根路由：仅使用日志中间件
app.get('/', (req, res) => {
  // 中间件链已记录请求，直接响应
  res.send('欢迎主页！\n');
});

// 受保护路由：组合多个中间件
// 执行顺序：logger → auth → 路由处理器
app.get('/protected', auth, (req, res) => {
  // 只有通过auth中间件验证才会到达此处
  res.send('受保护资源已访问\n');
});

// 错误处理中间件：捕获前面未处理的错误
// 必须定义为四参数函数
app.use((err, req, res, next) => {
  console.error('发生错误:', err.stack);
  res.status(500).json({ error: '服务器内部错误' });
});

// 监听端口启动服务器
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`服务器运行在 http://localhost:${PORT}`);
});

module.exports = app;