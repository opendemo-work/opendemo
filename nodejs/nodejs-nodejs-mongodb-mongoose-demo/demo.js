// demo.js
// 演示 Mongoose 基本 CRUD 操作

const mongoose = require('mongoose');
const User = require('./models/User');

// MongoDB 连接字符串（本地默认端口）
const DB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/test';

async function runDemo() {
  try {
    // 1. 连接数据库
    await mongoose.connect(DB_URI);
    console.log('✅ 已成功连接到 MongoDB');

    // 2. 创建新用户
    const newUser = await User.create({ name: 'Alice', age: 25 });
    console.log('📝 新用户已创建：', newUser);

    // 3. 查询用户
    const foundUser = await User.findOne({ name: 'Alice' });
    console.log('🔍 查询到的用户：', foundUser);

    // 4. 更新用户
    const updatedUser = await User.findOneAndUpdate(
      { name: 'Alice' },
      { age: 26 },
      { new: true }  // 返回更新后的文档
    );
    console.log('✏️ 用户已更新：', updatedUser);

    // 5. 删除用户
    await User.deleteOne({ name: 'Alice' });
    console.log('🗑️ 用户已删除');

  } catch (error) {
    console.error('❌ 操作失败：', error.message);
  } finally {
    // 6. 断开数据库连接
    await mongoose.connection.close();
    console.log('🔌 已断开数据库连接');
  }
}

// 执行演示
runDemo();