/**
 * 文件: spread-function.js
 * 功能: 演示展开运算符在函数参数中的使用
 */

// 示例1：剩余参数 - 收集函数参数为数组
function addAll(...nums) {
  return nums.reduce((sum, num) => sum + num, 0);
}
console.log('求和结果:', addAll(1, 2, 3, 4, 5));

// 示例2：找出最大值（Math.max 需要独立参数）
const values = [3, 1, 8, 4];
console.log('最大值:', Math.max(...values));

// 示例3：展开数组作为函数参数调用
function pairSum(a, b, c, d) {
  console.log(`函数调用拆分: [${a}, ${b}] 和 [${c}, ${d}]`);
}
const part1 = [1, 2];
const part2 = [3, 4];
pairSum(...part1, ...part2);

// 示例4：结合默认值与剩余参数
function greet(greeting, ...names) {
  return `${greeting} ${names.join(', ')}!`;
}
console.log(greet('Hello', 'Tom', 'Jerry', 'Bob'));