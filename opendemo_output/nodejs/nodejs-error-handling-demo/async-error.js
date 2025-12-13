/**
 * async-error.js - 异步错误处理示例 (async/await)
 * 
 * 演示如何在 async 函数中使用 try/catch 处理异步错误。
 */

async function fetchData() {
  // 模拟异步操作（如API调用）
  return new Promise((_, reject) => {
    setTimeout(() => {
      reject(new Error('异步任务失败：网络请求超时'));
    }, 1000);
  });
}

async function main() {
  console.log('[ASYNC] 异步操作开始...');

  try {
    const result = await fetchData();
    console.log('[ASYNC] 结果:', result);
  } catch (err) {
    // await 的 Promise 被 reject 时，错误会被 catch 捕获
    console.error('[ASYNC] 错误被捕获:', err.message);
  } finally {
    console.log('[ASYNC] 错误已妥善处理，程序正常退出。');
  }
}

// 执行主函数
main().catch(err => {
  // 防御性编程：防止 main 内部未捕获的错误
  console.error('Unexpected error in main:', err);
});