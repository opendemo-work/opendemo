// api-server.js - 模拟REST API服务器

const http = require('http');

// 创建返回JSON数据的服务器
const apiServer = http.createServer((req, res) => {
  // 仅处理根路径的GET请求
  if (req.method === 'GET' && req.url === '/') {
    // 构造响应数据
    const data = {
      message: 'Hello from API!',
      timestamp: Date.now()
    };

    // 设置响应头：返回JSON格式数据
    res.writeHead(200, {
      'Content-Type': 'application/json; charset=utf-8'
    });

    // 将JavaScript对象转为JSON字符串并返回
    res.end(JSON.stringify(data));
  } else {
    // 其他请求返回404
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not Found' }));
  }
});

const PORT = 3001;

// 启动API服务器
apiServer.listen(PORT, () => {
  console.log(`API服务器运行在 http://localhost:${PORT}`);
});

// 错误处理
apiServer.on('error', (err) => {
  console.error('API服务器启动失败:', err.message);
});