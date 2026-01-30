/**
 * example2.js - 并行 vs 串行执行异步任务
 */

// 模拟异步任务：延迟1秒
function delayTask(name, delay = 1000) {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log(`${name}完成`);
      resolve();
    }, delay);
  });
}

// 串行执行：一个接一个
async function sequentialExecution() {
  console.log('【串行执行】');
  const start = Date.now();

  await delayTask('任务1');
  await delayTask('任务2');

  console.log(`总耗时约${(Date.now() - start) / 1000}秒\n`);
}

// 并行执行：同时开始
async function parallelExecution() {
  console.log('【并行执行】');
  const start = Date.now();

  // 同时启动两个任务，并等待全部完成
  await Promise.all([
    delayTask('任务1', 1000),
    delayTask('任务2', 1000)
  ]);

  console.log(`两个任务都已完成`);
  console.log(`总耗时约${(Date.now() - start) / 1000}秒\n`);
}

// 执行演示
async function main() {
  await sequentialExecution();
  await parallelExecution();
}

main().catch(err => console.error(err));