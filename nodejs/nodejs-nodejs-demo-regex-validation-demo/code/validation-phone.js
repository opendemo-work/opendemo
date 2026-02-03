/**
 * validation-phone.js
 * 功能：验证中国大陆手机号码
 * 场景：手机登录或短信验证码功能中的号码校验
 */

// 中国手机号正则：
// ^1                  : 以1开头
// [3-9]               : 第二位为3-9（目前号段范围）
// [0-9]{9}            : 后续9位任意数字
// $                   : 字符串结束
const phoneRegex = /^1[3-9][0-9]{9}$/;

/**
 * 验证手机号是否为中国大陆有效号码
 * @param {string|number} phone - 手机号（支持字符串或数字）
 * @returns {boolean} 是否匹配
 */
function validatePhone(phone) {
  // 统一转换为字符串并去除空格
  const phoneStr = String(phone).trim();
  // 检查是否全为数字且长度正确
  return phoneRegex.test(phoneStr);
}

// 测试用例
const testPhones = [
  '13812345678',
  '15987654321',
  '12345678901', // ❌ 开头非13-19
  '1381234567',  // ❌ 位数不足
  '138123456789' // ❌ 位数过多
];

// 执行验证并输出结果
testPhones.forEach(phone => {
  if (validatePhone(phone)) {
    console.log(`✅ '${phone}' 是合法手机号`);
  } else {
    console.log(`❌ '${phone}' 不是合法手机号`);
  }
});