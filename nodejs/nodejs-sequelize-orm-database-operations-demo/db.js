// db.js - 数据库连接配置

const { Sequelize } = require('sequelize');

// 创建 Sequelize 实例
// 请根据实际环境修改数据库名、用户名、密码和主机
const sequelize = new Sequelize('sequelize_demo', 'postgres', 'password', {
  host: 'localhost',           // 数据库主机
  dialect: 'postgres',         // 使用 PostgreSQL
  port: 5432,                  // 端口，默认 5432
  logging: false,              // 关闭 SQL 日志输出（生产环境建议开启调试时再打开）
  define: {
    timestamps: true,          // 自动添加 createdAt 和 updatedAt 字段
    underscored: false         // 使用驼峰命名而非下划线
  }
});

// 测试数据库连接
async function connectDB() {
  try {
    await sequelize.authenticate();
    console.log('✅ 数据库连接成功');
  } catch (error) {
    console.error('❌ 数据库连接失败:', error.message);
    process.exit(1); // 连接失败则退出进程
  }
}

module.exports = { sequelize, connectDB };