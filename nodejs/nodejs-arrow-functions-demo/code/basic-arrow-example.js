/**
 * 基础箭头函数示例
 * 展示简洁语法和隐式返回
 */

// 单行表达式：自动返回结果
const add = (a, b) => a + b;

// 单参数可省略括号
const greet = name => `Hello, ${name}`;

// 多行函数体需使用花括号和显式 return
const multiply = (x, y) => {
  const result = x * y;
  return result;
};

// 导出函数以便测试
if (require.main === module) {
  console.log('加法结果:', add(3, 5));
  console.log('问候语:', greet('Alice'));
}

module.exports = { add, greet, multiply };