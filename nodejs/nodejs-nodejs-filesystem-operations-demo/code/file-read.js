/**
 * file-read.js - 安全读取文件内容
 * 
 * 演示如何使用fs.readFile()异步读取文件
 * 包含完整的错误处理逻辑
 */

// 引入文件系统模块
const fs = require('fs');

// 异步读取文件内容
// 第三个参数指定字符编码，避免返回Buffer对象
fs.readFile('hello.txt', 'utf8', (err, data) => {
  // 统一错误处理
  if (err) {
    // 根据不同错误类型提供更具体的提示
    if (err.code === 'ENOENT') {
      console.error('文件不存在，请先运行 file-write.js');
    } else {
      console.error('读取文件时出错:', err.message);
    }
    return;
  }

  // 成功读取，输出内容
  console.log('文件内容:', data);
});