// =========================================
// variable_scope.js - 变量作用域与提升演示
// =========================================

console.log('--- 变量作用域演示 ---');

// var 声明的变量具有函数作用域和变量提升
console.log('var 提升:', hoistedVar); // undefined，而非报错
var hoistedVar = '我被提升了';

// let 和 const 具有块级作用域，且存在暂时性死区（TDZ）
console.log('块外:', typeof blockLet); // undefined，因为尚未进入块

{
  // 块级作用域
  let blockLet = '我是let变量';
  var functionScopedVar = '我是var';

  console.log('块内:', blockLet);
}

// blockLet 在此无法访问（已超出块范围）
console.log('var变量在函数内:', functionScopedVar); // var 不受块限制

// 演示函数作用域
function testVarScope() {
  if (true) {
    var insideIf = '我在if中';
  }
  console.log('函数内访问if中的var:', insideIf); // 可访问
}

testVarScope();