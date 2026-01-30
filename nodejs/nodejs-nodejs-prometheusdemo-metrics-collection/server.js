// server.js - 主服务入口文件
const express = require('express');
const client = require('prom-client');

// 导入自定义指标模块
const { httpRequestCounter, responseTimeHistogram } = require('./metrics');

// 创建Express应用
const app = express();
const PORT = 3000;

// 根路由 - 模拟业务接口
app.get('/', (req, res) => {
  // 记录请求计数
  httpRequestCounter.inc({
    method: req.method,
    route: req.route?.path || req.path,
    status_code: '200'
  });

  // 模拟响应时间观测
  const end = responseTimeHistogram.startTimer();
  setTimeout(() => {
    end({ route: '/' }); // 结束计时并记录
    res.send('Hello World! Prometheus metrics are available at /metrics');
  }, Math.random() * 100); // 随机延迟模拟真实响应
});

// 暴露Prometheus指标的专用端点
app.get('/metrics', async (req, res) => {
  try {
    // 获取所有已注册的指标
    const metrics = await client.register.metrics();
    
    // 设置正确的Content-Type
    res.set('Content-Type', client.register.contentType);
    
    // 返回指标数据
    res.end(metrics);
  } catch (err) {
    console.error('Error collecting metrics:', err);
    res.status(500).end('Internal Server Error');
  }
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
  console.log('访问 http://localhost:3000/metrics 查看Prometheus指标');
});

// 可选：每分钟打印一次总请求数用于调试
setInterval(() => {
  console.log('Metrics endpoint ready - use /metrics to scrape');
}, 60000);

module.exports = app;