/**
 * 示例1: 使用 map 和 filter 处理员工数据
 * 展示如何筛选符合条件的数据并转换格式
 */

// 模拟员工数据
const employees = [
  { name: 'Alice', age: 30, salary: 60000, position: 'Engineer' },
  { name: 'Bob', age: 25, salary: 70000, position: 'Designer' },
  { name: 'Charlie', age: 35, salary: 90000, position: 'Senior Engineer' }
];

// 场景1: 获取所有年龄大于等于30岁的员工姓名
const adultNames = employees
  .filter(employee => employee.age >= 30) // 过滤出成年人
  .map(employee => employee.name);         // 提取姓名

console.log('成年人姓名:', adultNames);

// 场景2: 给所有工程师加薪10%后获取新薪资列表
const raisedSalaries = employees
  .filter(emp => emp.position.includes('Engineer')) // 筛选工程师
  .map(emp => emp.salary * 1.1);                    // 应用10%加薪

console.log('加薪后工资:', raisedSalaries.map(s => Math.round(s)));