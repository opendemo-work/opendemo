/**
 * reduce-example.js - 使用 reduce 方法进行数据聚合
 * 场景：统计班级成绩总分、平均分和各等级分布
 */

// 学生数据源（可来自API或数据库）
const students = [
  { name: 'Alice', grade: 88 },
  { name: 'Bob', grade: 58 },
  { name: 'Charlie', grade: 72 },
  { name: 'Diana', grade: 91 },
  { name: 'Eve', grade: 45 }
];

// 初始化累加器对象
const initialAccumulator = {
  total: 0,           // 总分
  count: 0,           // 学生数量
  gradeCounts: {      // 各等级计数
    A: 0,
    B: 0,
    C: 0,
    D: 0,
    F: 0
  }
};

// 使用 reduce 一次遍历完成多项统计
const stats = students.reduce((acc, student) => {
  // 累加总分和人数
  acc.total += student.grade;
  acc.count++;

  // 根据成绩增加对应等级计数
  const { grade } = student;
  if (grade >= 90) acc.gradeCounts.A++;
  else if (grade >= 80) acc.gradeCounts.B++;
  else if (grade >= 70) acc.gradeCounts.C++;
  else if (grade >= 60) acc.gradeCounts.D++;
  else acc.gradeCounts.F++;

  // 返回更新后的累加器
  return acc;
}, initialAccumulator);

// 计算平均分（保留一位小数）
stats.average = parseFloat((stats.total / stats.count).toFixed(1));

// 删除不需要暴露的中间变量
delete stats.count;

// 输出最终统计结果
console.log('\n=== Reduce 示例：统计结果 ===');
console.log(stats);