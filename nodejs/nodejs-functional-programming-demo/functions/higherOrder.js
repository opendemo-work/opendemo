// higherOrder.js - 高阶函数示例：函数作为参数传递

// 示例数据：用户列表
const users = [
  { name: '张三', age: 17 },
  { name: '李四', age: 25 },
  { name: '王五', age: 30 }
];

// 普通函数：判断是否成年
function isAdult(user) {
  return user.age >= 18;
}

// 高阶函数应用：filter接收一个函数作为参数
const adults = users.filter(isAdult);

// 使用箭头函数结合map提取姓名
const names = adults.map(user => user.name);

// 组合函数：将多个操作链式调用
const getAdultNames = (users) => {
  return users
    .filter(u => u.age >= 18)
    .map(u => u.name);
};

// 输出结果
console.log('成年人:', adults);
console.log('成年人名字:', getAdultNames(users));