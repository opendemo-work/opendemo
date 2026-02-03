// =========================================
// dynamic_typing.js - 动态类型特性演示
// =========================================

console.log('--- 动态类型演示 ---');

// JavaScript 是动态类型语言，变量类型在运行时决定
let dynamicVar = 'Hello'; // 初始为字符串
console.log(`初始为字符串: ${dynamicVar}, 类型: ${typeof dynamicVar}`);

// 重新赋值为数字
dynamicVar = 42;
console.log(`变为数字: ${dynamicVar}, 类型: ${typeof dynamicVar}`);

// 再次赋值为布尔值
dynamicVar = true;
console.log(`变为布尔值: ${dynamicVar}, 类型: ${typeof dynamicVar}`);

// 赋值为对象
dynamicVar = { type: 'object' };
console.log(`变为对象: ${JSON.stringify(dynamicVar)}, 类型: ${typeof dynamicVar}`);

// 总结：变量本身没有类型，值才有类型