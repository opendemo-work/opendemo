/**
 * concurrent-requests.js - 演示使用 Promise.all 并发执行多个异步任务
 */

// 模拟从不同源获取数据的异步函数
function fetchData(id) {
  return new Promise(resolve => {
    const delay = Math.floor(Math.random() * 1000) + 500; // 随机延迟 500-1500ms
    setTimeout(() => {
      resolve(`结果${id}`);
    }, delay);
  });
}

// 并发发起三个请求
console.log('开始并发请求...');

Promise.all([
  fetchData(1),
  fetchData(2),
  fetchData(3)
])
  .then(results => {
    console.log('所有请求完成:', results);
  })
  .catch(error => {
    console.error('某个请求失败:', error.message);
  });