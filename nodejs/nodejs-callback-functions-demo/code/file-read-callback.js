// file-read-callback.js - 使用回调读取文件内容

const fs = require('fs');
const path = require('path');

// 定义要读取的文件路径
const filePath = path.join(__dirname, '..', 'sample.txt');

/**
 * 读取文件内容并处理结果
 * 使用错误优先回调风格
 */
fs.readFile(filePath, 'utf8', (err, data) => {
  if (err) {
    // 如果文件不存在或读取失败，输出错误
    console.error('读取文件时出错：', err.message);
    return;
  }

  // 成功读取文件
  console.log('文件内容读取成功：', data.trim());
});