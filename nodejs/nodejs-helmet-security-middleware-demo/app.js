/**
 * 基础安全中间件示例
 * 使用Helmet默认配置保护Express应用
 */

const express = require('express');
const helmet = require('helmet');

// 创建Express应用实例
const app = express();

// 使用Helmet应用默认安全头
// 自动设置包括：X-Frame-Options, X-XSS-Protection, X-Content-Type-Options等
app.use(helmet());

// 定义根路由
app.get('/', (req, res) => {
  res.send('<h1>🛡️ 安全页面 - Helmet默认防护已启用</h1>');
});

// 启动服务器
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`✅ 基础安全服务器运行在 http://localhost:${PORT}`);
});

// 【关键概念】
// - helmet() 启用9项安全防护，默认开启所有推荐设置
// - 无需配置即可防御常见攻击，适合快速集成