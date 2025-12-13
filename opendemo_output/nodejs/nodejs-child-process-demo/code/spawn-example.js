/**
 * spawn-example.js - 使用child_process.spawn执行系统命令
 * 
 * 特点：
 * - 实时流式输出（适用于大文件或长时间任务）
 * - 跨平台兼容（自动检测OS选择命令）
 * - 标准错误独立捕获
 */

const { spawn } = require('child_process');
const path = require('path');
const os = require('os');

// 根据操作系统选择合适的列出目录命令
const command = os.platform() === 'win32' ? 'dir' : 'ls';
const args = os.platform() === 'win32' ? [] : ['-la']; // Windows dir默认详细

// 创建子进程
const child = spawn(command, args, {
  cwd: process.cwd(), // 当前工作目录
  env: { ...process.env }, // 继承环境变量
  shell: true // 启用shell以支持复杂命令
});

// 监听标准输出流
child.stdout.on('data', (data) => {
  // 将Buffer转为字符串并按行分割处理
  const lines = data.toString().split(/\r?\n/).filter(line => line);
  lines.forEach(line => {
    console.log(`[stdout] ${line}`);
  });
});

// 监听标准错误流
child.stderr.on('data', (data) => {
  const lines = data.toString().split(/\r?\n/).filter(line => line);
  lines.forEach(line => {
    console.error(`[stderr] ${line}`);
  });
});

// 监听子进程关闭事件
child.on('close', (code) => {
  console.log(`子进程退出码: ${code}`);
  if (code !== 0) {
    console.error('命令执行失败，请检查系统环境');
  }
});

// 错误处理（例如命令未找到）
child.on('error', (err) => {
  console.error('启动子进程失败:', err.message);
});

// 最佳实践：设置超时防止挂起
const timeout = setTimeout(() => {
  console.warn('命令执行超时，正在终止...');
  child.kill(); // 安全终止子进程
}, 30000); // 30秒超时

// 清理超时定时器
child.on('close', () => clearTimeout(timeout));