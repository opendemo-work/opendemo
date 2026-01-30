// index.js - 主程序入口，演示 Sequelize CRUD 操作

const { sequelize } = require('./db');
const User = require('./userModel');
const { connectDB } = require('./db');

// 主函数：执行完整的 CRUD 示例
async function main() {
  try {
    // 1. 连接数据库
    await connectDB();

    // 2. 同步模型到数据库（创建表）
    await sequelize.sync({ force: true }); // 每次运行重置表，仅用于演示
    console.log('🔄 数据表已同步');

    // 3. 创建用户（Create）
    const newUser = await User.create({
      name: 'Alice',
      email: 'alice@example.com'
    });
    console.log('✅ 用户已创建:', newUser.toJSON());

    // 4. 查询用户（Read）
    const foundUser = await User.findByPk(newUser.id);
    if (foundUser) {
      console.log('🔍 查询到的用户:', foundUser.name);
    }

    // 5. 更新用户（Update）
    await foundUser.update({
      email: 'alice.new@example.com'
    });
    console.log('✅ 用户邮箱已更新');

    // 6. 删除用户（Delete）
    await foundUser.destroy();
    console.log('✅ 用户已删除');

    console.log('✨ 所有操作完成');
  } catch (error) {
    console.error('🚨 操作出错:', error.message);
  } finally {
    // 关闭数据库连接
    await sequelize.close();
  }
}

// 启动主函数
main();