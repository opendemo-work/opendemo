// ip-based-limiter.js - 基于IP的独立限流
// 每个客户端IP独立计算请求次数

const express = require('express');
const { RateLimiterMemory } = require('rate-limiter-flexible');

const app = express();
const port = 3001;

// 为每个IP设置限流：每10秒最多15次请求
const limiter = new RateLimiterMemory({
  points: 15,
  duration: 10, // 10秒内最多15次
});

// 提取客户端IP作为限流键值
const getClientIp = (req) => {
  return req.ip || req.connection.remoteAddress;
};

// 限流中间件
app.use(async (req, res, next) => {
  const clientIp = getClientIp(req);

  try {
    await limiter.consume(clientIp);
    next();
  } catch (rejRes) {
    res.setHeader('Retry-After', Math.round(rejRes.msBeforeNext / 1000));
    res.status(429).send('请求过于频繁，请稍后再试。');
  }
});

app.get('/', (req, res) => {
  res.send(`来自 ${req.ip} 的请求已成功处理！`);
});

app.listen(port, () => {
  console.log(`IP-Based Rate Limiter 服务器运行在 http://localhost:${port}`);
});