// variables-let-const.js
// 演示 let 和 const 的块级作用域特性

console.log('let 支持块级作用域');

// 使用 let 声明块级变量
if (true) {
  let blockVar = true;
  console.log('if 块内的值:', blockVar);
}
// blockVar 在此处无法访问（已超出作用域）

// let 不允许重复声明（在相同作用域）
let i;
for (i = 0; i < 5; i++) {
  // 每次迭代共享同一个 i
}
console.log('循环后仍可访问 i:', i); // 输出: 5

// 使用 const 声明常量（必须初始化）
const PI = 3.14159;
console.log('const 必须初始化且不可重新赋值');

// const 对象不能重新赋值，但属性可以修改
const person = { name: 'Alice' };
person.name = 'Bob'; // 合法：修改属性
console.log('对象属性可以修改:', person.name);

// person = {}; // 错误：不能重新赋值 const 变量