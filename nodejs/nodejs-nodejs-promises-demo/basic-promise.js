/**
 * basic-promise.js - 演示 Promise 的基本创建与使用
 */

// 模拟一个异步获取用户数据的函数
function fetchUser(id) {
  return new Promise((resolve, reject) => {
    // 模拟网络延迟
    setTimeout(() => {
      if (id > 0) {
        resolve({ id: id, name: 'Alice' }); // 成功时调用 resolve
      } else {
        reject(new Error('无效的用户ID'));   // 失败时调用 reject
      }
    }, 500);
  });
}

// 使用 Promise 的方式获取用户
fetchUser(1)
  .then(user => {
    // 成功处理
    console.log(`用户加载成功: ${user.name}`);
  })
  .catch(error => {
    // 错误处理
    console.error('加载失败:', error.message);
  });