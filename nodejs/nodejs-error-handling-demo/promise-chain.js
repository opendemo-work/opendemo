/**
 * promise-chain.js - Promise 链错误处理示例
 * 
 * 展示如何通过 .catch() 处理多个 .then() 组成的异步链中的错误。
 */

function stepOne() {
  return Promise.resolve('原始数据');
}

function stepTwo(data) {
  return Promise.resolve(`${data} -> 已处理`);
}

function stepThree(processedData) {
  return Promise.reject(new Error('第三步模拟失败'));
}

console.log('[PROMISE] 开始一连串异步操作...');

stepOne()
  .then(data => {
    console.log('[PROMISE] 第一步完成：', data);
    return stepTwo(data);
  })
  .then(processedData => {
    console.log('[PROMISE] 第二步完成：', processedData);
    return stepThree(processedData);
  })
  .then(finalResult => {
    console.log('[PROMISE] 最终结果：', finalResult);
  })
  .catch(err => {
    // 任何前面步骤的 reject 都会跳到这里
    console.error('[PROMISE] 错误被捕获:', err.message);
  })
  .finally(() => {
    console.log('[PROMISE] 整个流程结束，错误被集中处理。');
  });