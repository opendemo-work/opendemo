/**
 * type-checking.js
 * 类型检测和类型转换演示
 */

console.log('=== 类型检测与转换 ===');

// 使用typeof检测基本类型
function logType(value, label) {
  console.log(`${label}: ${value} (类型: ${typeof value})`);
}

logType('hello', '字符串');
logType(42, '数字');
logType(true, '布尔值');
logType(undefined, 'undefined');
logType(null, 'null'); // 注意：typeof null 返回 'object'（历史遗留bug）

// 检测对象和数组
const arr = [1, 2, 3];
const obj = { name: 'test' };

logType(arr, '数组');
logType(obj, '对象');

// 正确检测数组类型
console.log(`arr是数组吗？ ${Array.isArray(arr)}`); // true
console.log(`obj是数组吗？ ${Array.isArray(obj)}`); // false

// 类型转换示例

// 字符串转数字
const strNum = '123';
const num = Number(strNum);
const num2 = parseInt(strNum, 10);

logType(strNum, '字符串数字');
logType(num, '转换后的数字');

// 数字转字符串
const count = 456;
const strCount = String(count);
const strCount2 = count.toString();

logType(count, '数字');
logType(strCount, '转换后的字符串');

// 布尔转换
logType(Boolean(0), 'Boolean(0)');
logType(Boolean(1), 'Boolean(1)');
logType(Boolean(''), 'Boolean("")');
logType(Boolean('hello'), 'Boolean("hello")');
logType(Boolean(null), 'Boolean(null)');

// 真值和假值总结
console.log('\nJavaScript中的假值：');
console.log('- false');
console.log('- 0');
console.log('- "" (空字符串)');
console.log('- null');
console.log('- undefined');
console.log('- NaN');
console.log('其余均为真值');