/**
 * variable-scopes.js
 * 变量作用域和声明方式对比
 */

console.log('=== 变量作用域演示 ===');

// 使用var声明（函数作用域）
for (var i = 0; i < 5; i++) {
  // i 在整个函数作用域内都可访问
}
console.log(`i在循环外仍可访问: ${i}`); // 输出: 5

// 使用let声明（块级作用域）
for (let j = 0; j < 5; j++) {
  // j 只在当前块内有效
}
// console.log(j); // 这行会报错：j is not defined
console.log('let声明的j在循环外不可访问');

// const用于声明常量（块级作用域）
const PI = 3.14159;
// PI = 3.14; // 错误：Assignment to constant variable.
console.log(`圆周率: ${PI}`);

// const声明的对象可以修改属性
const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000
};

config.timeout = 10000; // 允许：修改对象属性
console.log('更新后的配置:', config);

// 但不能重新赋值
// config = {}; // 错误

// 变量提升演示
console.log(`提升前的x: ${x}`); // undefined（不是报错）
var x = 10;
console.log(`提升后的x: ${x}`); // 10

// 注意：let/const也存在提升，但不会初始化，形成“暂时性死区”
// console.log(y); // 报错：Cannot access 'y' before initialization
let y = 20;