/**
 * 配置管理模块：集中处理环境变量和应用配置
 * 使用 dotenv 实现多环境支持
 */

require('dotenv').config();

// 配置对象，统一导出供其他模块使用
const config = {
  port: process.env.PORT || 3000,
  nodeEnv: process.env.NODE_ENV || 'development',
  // 是否启用详细健康检查日志
  enableHealthCheckLogging: process.env.ENABLE_HEALTH_LOG === 'true'
};

module.exports = config;