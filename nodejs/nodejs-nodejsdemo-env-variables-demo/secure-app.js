// secure-app.js - 生产环境安全配置示例
// 展示如何在生产中优先使用系统环境变量

// 仅在非生产环境加载 .env 文件（开发时使用）
if (process.env.NODE_ENV !== 'production') {
  require('dotenv').config();
}

// 安全地读取配置：优先使用系统变量，提供默认值
const PORT = process.env.PORT || 8080;
const NODE_ENV = process.env.NODE_ENV || 'development';

console.log(`🔐 当前环境: ${NODE_ENV}`);
console.log(`服务器将在端口 ${PORT} 启动`);

// 注意：生产部署时，应通过操作系统设置环境变量，而非 .env 文件