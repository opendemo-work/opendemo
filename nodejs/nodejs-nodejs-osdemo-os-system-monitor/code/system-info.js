/**
 * system-info.js - 获取系统基本信息
 * 包括主机名、操作系统、CPU、内存等
 */

const os = require('os');

// 格式化字节为GB，保留两位小数
function bytesToGB(bytes) {
  return (bytes / (1024 ** 3)).toFixed(2);
}

// 获取系统基本信息
console.log('系统信息监控 - 基本信息');
console.log('========================');

console.log(`主机名: ${os.hostname()}`);
console.log(`操作系统: ${os.type()}`);
console.log(`系统架构: ${os.arch()}`);
console.log(`平台: ${os.platform()}`);

const cpus = os.cpus();
if (cpus.length > 0) {
  console.log(`CPU型号: ${cpus[0].model}`);
  console.log(`CPU核心数: ${cpus.length}`);
}

const totalMemory = os.totalmem();
const freeMemory = os.freemem();
const usedMemory = totalMemory - freeMemory;
const memoryUsagePercent = ((usedMemory / totalMemory) * 100).toFixed(2);

console.log(`总内存: ${bytesToGB(totalMemory)} GB`);
console.log(`可用内存: ${bytesToGB(freeMemory)} GB (${memoryUsagePercent}%)`);