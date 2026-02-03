/**
 * system-uptime.js - 显示系统运行时间和上次启动时间
 * 将秒数转换为可读的时间格式
 */

const os = require('os');

// 将秒数转换为 “X天 Y小时 Z分钟” 格式
function formatUptime(seconds) {
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);

  return `${days}天 ${hours}小时 ${minutes}分钟`;
}

const uptimeInSeconds = os.uptime();
const bootTime = new Date(Date.now() - uptimeInSeconds * 1000);

console.log('系统运行时间');
console.log('============');
console.log(`已运行: ${formatUptime(uptimeInSeconds)}`);
console.log(`上次重启时间: ${bootTime.toISOString()}`);