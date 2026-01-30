// consumer.js - Bull 队列任务消费者
// 负责从队列中取出并处理任务

// 导入依赖模块
require('dotenv').config();
const Queue = require('bull');

// 创建与生产者相同的队列实例，确保能消费相同队列
const emailQueue = new Queue('emailQueue', process.env.REDIS_URL || 'redis://127.0.0.1:6379');

// 注册任务处理器：处理队列中的每个任务
emailQueue.process(async (job) => {
  const { to, subject } = job.data;

  console.log(`📨 正在处理任务 #${job.id}: 发送邮件给 ${to}`);

  // 模拟异步操作（如调用邮件API）
  await new Promise((resolve, reject) => {
    setTimeout(() => {
      // 模拟随机失败（用于测试重试机制）
      if (Math.random() < 0.3) {
        reject(new Error('邮件服务临时不可用'));
      } else {
        resolve();
      }
    }, 2000); // 模拟2秒处理时间
  });

  console.log(`✅ 任务 #${job.id} 处理完成`);
});

// 监听任务失败事件
emailQueue.on('failed', (job, err) => {
  console.error(`❌ 任务 #${job.id} 失败: ${err.message}`);
});

// 启动成功提示
console.log('✅ 消费者已启动，正在监听 \u0027emailQueue\u0027 队列...');

// 可选：优雅关闭
process.on('SIGINT', async () => {
  await emailQueue.close();
  console.log('\n👋 消费者已关闭');
  process.exit(0);
});