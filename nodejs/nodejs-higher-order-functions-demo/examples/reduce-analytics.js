/**
 * 示例2: 使用 reduce 进行数据聚合分析
 * 展示如何用 reduce 实现统计功能
 */

const employees = [
  { name: 'Alice', age: 30, salary: 60000 },
  { name: 'Bob', age: 25, salary: 70000 },
  { name: 'Charlie', age: 40, salary: 90000 }
];

// 计算总薪资
const totalSalary = employees.reduce((sum, emp) => sum + emp.salary, 0);
console.log('总薪资:', totalSalary);

// 计算平均年龄
const averageAge = employees.reduce((sum, emp) => sum + emp.age, 0) / employees.length;
console.log('平均年龄:', Number(averageAge.toFixed(2)));

// 找出最年轻的员工年龄
const youngestAge = employees.reduce((min, emp) => (emp.age < min ? emp.age : min), Infinity);
console.log('最年轻员工:', youngestAge);

// 构建按职位分组的映射（高级 reduce 用法）
const groupedByPosition = employees.reduce((groups, emp) => {
  const pos = emp.position || 'Unknown';
  if (!groups[pos]) groups[pos] = [];
  groups[pos].push(emp);
  return groups;
}, {});

console.log('按职位分组:', Object.keys(groupedByPosition));