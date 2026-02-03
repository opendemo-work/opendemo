// callback-basics.js - 基础回调函数示例

/**
 * 模拟一个异步操作，比如网络请求或定时任务
 * @param {function} callback - 回调函数，接收两个参数：error 和 result
 */
function doAsyncTask(callback) {
  console.log('开始执行异步任务...');

  // 使用 setTimeout 模拟异步延迟
  setTimeout(() => {
    const success = true; // 模拟操作成功

    if (success) {
      // 成功时，第一个参数传 null（无错误），第二个传结果
      callback(null, 'Hello from callback!');
    } else {
      // 失败时，传入错误对象
      callback(new Error('任务失败'), null);
    }
  }, 1000); // 1秒后执行
}

// 调用异步函数并传入回调
doAsyncTask((error, result) => {
  if (error) {
    console.error('发生错误：', error.message);
  } else {
    console.log('任务完成！结果是：', result);
  }
});