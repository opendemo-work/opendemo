/**
 * file-write.js - 异步写入文件示例
 * 
 * 使用Node.js内置fs模块将字符串写入文件
 * 展示基本的异步非阻塞I/O操作
 */

// 引入Node.js核心文件系统模块
const fs = require('fs');

// 要写入的内容
const content = 'Hello, this is a test file created with Node.js fs module.';

// 异步写入文件
// 参数说明:
// - 第1个参数: 文件路径
// - 第2个参数: 要写入的数据
// - 第3个参数: 字符编码（推荐显式指定）
// - 第4个参数: 回调函数，接收错误对象作为唯一参数
fs.writeFile('hello.txt', content, 'utf8', (err) => {
  // 错误优先回调模式: 如果err不为null表示出错
  if (err) {
    console.error('写入文件失败:', err.message);
    return;
  }
  console.log('文件已成功写入: hello.txt');
});