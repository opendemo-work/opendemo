/**
 * dir-create.js - 目录创建与日志文件写入
 * 
 * 演示如何创建目录并写入子文件
 * 使用递归模式安全创建多级目录
 */

const fs = require('fs');

// 创建名为logs的目录（支持递归创建）
fs.mkdir('logs', { recursive: true }, (err) => {
  if (err) {
    console.error('创建目录失败:', err.message);
    return;
  }

  console.log("目录 'logs' 已创建或已存在");

  // 在logs目录下写入日志文件
  const logContent = `[INFO] Application started at ${new Date().toISOString()}\n`;
  
  fs.writeFile('logs/app.log', logContent, 'utf8', (err) => {
    if (err) {
      console.error('写入日志文件失败:', err.message);
      return;
    }
    console.log('日志文件已写入: logs/app.log');
  });
});