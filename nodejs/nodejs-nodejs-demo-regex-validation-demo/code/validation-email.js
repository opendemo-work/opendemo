/**
 * validation-email.js
 * 功能：使用正则表达式验证电子邮件格式
 * 场景：用户注册表单中的邮箱输入校验
 */

// 定义邮箱正则表达式
// 解析：
// ^[a-zA-Z0-9._%+-]+ : 开头为一个或多个合法字符（用户名部分）
// @                   : 必须包含 @ 符号
// [a-zA-Z0-9.-]+      : 域名主体（如 gmail、example）
// \\.[a-zA-Z]{2,}      : 点号 + 至少两个字母的顶级域名（如 .com, .org）
// $                   : 字符串结尾
const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

/**
 * 验证邮箱是否合法
 * @param {string} email - 待验证的邮箱字符串
 * @returns {boolean} 是否匹配
 */
function validateEmail(email) {
  if (typeof email !== 'string') return false;
  return emailRegex.test(email);
}

// 测试用例
const testEmails = [
  'test@example.com',
  'user.name+tag@domain.co.uk',
  'invalid-email',
  '@missing.com',
  'no-at-symbol.com'
];

// 执行验证并输出结果
testEmails.forEach(email => {
  if (validateEmail(email)) {
    console.log(`✅ '${email}' 是合法邮箱`);
  } else {
    console.log(`❌ '${email}' 不是合法邮箱`);
  }
});