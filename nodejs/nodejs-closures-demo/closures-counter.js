/**
 * 示例1：使用闭包实现计数器
 * 
 * 说明：每次调用 createCounter() 都会创建一个新的独立计数器实例
 * 利用闭包保持对局部变量 'count' 的引用，实现状态持久化
 */

function createCounter() {
  // 这个变量被内部函数引用，不会被垃圾回收
  let count = 0;

  // 返回一个函数，该函数形成了闭包，可以访问外部的 count 变量
  return function() {
    count++; // 每次调用都会修改外部函数的局部变量
    return count;
  };
}

// 创建两个独立的计数器实例
const counter1 = createCounter();
const counter2 = createCounter();

// 调用并输出结果
console.log(`计数器1: ${counter1()}`); // 1
console.log(`计数器1: ${counter1()}`); // 2
console.log(`计数器2: ${counter2()}`); // 1（独立状态）
console.log(`计数器1: ${counter1()}`); // 3