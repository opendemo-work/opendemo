// map-demo.js - 演示Map数据结构的使用

// 创建一个新的Map实例
// Map允许使用任何类型的值作为键或值，并保持插入顺序
const userMap = new Map();

// 使用.set()方法添加键值对
// 键可以是字符串、数字、对象甚至函数
userMap.set('user1', { name: 'Alice', age: 25 });
userMap.set('user2', { name: 'Bob', age: 30 });

// 使用.get()方法根据键获取对应的值
const userInfo = userMap.get('user1');
console.log('用户信息:', userInfo);

// Map也常用于配置或映射表
const gradeMap = new Map();
gradeMap.set('数学', 'A');
gradeMap.set('英语', 'B+');
console.log('课程映射:', [...gradeMap].map(([k, v]) => `${k} → ${v}`).join(', '));

// 更新值
gradeMap.set('英语', 'A+');
console.log('更新后成绩:', gradeMap.get('英语'));

// 删除某个键值对
gradeMap.delete('英语');
console.log('删除英语成绩后:', gradeMap);

// 遍历Map（可选）
// gradeMap.forEach((value, key) => {
//   console.log(`${key}: ${value}`);
// });