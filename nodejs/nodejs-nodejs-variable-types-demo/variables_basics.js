// =========================================
// variables_basics.js - 基本变量类型演示
// =========================================

// 使用 const 声明常量（推荐用于不会重新赋值的变量）
const name = '张三'; // 字符串类型
const age = 25; // 数字类型
const isStudent = true; // 布尔类型
const score = null; // null 表示“无值”，是一种特殊的对象类型（历史原因）
let undefinedValue; // 未赋值的变量，默认为 undefined

// 输出变量值及其类型
console.log('--- 基本变量类型 ---');
console.log(`姓名: ${name}, 类型: ${typeof name}`);
console.log(`年龄: ${age}, 类型: ${typeof age}`);
console.log(`是否学生: ${isStudent}, 类型: ${typeof isStudent}`);
console.log(`分数: ${score}, 类型: ${typeof score}`); // 注意：typeof null === 'object' 是一个已知的bug
console.log(`未定义值: ${undefinedValue}, 类型: ${typeof undefinedValue}`);

// 复杂类型：数组和对象
const hobbies = ['读书', '游泳']; // 数组本质上是对象
const person = { name: '李四', age: 30 }; // 对象

console.log('\n--- 数组与对象 ---');
console.log(`爱好: ${hobbies}, 类型: ${typeof hobbies}`);
console.log(`个人信息: ${JSON.stringify(person)}, 类型: ${typeof person}`);

// 特殊值：函数也是对象类型
const greet = function() { return 'Hello'; };
console.log(`greet 函数类型: ${typeof greet}`);