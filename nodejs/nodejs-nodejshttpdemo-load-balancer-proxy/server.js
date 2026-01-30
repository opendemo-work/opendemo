// server.js - 负载均衡HTTP代理主服务
const express = require('express');
const httpProxy = require('http-proxy');

// 创建Express应用和代理服务器
const app = express();
const proxy = httpProxy.createProxyServer();

// 定义后端服务器列表（真实场景中可从配置中心获取）
const backends = [
  'http://localhost:3001',
  'http://localhost:3002'
];

// 轮询索引，用于实现简单轮询算法
let currentIndex = 0;

/**
 * 获取下一个后端服务器地址
 * 使用轮询（Round Robin）策略实现负载均衡
 * @returns {string} 后端服务器URL
 */
function getNextBackend() {
  currentIndex = (currentIndex + 1) % backends.length;
  console.log(`请求将转发到: ${backends[currentIndex]}`);
  return backends[currentIndex];
}

// 核心代理中间件
app.use((req, res) => {
  // 动态选择目标后端
  const target = getNextBackend();

  // 通过代理转发请求到选定的后端
  proxy.web(req, res, { target }, (err) => {
    // 错误处理：当前后端不可用时返回502
    console.error(`代理错误: ${err.message}`);
    res.status(502).send('Bad Gateway - 目标服务暂时不可用');
  });
});

// 启动代理服务器
const PORT = 8000;
app.listen(PORT, () => {
  console.log(`负载均衡代理运行在端口 ${PORT}`);
  console.log(`将请求轮询转发到 ${JSON.stringify(backends)}`);
});

// 优雅关闭
process.on('SIGINT', () => {
  console.log('\n正在关闭代理服务器...');
  process.exit(0);
});