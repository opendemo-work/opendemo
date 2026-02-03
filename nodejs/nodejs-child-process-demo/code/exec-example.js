/**
 * exec-example.js - 使用child_process.exec执行短时命令
 * 
 * 特点：
 * - 简洁回调风格API
 * - 自动缓冲完整输出
 * - 适合快速获取命令结果
 */

const { exec } = require('child_process');
const os = require('os');

// 构建跨平台命令
const platform = os.platform();
const command = platform === 'win32' 
  ? 'echo %CD% && dir /b' 
  : 'pwd && ls -1';

// 执行命令
exec(command, {
  maxBuffer: 1024 * 1024, // 设置最大缓冲区为1MB
  timeout: 30000,         // 30秒超时
  encoding: 'utf8'        // 输出编码
}, (error, stdout, stderr) => {

  // 清除Node.js事件循环避免延迟退出
  process.exitCode = error ? 1 : 0;

  if (error) {
    console.error('执行错误:', error);
    return;
  }

  if (stderr) {
    console.warn('标准错误输出:', stderr);
    return;
  }

  // 成功执行
  console.log('完整命令输出:\n' + stdout.trim());
  console.log('\n子进程成功执行');
});

// 最佳实践：监控未捕获异常
process.on('uncaughtException', (err) => {
  console.error('未捕获异常:', err);
  process.exit(1);
});

process.on('unhandledRejection', (reason) => {
  console.error('未处理的Promise拒绝:', reason);
  process.exit(1);
});