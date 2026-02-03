/**
 * 主服务文件：实现 Liveness 和 Readiness 健康检查
 * 符合微服务架构标准，适用于容器化部署
 */

// 导入核心模块
const express = require('express');
const dotenv = require('dotenv');

// 加载环境变量
dotenv.config();

// 创建 Express 应用实例
const app = express();

// 使用 JSON 中间件解析请求体
app.use(express.json());

// 模拟服务就绪状态（默认为 true）
let isReady = true;

// --- 健康检查路由 ---

/**
 * Liveness 检查：仅表示应用进程正在运行
 * 即使依赖失败也应返回 200，除非进程崩溃
 */
app.get('/health/liveness', (req, res) => {
  res.status(200).json({ status: 'up' });
});

/**
 * Readiness 检查：判断服务是否准备好接收请求
 * 可用于检测数据库连接、缓存、外部 API 等依赖
 */
app.get('/health/readiness', (req, res) => {
  if (isReady) {
    res.status(200).json({ status: 'ready' });
  } else {
    // 当服务未就绪时返回 503，负载均衡器将不再转发请求
    res.status(503).json({ status: 'not ready', reason: 'manual override' });
  }
});

// 调试接口：手动触发就绪失败（用于测试）
app.post('/debug/fail-readiness', (req, res) => {
  isReady = false;
  res.status(200).json({ message: 'Readiness 设置为失败' });
});

// 恢复就绪状态
app.post('/debug/restore-readiness', (req, res) => {
  isReady = true;
  res.status(200).json({ message: 'Readiness 已恢复' });
});

// 获取当前就绪状态（调试用）
app.get('/debug/status', (req, res) => {
  res.status(200).json({ isReady });
});

// 启动服务器
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✅ 应用正在监听端口 ${PORT}...`);
  console.log(`➡️  Liveness: http://localhost:${PORT}/health/liveness`);
  console.log(`➡️  Readiness: http://localhost:${PORT}/health/readiness`);
});

// 导出 app 以便测试
module.exports = app;