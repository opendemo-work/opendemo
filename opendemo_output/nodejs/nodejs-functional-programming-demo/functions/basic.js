// basic.js - 基础函数定义与调用示例

// 函数声明：传统方式定义函数
function greet(name) {
  return `Hello, ${name}`;
}

// 函数表达式：将函数赋值给变量
const add = function(a, b) {
  return a + b;
};

// 箭头函数：ES6简洁语法，适合单行逻辑
const multiply = (a, b) => a * b;

// 导出函数以便其他模块使用
module.exports = { greet, add, multiply };

// 主程序执行逻辑
console.log(greet('张三'));
console.log('5 + 3 =', add(5, 3));