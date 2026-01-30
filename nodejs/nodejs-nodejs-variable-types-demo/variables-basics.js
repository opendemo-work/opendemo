/**
 * variables-basics.js
 * 基本变量类型演示
 */

// 字符串类型 - 表示文本数据
const name = '张三';
const greeting = `你好，${name}！`; // 模板字符串

// 数字类型 - 包括整数和浮点数
const age = 25;
const price = 99.99;

// 布尔类型 - true 或 false
const isStudent = true;
const isEmployed = false;

// null - 表示“无”或“空值”
const car = null;

// undefined - 变量已声明但未赋值
let job;

// 对象类型 - 复合数据结构
const person = {
  name: '李四',
  age: 30,
  hobbies: ['读书', '游泳']
};

// 数组类型 - 有序的数据集合
const colors = ['红色', '绿色', '蓝色'];

// 输出所有变量的值和类型
console.log('=== 基本变量类型 ===');
console.log(`姓名: ${name} (类型: ${typeof name})`);
console.log(`年龄: ${age} (类型: ${typeof age})`);
console.log(`是否学生: ${isStudent} (类型: ${typeof isStudent})`);
console.log(`职业: ${job} (类型: ${typeof job})`);
console.log(`汽车: ${car} (类型: ${typeof car})`);
console.log(`问候语: ${greeting}`);
console.log(`人物对象:`, person);
console.log(`颜色数组:`, colors);