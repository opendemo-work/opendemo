/**
 * freezeObject.js
 * 功能：演示如何冻结对象以防止修改
 * 使用 Object.freeze() 创建不可变对象
 */

'use strict';

// 创建一个可变对象
const user = {
  name: 'Bob',
  role: 'developer'
};

// 冻结对象，使其不可更改
Object.freeze(user);

// 尝试修改冻结对象的属性（在非严格模式下静默失败）
user.role = 'manager';
user.email = 'bob@example.com'; // 添加新属性也会失败

// 验证对象是否真正被冻结
if (user.role !== 'manager' && !("email" in user)) {
  console.log('尝试修改冻结对象失败 → 冻结生效！');
} else {
  console.log('冻结未生效，请检查代码逻辑');
}