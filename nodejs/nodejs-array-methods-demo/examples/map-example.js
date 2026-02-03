/**
 * map-example.js - 使用 map 方法进行数据转换
 * 场景：将学生成绩转换为带评级的对象
 */

// 定义初始学生数据数组
const students = [
  { name: 'Alice', grade: 88 },
  { name: 'Bob', grade: 58 },
  { name: 'Charlie', grade: 72 },
  { name: 'Diana', grade: 91 },
  { name: 'Eve', grade: 45 }
];

// 使用 map 方法创建一个新数组，每个元素包含学生姓名和成绩等级
const gradedStudents = students.map(student => {
  // 根据分数判断等级
  let level;
  if (student.grade >= 90) {
    level = 'A';
  } else if (student.grade >= 80) {
    level = 'B';
  } else if (student.grade >= 70) {
    level = 'C';
  } else if (student.grade >= 60) {
    level = 'D';
  } else {
    level = 'F';
  }

  // 返回新对象，保持原始数据不可变
  return {
    name: student.name,
    grade: student.grade,
    letterGrade: level
  };
});

// 输出结果
console.log('\n=== Map 示例：成绩评级 ===');
gradedStudents.forEach(s => {
  console.log(`${s.name}: ${s.letterGrade}`);
});