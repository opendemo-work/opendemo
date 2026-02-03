// src/math.js
// 数学计算工具函数

/**
 * 加法运算
 * @param {number} a - 第一个加数
 * @param {number} b - 第二个加数
 * @returns {number} 两数之和
 */
function add(a, b) {
  return a + b;
}

/**
 * 执行回调函数并对结果进行加法运算
 * @param {Function} callback - 回调函数
 * @param {number} value - 基础值
 * @returns {number} 回调结果与基础值的和
 */
function processWithCallback(callback, value) {
  const callbackResult = callback();
  return add(callbackResult, value);
}

module.exports = { add, processWithCallback };