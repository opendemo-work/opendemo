// async.js - 异步函数示例：使用async/await模拟API调用

// 模拟异步API请求（如从数据库或远程服务获取数据）
function fetchUserData(id) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ id: id, name: 'Alice' });
    }, 1000); // 模拟1秒延迟
  });
}

// async函数：用于处理异步操作
async function getUserAndLog(id) {
  console.log('正在获取用户数据...');

  // await会暂停函数执行直到Promise完成
  const userData = await fetchUserData(id);

  console.log('用户数据:', userData);
  return userData;
}

// 调用异步函数并处理结果
getUserAndLog(1).catch(err => {
  console.error('发生错误:', err);
});