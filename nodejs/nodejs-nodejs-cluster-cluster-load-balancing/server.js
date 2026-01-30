/**
 * server.js - 使用 Node.js Cluster 模块实现多进程负载均衡
 * 主进程负责管理工作进程，工作进程处理实际 HTTP 请求
 */

const cluster = require('node:cluster');
const http = require('node:http');
const os = require('node:os');

// 获取 CPU 核心数量，决定创建工作进程的数量
const numCPUs = os.cpus().length;

if (cluster.isMaster) {
  // 主进程逻辑：只运行一次
  console.log(`✅ 主进程 PID: ${process.pid} 已启动`);

  // 创建与 CPU 核心数相等的工作进程
  for (let i = 0; i < numCPUs; i++) {
    const worker = cluster.fork();
    console.log(`🚀 创建工作进程 #${i + 1} (PID: ${worker.process.pid})`);
  }

  // 监听工作进程退出事件，实现故障恢复
  cluster.on('exit', (worker, code, signal) => {
    console.warn(`⚠️ 工作进程 ${worker.process.pid} 已退出，代码: ${code}, 信号: ${signal}`);
    console.log('🔄 正在启动新的工作进程...');
    cluster.fork(); // 自动重启新进程
  });
} else {
  // 工作进程逻辑：每个进程运行一个 HTTP 服务器
  // 所有工作进程共享同一个端口，由操作系统进行负载均衡

  http.createServer((req, res) => {
    // 模拟一些 CPU 密集型任务（避免过快响应）
    const startTime = Date.now();
    while (Date.now() - startTime < 10); // 轻微延迟，便于观察负载分布

    // 记录请求处理信息
    console.log(`📩 请求由工作进程 PID: ${process.pid} 处理`);

    // 返回响应
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      message: 'Hello from Node.js Cluster!',
      workerPid: process.pid,
      timestamp: new Date().toISOString()
    }));
  }).listen(3000, () => {
    console.log(`👂 工作进程 ${process.pid} 正在运行，监听端口 3000`);
  });

  // 捕获未处理的异常，防止进程意外退出
  process.on('uncaughtException', (err) => {
    console.error(`❌ 工作进程 ${process.pid} 发生未捕获异常:`, err);
    process.exit(1); // 触发 cluster 的 exit 事件，由主进程重启
  });
}