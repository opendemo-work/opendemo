// server.js - 基础HTTP服务器示例

const http = require('http');

// 创建HTTP服务器实例
const server = http.createServer((req, res) => {
  // 根据请求的URL路径返回不同内容
  if (req.url === '/') {
    // 设置响应头：状态码200，内容类型为HTML
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    // 返回主页内容
    res.end('<h1>欢迎访问首页</h1><p><a href="/about">了解我们</a></p>');
  } else if (req.url === '/about') {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end('<h1>关于我们</h1><p>这是一个使用Node.js http模块构建的简单网站。</p>');
  } else {
    // 处理404情况
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('页面未找到');
  }
});

const PORT = 3000;

// 启动服务器并监听指定端口
server.listen(PORT, () => {
  console.log(`服务器运行在 http://localhost:${PORT}`);
});

// 最佳实践：添加错误处理
server.on('error', (err) => {
  console.error('服务器启动失败:', err.message);
});