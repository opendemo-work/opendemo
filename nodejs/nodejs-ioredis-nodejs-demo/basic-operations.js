// basic-operations.js
// 功能：演示 ioredis 基础字符串操作与缓存过期机制

const Redis = require('ioredis');

// 创建 Redis 客户端实例，默认连接 localhost:6379
const redis = new Redis();

async function demoBasicCache() {
  const key = 'user:john';
  const value = JSON.stringify({ name: 'John Doe', age: 30 });

  try {
    // 设置带过期时间的键值对（EX = seconds）
    await redis.set(key, value, 'EX', 2); // 2秒后自动过期
    console.log('✅ 设置用户 john 成功');

    // 立即读取数据
    const data = await redis.get(key);
    console.log('🔍 获取用户数据:', JSON.parse(data));

    // 等待缓存过期
    console.log('⏳ 2秒后缓存将过期...');
    setTimeout(async () => {
      const expiredData = await redis.get(key);
      console.log('🗑️ 缓存已过期，获取结果:', expiredData); // 应为 null

      // 释放连接资源
      await redis.quit();
    }, 2500);
  } catch (err) {
    console.error('❌ 操作失败:', err.message);
    await redis.quit();
  }
}

// 执行演示
demoBasicCache().catch(console.error);