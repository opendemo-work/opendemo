/**
 * 示例1：使用Symbol作为唯一属性键
 * 
 * 演示如何利用Symbol的唯一性来添加不会冲突的对象属性
 */

// 创建一个Symbol，用于表示用户的私有/唯一数据
const USER_PRIVATE_DATA = Symbol('userPrivateData');

// 模拟一个用户对象
const user = {
  name: 'Alice',
  age: 30,
  // 使用Symbol作为键，存储只有特定代码才能访问的数据
  [USER_PRIVATE_DATA]: '用户专属数据'
};

// 正常访问Symbol属性
console.log('用户数据中的Symbol属性值:', user[USER_PRIVATE_DATA]);

// 展示Symbol属性不会被常规方法枚举
console.log('遍历对象时不会显示Symbol属性');

// Object.keys() 只返回字符串键
console.log('普通属性:', Object.keys(user).join(', '));

// for...in 循环也不会遍历Symbol属性
for (let key in user) {
  console.log('for...in 遍历:', key);
}

// 获取所有Symbol属性（用于调试或特定场景）
const symbols = Object.getOwnPropertySymbols(user);
console.log('Symbol属性数量:', symbols.length);
console.log('Symbol描述:', symbols[0].description);