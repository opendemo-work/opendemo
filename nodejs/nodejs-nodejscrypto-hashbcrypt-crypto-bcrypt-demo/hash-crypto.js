// hash-crypto.js - 使用Node.js内置crypto模块进行SHA-256哈希

// 引入Node.js内置的crypto模块，用于加密操作
const crypto = require('crypto');

// 模拟用户输入的密码（实际应用中从请求体获取）
const password: "${GENERIC_PASSWORD}";

// 创建SHA-256哈希函数实例
// SHA-256是单向哈希算法，无法逆向还原原始数据
const createHash = (input) => {
  return crypto.createHash('sha256')
    .update(input)           // 输入要哈希的数据
    .digest('hex');          // 以十六进制字符串形式输出
};

// 对密码进行哈希处理
const hashedPassword1 = createHash(password);
const hashedPassword2 = createHash(password); // 再次哈希相同密码

// 输出结果
console.log(`\n=== Crypto SHA-256 哈希示例 ===`);
console.log(`原始密码: ${password}`);
console.log(`SHA-256哈希值: ${hashedPassword1}`);
console.log(`SHA-256哈希值(重复): ${hashedPassword2}`);
console.log(`注意：相同输入始终产生相同输出，存在安全风险！`);

// 警告：此方法不加盐，不适合直接用于密码存储！