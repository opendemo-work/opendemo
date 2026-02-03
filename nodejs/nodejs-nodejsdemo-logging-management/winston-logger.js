/**
 * 使用 Winston 实现结构化日志记录
 * 支持控制台和文件双输出
 */

// 导入winston日志库
const winston = require('winston');
// 导入Node.js内置文件系统模块
const fs = require('fs');
// 导入路径处理模块
const path = require('path');

// 确保日志目录存在
const logDir = './logs';
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir);
}

// 创建winston日志器实例
const logger = winston.createLogger({
  // 设置日志级别，低于此级别的不会输出
  level: 'info',
  // 自定义日志格式：时间 + 级别 + 消息 + 元数据
  format: winston.format.printf(({ level, message, timestamp, ...metadata }) => {
    const time = new Date().toISOString();
    // 构建基础日志字符串
    let msg = `[${level.toUpperCase()}] ${message}`;
    // 如果有额外元数据，则附加显示
    if (Object.keys(metadata).length > 0) {
      msg += ' - ' + Object.entries(metadata)
        .map(([key, val]) => `${key}: ${val}`)
        .join(', ');
    }
    return `${msg}`;
  }),
  // 配置日志传输目标：控制台 + 文件
  transports: [
    // 输出到控制台
    new winston.transports.Console(),
    // 输出到文件
    new winston.transports.File({ filename: path.join(logDir, 'app.log') })
  ]
});

// 示例：记录应用启动信息（带元数据）
logger.info('应用启动成功', { userId: 123, module: 'auth' });

// 示例：记录错误信息（带结构化数据）
logger.error('数据库连接失败', { error: 'Connection timeout', retries: 3 });

// 提示日志已保存
console.log('日志已保存至 ./logs/app.log');