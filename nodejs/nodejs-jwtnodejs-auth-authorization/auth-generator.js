// auth-generator.js
// JWT令牌生成器示例
// 演示如何创建安全的JWT令牌

// 引入jsonwebtoken库
const jwt = require('jsonwebtoken');

// 密钥 - 生产环境中应从环境变量读取
// 注意：这是示例密钥，实际使用中必须保密且足够复杂
const SECRET_KEY = process.env.JWT_SECRET || "";

// 模拟用户数据（通常来自数据库查询）
const userPayload = {
  userId: 123,
  name: '张三'
};

// 令牌选项配置
const tokenOptions = {
  expiresIn: '1h'  // 令牌有效期1小时
};

// 生成JWT令牌
// sign(payload, secretOrPrivateKey, options)
const generateToken = () => {
  try {
    const token = jwt.sign(userPayload, SECRET_KEY, tokenOptions);
    console.log('\n生成的JWT令牌:\n' + token);
    return token;
  } catch (error) {
    console.error('令牌生成失败:', error.message);
    throw error;
  }
};

// 导出生成函数以便其他模块使用
module.exports = { generateToken, SECRET_KEY };

// 直接运行时执行生成
if (require.main === module) {
  generateToken();
}