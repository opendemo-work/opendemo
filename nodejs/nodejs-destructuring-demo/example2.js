/**
 * example2.js - 数组解构与函数参数应用
 * 演示数组元素提取、变量交换和函数参数解构
 */

// 示例数组
const fruits = ['苹果', '香蕉', '橙子'];

// 基础数组解构
const [first, second] = fruits;
console.log(`【示例2-基础】第一名：${first}，第二名：${second}`);

// 跳过元素
const [ , , third ] = fruits;
console.log(`【示例2-跳过】第三名：${third}`);

// 使用剩余操作符收集其余元素
const [primary, ...others] = fruits;
console.log(`【示例2-剩余】主选：${primary}，其他：${others.join('、')}`);

// 变量交换（无需临时变量）
let a = 1, b = 2;
[b, a] = [a, b];
console.log(`【示例2-交换】交换后 a=${a}, b=${b}`);

// 函数参数解构 - 提升可读性
function displayScores([best, worst]) {
  console.log(`【示例2-函数】最高分：${best}，最低分：${worst}`);
}

displayScores([98, 62]);

// 带默认值的参数解构
function logPerson([name = '未知', age = 0] = []) {
  console.log(`【示例2-默认】人物：${name}，年龄：${age}`);
}

logPerson(['Charlie', 30]);
logPerson(); // 使用默认值