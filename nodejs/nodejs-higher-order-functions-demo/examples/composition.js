/**
 * 示例3: 高阶函数组合与链式调用
 * 展示如何组合多个函数解决复杂问题
 */

const employees = [
  { name: 'Alice', age: 30, salary: 60000, position: 'Senior Engineer' },
  { name: 'Bob', age: 25, salary: 70000, position: 'Designer' },
  { name: 'Charlie', age: 35, salary: 100000, position: 'Senior Engineer' }
];

// 场景1: 计算所有高级工程师的总薪资
const seniorTotalSalary = employees
  .filter(e => e.position === 'Senior Engineer')
  .map(e => e.salary)
  .reduce((sum, salary) => sum + salary, 0);

console.log('高级工程师总薪资:', seniorTotalSalary);

// 场景2: 找出年龄 >= 30 且是工程师的员工姓名
const qualifiedNames = employees
  .filter(e => e.age >= 30 && e.position.includes('Engineer'))
  .map(e => e.name);

console.log('符合条件的员工姓名:', qualifiedNames);

// 场景3: 使用函数组合思想重构（更清晰）
const isExperiencedEngineer = e => e.age >= 30 && e.position.includes('Engineer');
const getName = e => e.name;

const result = employees.filter(isExperiencedEngineer).map(getName);
console.log('经验丰富的工程师:', result);