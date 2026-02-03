/**
 * network-info.js - 列出所有网络接口及其IP地址
 * 区分IPv4和IPv6，并跳过内部回环地址（如虚拟机、Docker）
 */

const os = require('os');

console.log('网络接口信息');
console.log('==============');

// 获取网络接口对象
const interfaces = os.networkInterfaces();

// 遍历每个网络接口
Object.keys(interfaces).forEach(interfaceName => {
  interfaces[interfaceName].forEach(info => {
    // 跳过非IPv4/IPv6或内部地址
    if (!info.internal && (info.family === 'IPv4' || info.family === 'IPv6')) {
      console.log(`${interfaceName} (${info.family}): ${info.address}`);
    }
  });
});