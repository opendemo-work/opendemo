/**
 * 文件: spread-array.js
 * 功能: 演示展开运算符在数组中的应用
 */

// 示例1：合并两个数组
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const mergedArray = [...arr1, ...arr2];
console.log('合并后的数组:', mergedArray);

// 示例2：复制数组（避免引用同一内存）
const originalArray = ['a', 'b', 'c'];
const copiedArray = [...originalArray];
copiedArray.push('d'); // 修改副本不影响原数组
console.log('复制的数组:', copiedArray);
console.log('原数组未变:', originalArray);

// 示例3：展开可迭代对象（如字符串）
const str = 'hello';
const charArray = [...str];
console.log('展开字符串:', charArray);

// 示例4：作为函数参数传递
function sum(a, b, c) {
  return a + b + c;
}
const numbers = [10, 20, 30];
console.log('函数传参展开:', sum(...numbers));