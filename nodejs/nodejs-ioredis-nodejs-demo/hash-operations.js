// hash-operations.js
// 功能：演示 Redis 哈希（Hash）类型的操作，适合存储对象字段

const Redis = require('ioredis');

// 创建 Redis 客户端
const redis = new Redis();

async function demoHashOperations() {
  const userKey = 'user:alice';

  try {
    // 使用哈希结构存储用户多个字段
    await redis.hset(userKey, 'name', 'Alice');
    await redis.hset(userKey, 'email', 'alice@example.com');
    console.log('🧩 使用 HSET 写入用户信息');

    // 获取所有字段
    const userData = await redis.hgetall(userKey);
    console.log('🔍 使用 HGETALL 获取完整用户信息:', userData);

    // 单独获取某个字段
    const email = await redis.hget(userKey, 'email');
    console.log('📧 单独获取邮箱:', email);

    // 演示完成后关闭连接
    await redis.quit();
  } catch (err) {
    console.error('❌ 哈希操作失败:', err.message);
    await redis.quit();
  }
}

// 运行演示
demoHashOperations().catch(console.error);