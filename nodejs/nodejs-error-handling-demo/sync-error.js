/**
 * sync-error.js - 同步错误处理示例
 * 
 * 本文件演示如何使用 try-catch 捕获同步代码中抛出的错误。
 */

console.log('[SYNC] 开始执行可能出错的操作...');

try {
  // 模拟一个可能出错的同步操作
  function loadDataSync() {
    throw new Error('发生了一个同步错误！');
  }

  const data = loadDataSync();
  console.log('[SYNC] 数据加载成功:', data);
} catch (err) {
  // 捕获并处理错误
  console.error('[SYNC] 错误被捕获:', err.message);
} finally {
  // 无论是否出错都会执行
  console.log('[SYNC] 程序继续运行，未崩溃。');
}