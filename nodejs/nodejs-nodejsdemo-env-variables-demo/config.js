// config.js - 环境配置加载模块
// 使用 dotenv 安全加载本地环境变量

// 导入 dotenv 库，用于从 .env 文件加载环境变量
require('dotenv').config();

// 定义一个函数来验证并获取配置
function loadConfig() {
  // 从 process.env 获取变量（由 dotenv 注入）
  const { PORT, DATABASE_URL, API_KEY } = process.env;

  // 验证必要配置是否存在
  if (!PORT) throw new Error('配置错误：缺少 PORT 环境变量');
  if (!DATABASE_URL) throw new Error('配置错误：缺少 DATABASE_URL 环境变量');
  if (!API_KEY) console.warn('⚠️  警告：API_KEY 未设置，某些功能可能受限');

  // 返回格式化后的配置对象
  return {
    port: parseInt(PORT, 10),
    databaseUrl: DATABASE_URL,
    apiKey: API_KEY,
    isSecure: process.env.NODE_ENV === 'production'
  };
}

// 导出加载的配置
const config = loadConfig();
console.log('配置已加载：');
console.log(`端口: ${config.port}`);
console.log(`数据库: ${config.databaseUrl}`);
console.log(`API密钥: ${config.apiKey ? '***' : '(未设置)'}`);

module.exports = config;