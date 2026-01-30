// cron-dynamic.js - 动态控制定时任务示例
// 展示如何手动启动和停止任务

const cron = require('node-cron');

// 创建一个每5秒执行一次的任务，但暂不启动
let task = cron.schedule('*/5 * * * * *', () => {
  const now = new Date();
  console.log(`[动态任务] 执行中: ${now.toISOString()}`);
}, {
  scheduled: false, // 手动控制启动
  timezone: 'Asia/Shanghai'
});

// 启动任务
task.start();
console.log('[动态任务] 已启动，每5秒执行一次...');

// 监听用户输入以停止任务
console.log('\n📌 按 Enter 键停止任务...');
process.stdin.setEncoding('utf8');
process.stdin.once('data', () => {
  task.stop(); // 停止任务
  console.log('\n[动态任务] 已成功停止。');
  process.exit(0); // 安全退出
});