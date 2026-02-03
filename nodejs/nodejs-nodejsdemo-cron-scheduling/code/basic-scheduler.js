/**
 * 基础定时任务调度示例
 * 使用固定间隔执行任务
 */
const schedule = require('node-schedule');

// 每5秒执行一次的任务
const job = schedule.scheduleJob('*/5 * * * * *', function() {
  console.log(`[基础调度] 当前时间: ${new Date().toISOString()}`);
});

// 1分钟后自动停止所有任务（演示用）
setTimeout(() => {
  console.log('[基础调度] 演示结束，程序退出');
  process.exit(0);
}, 60000);