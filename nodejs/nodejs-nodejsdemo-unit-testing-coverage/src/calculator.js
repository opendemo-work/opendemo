// src/calculator.js
// 简单的计算器模块，包含同步和异步方法用于测试演示

/**
 * 同步加法函数
 * @param {number} a - 第一个加数
 * @param {number} b - 第二个加数
 * @returns {number} 两数之和
 */
function add(a, b) {
  if (typeof a !== 'number' || typeof b !== 'number') {
    throw new TypeError('参数必须是数字');
  }
  return a + b;
}

/**
 * 异步获取示例数据（模拟API调用）
 * @returns {Promise<Object>} 包含示例数据的Promise
 */
function fetchData() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ id: 1, name: '测试用户' });
    }, 100);
  });
}

module.exports = { add, fetchData };