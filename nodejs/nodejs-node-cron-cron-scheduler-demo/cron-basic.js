// cron-basic.js - 基础定时任务示例
// 每分钟执行一次

// 导入 node-cron 库
const cron = require('node-cron');

// 定义每分钟执行的任务
// Cron 表达式：'*/1 * * * *'
// 含义：每分钟的第0秒执行（即每分钟一次）
cron.schedule('*/1 * * * *', () => {
  const now = new Date();
  console.log(`[定时任务] 当前时间: ${now.toISOString()}`);
}, {
  // 启用任务
  scheduled: true,
  // 设置时区为上海（UTC+8）
  timezone: 'Asia/Shanghai'
});

console.log('✅ 基础定时任务已启动，每分钟打印一次当前时间。');
console.log('📌 按 Ctrl+C 可退出程序。');