/**
 * example3.js - async/await 错误处理演示
 */

// 模拟可能失败的异步操作
function fetchProtectedResource(validToken = false) {
  return new Promise((_, reject) => {
    setTimeout(() => {
      if (!validToken) {
        reject(new Error('访问被拒绝！'));
      } else {
        resolve('资源数据');
      }
    }, 1000);
  });
}

// 使用 try/catch 处理异步错误
async function main() {
  console.log('尝试获取受保护资源...');

  try {
    // 尝试调用失败的异步函数
    await fetchProtectedResource(false);
  } catch (error) {
    // 错误会在这里被捕获
    console.log(`错误被捕获：${error.message}`);
  } finally {
    console.log('异步操作继续执行');
  }
}

// 调用主函数
main().catch(err => console.error(err));