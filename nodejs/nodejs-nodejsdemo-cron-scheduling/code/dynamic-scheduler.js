/**
 * 动态任务管理示例
 * 演示如何创建和取消定时任务
 */
const schedule = require('node-schedule');

// 创建一个每2秒执行的任务
let counter = 0;
const dynamicJob = schedule.scheduleJob('*/2 * * * * *', function() {
  counter++;
  console.log(`[动态调度] 任务执行中... ${counter}`);
  
  // 在第5次执行后取消任务
  if (counter === 5) {
    console.log('[动态调度] 任务已取消');
    dynamicJob.cancel(); // 取消任务
    setTimeout(() => process.exit(0), 1000);
  }
});

console.log('[动态调度] 任务已启动');

// 额外的安全检查：30秒后强制退出（防止意外）
setTimeout(() => {
  if (!dynamicJob.canceled) {
    dynamicJob.cancel();
  }
  console.log('[动态调度] 安全退出');
  process.exit(0);
}, 30000);