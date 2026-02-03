/**
 * validation-password.js
 * 功能：验证密码强度（至少8位，含大小写字母和数字）
 * 场景：用户设置密码时的安全性检查
 */

// 使用前瞻断言（lookahead）组合多个条件
// (?=.*[a-z]) : 至少包含一个小写字母
// (?=.*[A-Z]) : 至少包含一个大写字母
// (?=.*\\d)   : 至少包含一个数字
// [A-Za-z\\d@$!%*?&]{8,} : 总长度至少8位，仅允许指定字符
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)[A-Za-z\\d@$!%*?&]{8,}$/;

/**
 * 验证密码强度
 * @param {string} password - 待验证的密码
 * @returns {boolean} 是否符合强度要求
 */
function validatePassword(password) {
  if (typeof password !== 'string') return false;
  return passwordRegex.test(password);
}

// 测试用例
const testPasswords = [
  'Abc12345',
  'Password1',
  'abc123',     // ❌ 太短且无大写
  'password',   // ❌ 无大写无数字
  'ABC12345',   // ❌ 无小写
  'Abcdefgh'    // ❌ 无数字
];

// 执行验证并输出结果
testPasswords.forEach(pwd => {
  if (validatePassword(pwd)) {
    console.log(`✅ '${pwd}' 密码强度合格`);
  } else {
    console.log(`❌ '${pwd}' 密码强度不合格`);
  }
});