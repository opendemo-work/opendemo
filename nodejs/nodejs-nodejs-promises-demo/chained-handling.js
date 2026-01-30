/**
 * chained-handling.js - 演示 Promise 链式调用与错误处理
 */

// 模拟异步操作：验证数据
function validateData(data) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (data && typeof data === 'string') {
        resolve(data);
      } else {
        reject(new Error('数据格式无效'));
      }
    }, 300);
  });
}

// 模拟异步操作：格式化数据
function formatData(data) {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve(data.toUpperCase() + ' (已格式化)');
    }, 300);
  });
}

// 模拟异步操作：最终处理
function processData(formattedData) {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve(`处理结果: ${formattedData}`);
    }, 300);
  });
}

// 链式调用多个异步操作
validateData('数据示例')
  .then(formatData)
  .then(ProcessedData => {
    console.log(ProcessedData);
  })
  .catch(err => {
    console.error('流程失败:', err.message);
  });