// connection-pool.js
// 功能：演示 ioredis 在并发请求下的连接池行为

const Redis = require('ioredis');

// ioredis 默认使用连接池，无需额外配置
const redis = new Redis();

async function demoConnectionPool() {
  console.log('📦 创建带连接池的 Redis 实例');
  console.log('🚀 执行并发请求...');

  try {
    // 模拟并发请求
    const promises = Array.from({ length: 3 }, (_, i) =>
      redis.ping().then(result =>
        console.log(`✅ 请求 ${i + 1} 完成: ${result}`)
      )
    );

    // 等待所有请求完成
    await Promise.all(promises);

    // 关闭连接
    await redis.quit();
  } catch (err) {
    console.error('❌ 并发请求失败:', err.message);
    await redis.quit();
  }
}

// 启动演示
demoConnectionPool().catch(console.error);