/**
 * 使用 Bunyan 生成结构化JSON日志
 * 天然支持机器可读的格式，适合集中式日志系统
 */

// 导入bunyan库
const bunyan = require('bunyan');

// 创建Bunyan日志器实例
// 所有字段都会成为最终JSON的一部分
const logger = bunyan.createLogger({
  name: 'UserService',           // 服务名称
  streams: [
    {
      level: 'info',              // 日志级别
      stream: process.stdout        // 输出到控制台
    }
  ],
  serializers: bunyan.stdSerializers, // 使用标准序列化器处理错误、请求等
  src: true                        // 启用源码位置追踪（文件名、行号）
});

// 示例：记录普通业务事件（info级别）
logger.info({
  userId: 1001,
  ip: '192.168.1.10'
}, '用户登录成功');

// 示例：记录错误事件（error级别）
logger.error({
  query: 'SELECT * FROM users',
  error: 'ETIMEDOUT'
}, '数据库查询异常');

// Bunyan默认输出为一行JSON，便于日志系统解析