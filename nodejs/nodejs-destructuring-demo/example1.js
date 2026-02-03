/**
 * example1.js - 对象解构基础与进阶用法
 * 展示如何从对象中提取属性，并使用默认值和重命名
 */

// 模拟一个用户对象
const user = {
  name: 'Alice',
  age: 25,
  city: '北京',
  email: 'alice@example.com'
};

// 基础解构：提取指定字段
const { name, age } = user;
console.log(`【示例1-基础】用户姓名：${name}，年龄：${age}`);

// 重命名字段：将 city 解构为 residence
const { city: residence } = user;
console.log(`【示例1-重命名】居住地：${residence}`);

// 设置默认值：防止 undefined
const { nickname = '未设置昵称' } = user;
console.log(`【示例1-默认值】昵称：${nickname}`);

// 混合使用：重命名 + 默认值
const { phone = '无联系方式', email: contact } = user;
console.log(`【示例1-混合】联系邮箱：${contact}，电话：${phone}`);

// 嵌套对象解构
const student = {
  personal: {
    name: 'Bob',
    grade: 'A'
  },
  school: '清华大学'
};

const {
  personal: { name: studentName, grade },
  school
} = student;

console.log(`【示例1-嵌套】学生 ${studentName} 成绩 ${grade}，就读于 ${school}`);