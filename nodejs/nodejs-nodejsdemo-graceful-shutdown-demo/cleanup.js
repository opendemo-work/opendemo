/**
 * cleanup.js - 带资源清理的优雅关闭示例
 * 
 * 场景：模拟数据库连接池、日志写入器等需显式关闭的资源
 */

const express = require('express');

const app = express();
const PORT = process.env.PORT || 3001;

// 模拟数据库连接池（实际可能是 mongoose、pg等）
const db = {
  connected: true,
  close() {
    return new Promise((resolve) => {
      console.log('🔌 模拟清理数据库连接...');
      setTimeout(() => {
        this.connected = false;
        console.log('✅ 数据库连接已关闭');
        resolve();
      }, 800);
    });
  }
};

// 模拟日志缓冲区（需刷新）
const logger = {
  buffer: ['系统启动日志'],
  flush() {
    return new Promise((resolve) => {
      if (this.buffer.length > 0) {
        console.log(`📝 正在刷新 ${this.buffer.length} 条日志...`);
        setTimeout(() => {
          console.log('✅ 日志已全部写入磁盘');
          this.buffer = [];
          resolve();
        }, 500);
      } else {
        resolve();
      }
    });
  }
};

app.get('/', (req, res) => {
  logger.buffer.push(`访问根路径 - ${new Date().toISOString()}`);
  res.send('欢迎使用带清理功能的服务！');
});

const server = app.listen(PORT, () => {
  console.log(`✅ 清理示例服务器运行于 http://localhost:${PORT}`);
});

const shutdown = async () => {
  console.log('\n⏹ 开始执行优雅关闭流程...');

  // 停止接收新请求
  server.close(async () => {
    console.log('✅ HTTP服务器已关闭');

    // 并行清理资源
    await Promise.all([db.close(), logger.flush()]);

    console.log('🟢 所有资源已释放，进程退出。');
    process.exit(0);
  });
};

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);

// 错误处理
process.on('uncaughtException', (err) => {
  console.error('❌ 严重错误，立即关闭:', err);
  process.exit(1);
});