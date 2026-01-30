// variables-var.js
// 演示 var 的变量提升和函数作用域行为

function demonstrateVar() {
  // var 会被提升到函数顶部，但未初始化
  console.log('var 在函数内被提升:', localVar); // 输出: undefined

  var localVar = 'Hello World';

  // var 可以在同一作用域内重复声明（不推荐）
  var localVar = 'Hello Again';
  console.log('var 可以重新声明');

  // var 是函数作用域，因此在整个函数内都可访问
  console.log('var 是函数作用域:', localVar);
}

demonstrateVar();

// 注意：避免在全局使用 var，会污染全局对象
var globalVar = 'I am global';