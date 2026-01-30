/**
 * Cron表达式定时任务示例
 * 展示更复杂的调度模式
 */
const schedule = require('node-schedule');

// Cron表达式：每分钟的第30秒执行
// 格式：秒 分 时 日 月 星期
const cronJob = schedule.scheduleJob('30 * * * * *', function() {
  console.log(`[Cron调度] 执行时间: ${new Date().toISOString()}`);
});

// 演示运行5次后退出
let count = 0;
schedule.scheduleJob('*/10 * * * * *', function() {
  count++;
  if (count >= 5) {
    console.log('[Cron调度] 演示结束，程序退出');
    process.exit(0);
  }
});