/**
 * deepClone.js
 * 功能：演示对象的深拷贝操作
 * 使用 JSON 方法实现深拷贝，适用于纯数据对象
 */

'use strict';

// 定义一个包含嵌套结构的原始对象
const originalObj = {
  name: 'Alice',
  age: 30,
  address: {
    city: 'Beijing',
    zip: '100000'
  },
  hobbies: ['reading', 'coding']
};

// 使用 JSON 方法进行深拷贝
// 注意：此方法不适用于含函数、undefined、Symbol 的对象
const clonedObj = JSON.parse(JSON.stringify(originalObj));

// 修改原始对象的嵌套属性
originalObj.address.city = 'Shanghai';
originalObj.hobbies.push('traveling');

// 验证克隆对象是否独立
if (clonedObj.address.city === 'Beijing' && clonedObj.hobbies.length === 2) {
  console.log('原始对象修改后，副本未受影响 → 深拷贝成功！');
} else {
  console.log('深拷贝失败：副本受到原始对象影响');
}