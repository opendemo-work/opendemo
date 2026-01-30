/**
 * filter-example.js - 使用 filter 方法筛选数据
 * 场景：找出所有及格的学生
 */

// 假设这是从数据库或API获取的学生成绩列表
const allStudents = [
  { name: 'Alice', grade: 88 },
  { name: 'Bob', grade: 58 },
  { name: 'Charlie', grade: 72 },
  { name: 'Diana', grade: 91 },
  { name: 'Eve', grade: 45 }
];

// 使用 filter 方法筛选出成绩大于等于 60 的学生
const passingStudents = allStudents.filter(student => {
  return student.grade >= 60; // 返回布尔值，决定是否保留该项
});

// 输出结果
console.log('\n=== Filter 示例：及格学生 ===');
console.log(passingStudents);

// 额外提示：filter 不会改变原数组
console.log('\n原始数组长度:', allStudents.length);
console.log('筛选后数组长度:', passingStudents.length);