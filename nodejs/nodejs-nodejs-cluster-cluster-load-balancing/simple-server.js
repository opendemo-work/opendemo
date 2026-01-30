/**
 * simple-server.js - 单进程 HTTP 服务器（用于对比）
 * 仅用于演示单进程与集群模式的差异
 */

const http = require('node:http');

http.createServer((req, res) => {
  console.log(`📩 单进程服务器处理请求 (PID: ${process.pid})`);
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello from single-process server!\n');
}).listen(3000, () => {
  console.log(`👉 单进程服务器已启动，监听端口 3000 (PID: ${process.pid})`);
});