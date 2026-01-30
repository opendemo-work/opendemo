/**
 * iterateObject.js
 * 功能：安全遍历对象的自身可枚举属性
 * 使用 for...in 和 hasOwnProperty 过滤继承属性
 */

'use strict';

// 定义一个普通对象
const person = {
  name: 'Alice',
  age: 30
};

// 安全遍历对象的自身属性
// 使用 for...in 会遍历所有可枚举属性，包括原型链上的
// 因此需用 hasOwnProperty 过滤
for (const key in person) {
  if (person.hasOwnProperty(key)) {
    console.log(`键: ${key}, 值: ${person[key]}`);
  }
}

// 补充：也可使用 Object.keys() 获取自身可枚举属性数组
// Object.keys(person).forEach(key => {
//   console.log(`键: ${key}, 值: ${person[key]}`);
// });