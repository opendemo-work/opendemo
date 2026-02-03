// client.js - HTTP客户端请求示例

const http = require('http');

// 要请求的选项配置
const options = {
  hostname: 'localhost',
  port: 3001,
  path: '/',
  method: 'GET',
  headers: {
    'User-Agent': 'Node.js HTTP Client Demo'
  }
};

// 发起HTTP GET请求
const req = http.request(options, (res) => {
  console.log(`状态码: ${res.statusCode}`);

  // 用于拼接响应数据的数组
  let responseData = '';

  // 监听'data'事件，接收数据块
  res.on('data', (chunk) => {
    responseData += chunk;
  });

  // 监听'end'事件，表示数据接收完成
  res.on('end', () => {
    console.log(`响应内容: ${responseData}`);
  });
});

// 处理请求过程中的错误
req.on('error', (err) => {
  console.error('请求失败:', err.message);
});

// 结束请求发送（对于GET请求，通常不需要写入数据）
req.end();