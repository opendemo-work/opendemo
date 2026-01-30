/**
 * example1.js - 基础 async/await 示例：模拟获取用户信息
 */

// 模拟从服务器获取用户数据的异步函数
function fetchUser() {
  // 返回一个延迟1秒后解析的 Promise
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ name: 'Alice' });
    }, 1000);
  });
}

// 使用 async/await 的异步主函数
async function main() {
  console.log('正在获取用户信息...');

  // await 会暂停函数执行，直到 Promise 完成
  const user = await fetchUser();

  console.log(`用户姓名：${user.name}`);
}

// 调用异步函数
main().catch(err => console.error(err));