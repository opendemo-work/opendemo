// simple-rate-limiter.js - 简单内存限流器
// 展示最基本的请求频率控制

const express = require('express');
const { RateLimiterMemory } = require('rate-limiter-flexible');

// 创建Express应用
const app = express();
const port = 3000;

// 配置限流器：每秒最多5次请求
const limiter = new RateLimiterMemory({
  points: 5, // 允许的请求数
  duration: 1, // 时间窗口（秒）
});

// 应用全局限流中间件
app.use(async (req, res, next) => {
  try {
    // 消耗一个请求额度
    await limiter.consume(req.ip);
    next();
  } catch (rejRes) {
    // 超出限制时返回429状态码
    res.status(429).send('请求过于频繁，请稍后再试。');
  }
});

// 主路由
app.get('/', async (req, res) => {
  // 查询当前剩余请求数
  const remainingRequests = await limiter.get(req.ip);
  const remainingPoints = remainingRequests?.remainingPoints || 0;

  res.send(`你好！这是你的请求。剩余可用次数：${remainingPoints}`);
});

// 启动服务器
app.listen(port, () => {
  console.log(`Simple Rate Limiter 服务器运行在 http://localhost:${port}`);
});