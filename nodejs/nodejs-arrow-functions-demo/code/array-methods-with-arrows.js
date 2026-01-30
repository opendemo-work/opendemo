/**
 * 在数组高阶方法中使用箭头函数
 * 体现函数式编程风格
 */

const numbers = [1, 2, 3, 4, 5, 6];

// 使用 filter 提取偶数
const evens = numbers.filter(n => n % 2 === 0);

// 使用 map 计算平方
const squares = numbers.map(x => x ** 2);

// 使用 reduce 求和
const sum = numbers.reduce((acc, curr) => acc + curr, 0);

// 输出结果
if (require.main === module) {
  console.log('偶数:', evens);
  console.log('平方:', squares);
  console.log('总和:', sum);
}

module.exports = { evens, squares, sum };