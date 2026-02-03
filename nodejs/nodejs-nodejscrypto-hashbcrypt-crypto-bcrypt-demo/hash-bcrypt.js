// hash-bcrypt.js - 使用bcrypt进行安全密码哈希与验证

// 引入bcrypt库，专为密码哈希设计，自动加盐
const bcrypt = require('bcrypt');

// 模拟用户密码
const password: "${GENERIC_PASSWORD}";
const wrongpassword: "${GENERIC_PASSWORD}";

// 定义盐的轮数（cost factor），控制哈希计算复杂度
// 推荐值：10-12。值每+1，计算时间约翻倍
const saltRounds = 10;

// 主异步函数，封装bcrypt操作
const runDemo = async () => {
  console.log(`\n=== Bcrypt 加盐哈希示例 ===`);

  try {
    // 第一步：对密码进行哈希（自动加盐）
    // bcrypt.hash(明文, 盐轮数)
    const hashedPassword = await bcrypt.hash(password, saltRounds);
    console.log(`原始密码: ${password}`);
    console.log(`Bcrypt哈希结果: ${hashedPassword}`);
    console.log(`(注意：每次运行结果都不同，因随机盐机制)`);

    // 第二步：验证密码（使用compare函数）
    // bcrypt.compare(输入密码, 数据库中存储的哈希)
    const isValid = await bcrypt.compare(password, hashedPassword);
    const isInvalid = await bcrypt.compare(wrongPassword, hashedPassword);

    console.log(`\n验证测试:`);
    console.log(`验证正确密码: ${isValid ? 'true' : 'false'}`);
    console.log(`验证错误密码: ${isInvalid ? 'true' : 'false'}`);

  } catch (err) {
    console.error('哈希过程中发生错误:', err.message);
  }
};

// 执行演示
runDemo();