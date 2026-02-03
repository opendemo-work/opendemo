// main.js
// 主线程：创建多个 Worker 并管理任务调度

// 引入必要的模块
const { Worker } = require('worker_threads');
const path = require('path');
const { performance } = require('perf_hooks');

// 配置：启动4个线程，每个计算第20项斐波那契数（足够耗时）
const NUM_WORKERS = 4;
const TASK_INPUT = 20;

// 记录开始时间
const startTime = performance.now();

console.log(`启动 ${NUM_WORKERS} 个线程进行斐波那契计算...`);

// 创建一个Promise数组，用于收集所有Worker的结果
const workerPromises = [];

// 循环创建指定数量的工作线程
for (let i = 1; i <= NUM_WORKERS; i++) {
  // 创建新的 Worker 实例，加载工作线程脚本
  const worker = new Worker(path.resolve(__dirname, 'fibonacci-worker.js'));

  // 将每个 Worker 包装为 Promise，便于统一处理
  const promise = new Promise((resolve, reject) => {
    // 监听来自工作线程的消息
    worker.on('message', (result) => {
      console.log(`线程 #${result.taskId} 完成，结果: ${result.result}`);
      resolve(result);
    });

    // 监听错误事件，防止崩溃
    worker.on('error', reject);

    // 当 Worker 退出时触发
    worker.on('exit', (code) => {
      if (code !== 0) {
        reject(new Error(`Worker stopped with exit code ${code}`));
      }
    });
  });

  // 向工作线程发送任务数据
  worker.postMessage({ taskId: i, input: TASK_INPUT });

  // 添加到Promise数组
  workerPromises.push(promise);
}

// 等待所有线程完成
Promise.all(workerPromises)
  .then(() => {
    const endTime = performance.now();
    const duration = Math.round(endTime - startTime);
    console.log(`✅ 所有线程执行完毕，总耗时: ${duration}ms`);
  })
  .catch(err => {
    console.error('❌ 一个或多个线程执行失败:', err);
  });