// cron-advanced.js - 进阶定时任务示例
// 每天上午9点发送提醒

const cron = require('node-cron');

// Cron 表达式：'0 9 * * *'
// 含义：每天 9:00 AM 执行
cron.schedule('0 9 * * *', () => {
  const now = new Date();
  console.log(`[每日提醒] 早上好！今天是新一天的开始！ 🌅 (时间: ${now.toLocaleString('zh-CN')})`);
}, {
  scheduled: true,
  timezone: 'Asia/Shanghai' // 明确设置为中国标准时间
});

console.log('✅ 每日提醒任务已启动，每天上午9点自动触发。');
console.log('📌 当前系统时间:', new Date().toLocaleString('zh-CN'));
console.log('💡 提示：可通过修改系统时间测试任务触发。');