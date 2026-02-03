/**
 * async-flow-generator.js
 * 基本异步流程控制示例
 * 使用Generator按顺序执行多个异步任务
 */

// 模拟异步操作的辅助函数
function delay(ms, message) {
  return new Promise(resolve => {
    console.log(`延迟${ms}毫秒...`);
    setTimeout(() => resolve(message), ms);
  });
}

// Generator函数定义异步执行流程
function* asyncFlow() {
  console.log('执行第一步：初始化系统');
  const result1 = yield delay(2000, '第一步完成');
  console.log(result1);

  console.log('执行第二步：加载配置');
  const result2 = yield delay(1500, '第二步完成');
  console.log(result2);

  console.log('执行第三步：启动服务');
  const result3 = yield delay(1000, '第三步完成');
  console.log(result3);

  return '所有步骤执行完毕';
}

// 执行Generator的运行器
function run(generator) {
  const iterator = generator();
  
  function go(result) {
    if (result.done) {
      console.log(result.value);
      return;
    }
    // 当前yield返回的是Promise
    result.value.then(value => go(iterator.next(value)));
  }
  
  go(iterator.next());
}

// 启动演示
console.log('开始异步流程...');
run(asyncFlow);