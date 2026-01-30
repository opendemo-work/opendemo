// example-scopes.js
// 综合示例：展示不同作用域下变量的行为

// 全局变量
let globalVar = 'I am global';

function scopeExample() {
  console.log('全局变量:', globalVar);

  // 函数作用域变量
  let funcVar = 'I am local to function';

  if (true) {
    // 块级作用域变量（与外部同名，但独立）
    let globalVar = 'I am shadowing the global';
    console.log('块级作用域中 let 被屏蔽:', globalVar);

    // 使用 let 的 for 循环是安全的
    for (let i = 0; i < 3; i++) {
      console.log('for 循环使用 let 是安全的: i =', i);
    }
    // i 在此处仍然不可访问
  }

  // tempVar 仅在 if 块中定义
  // console.log(tempVar); // 错误！tempVar is not defined

  console.log('函数内访问全局变量:', globalVar);
}

scopeExample();

// 验证全局变量未被修改
console.log('全局变量:', globalVar);