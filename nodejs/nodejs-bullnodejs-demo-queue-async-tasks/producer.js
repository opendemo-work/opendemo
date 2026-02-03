// producer.js - Bull 队列任务生产者
// 负责将异步任务添加到队列中

// 导入依赖模块
require('dotenv').config();
const Queue = require('bull');

// 创建一个名为 'emailQueue' 的队列，连接到 Redis
// REDIS_URL 示例：redis://127.0.0.1:6379
const emailQueue = new Queue('emailQueue', process.env.REDIS_URL || 'redis://localhost:6379');

// 异步函数：添加发送邮件任务到队列
async function addSendEmailJob() {
  const to = 'example@example.com';
  const subject = '欢迎使用 Bull 队列！';

  try {
    // 将任务添加到队列，设置最多重试3次
    const job = await emailQueue.add(
      { to, subject },
      {
        attempts: 3, // 自动重试次数
        removeOnComplete: true, // 成功后从列表移除
        removeOnFail: 10000 // 失败后保留一段时间用于调试
      }
    );

    console.log(`✅ 任务已加入队列，任务ID: ${job.id}`);

    // 关闭队列连接（可选）
    // await emailQueue.close();
  } catch (error) {
    console.error('❌ 添加任务失败:', error.message);
  }
}

// 执行任务添加
addSendEmailJob();