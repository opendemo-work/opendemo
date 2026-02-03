/**
 * 文件: spread-object.js
 * 功能: 演示展开运算符在对象中的应用
 */

// 示例1：合并对象（后续属性覆盖前面）
const profile = { name: 'Alice', age: 25 };
const settings = { city: 'Beijing', role: 'Developer' };
const userInfo = { ...profile, ...settings };
console.log('合并后的用户信息:', userInfo);

// 示例2：覆盖属性值
const userWithUpdate = { ...userInfo, age: 26 };
console.log('更新年龄后:', userWithUpdate);

// 示例3：对象浅拷贝
const point = { x: 1, y: 2 };
const copiedPoint = { ...point };
copiedPoint.x = 99; // 修改副本
console.log('浅拷贝对象:', copiedPoint);
console.log('原对象未变:', point);

// 示例4：动态添加属性
const key = 'dynamicKey';
const dynamicObj = { [key]: 'dynamicValue', ...profile };
console.log('动态属性对象:', dynamicObj);