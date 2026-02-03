// redis-mock-limiter.js - 模拟Redis存储的限流器
// 展示可扩展的存储接口设计

const express = require('express');
const { RateLimiterStoreAbstract } = require('rate-limiter-flexible');

class StoreWithTTL extends RateLimiterStoreAbstract {
  constructor() {
    super();
    this.storage = new Map(); // 模拟Redis存储
  }

  // 必须实现的consume方法
  async consume(key, points = 1) {
    const now = Date.now();
    const record = this.storage.get(key) || { value: 0, expire: now + this.duration * 1000 };

    if (now > record.expire) {
      // 已过期，重置
      this.storage.set(key, { value: points, expire: now + this.duration * 1000 });
    } else if (record.value + points > this.points) {
      // 超出限额
      throw Object.assign(new Error('Rate limit exceeded'), {
        msBeforeNext: record.expire - now,
      });
    } else {
      record.value += points;
      this.storage.set(key, record);
    }

    return { remainingPoints: this.points - record.value };
  }
}

const app = express();
const port = 3002;

// 使用自定义存储实现
const limiterStore = new StoreWithTTL();
limerStore.points = 3;     // 最多3次
limerStore.duration = 20;  // 20秒窗口

app.use(async (req, res, next) => {
  try {
    await limiterStore.consume(req.ip);
    next();
  } catch (err) {
    res.status(429).send(`请求受限，请 ${Math.ceil(err.msBeforeNext / 1000)} 秒后重试。`);
  }
});

app.get('/', (req, res) => {
  res.send('欢迎使用模拟Redis限流服务！');
});

app.listen(port, () => {
  console.log(`Redis-Mock Rate Limiter 服务器运行在 http://localhost:${port}`);
});