// fibonacci-worker.js
// 工作线程：执行斐波那契计算（模拟CPU密集型任务）

// 引入 Worker Threads 模块中的 parentPort，用于与主线程通信
const { parentPort } = require('worker_threads');

// 定义一个计算斐波那契数列的函数（递归方式，故意低效以模拟耗时任务）
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

// 监听来自主线程的消息
parentPort.on('message', (data) => {
  // 解构获取任务ID和输入值
  const { taskId, input } = data;

  console.log(`线程 #${taskId} 开始计算 fibonacci(${input})...`);

  // 执行耗时计算
  const result = fibonacci(input);

  // 将结果发送回主线程
  parentPort.postMessage({
    taskId,
    result,
    status: 'completed'
  });
});