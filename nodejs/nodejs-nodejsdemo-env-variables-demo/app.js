// app.js - 主应用逻辑
// 演示如何在实际应用中使用配置

// 导入配置模块（自动加载 .env）
const config = require('./config');

// 模拟一个简单的HTTP服务器启动逻辑
console.log(`✅ 服务器启动在端口 ${config.port}`);
console.log(`正在连接数据库: ${config.databaseUrl}`);

// 实际项目中可在此处启动 Express/Koa 等框架
// const app = express();
// app.listen(config.port, () => { ... });