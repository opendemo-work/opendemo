/**
 * retry-mechanism.js
 * 带重试机制的异步操作控制器
 * 演示Generator如何实现复杂的错误处理逻辑
 */

// 模拟一个可能失败的异步操作
function flakyOperation() {
  return new Promise((resolve, reject) => {
    // 70%概率失败
    if (Math.random() < 0.7) {
      reject(new Error('操作失败'));
    } else {
      resolve('操作成功');
    }
  });
}

// Generator实现带指数退避的重试机制
function* retryOperation(maxRetries = 3) {
  let attempts = 0;
  let lastError;
  
  while (attempts < maxRetries) {
    attempts++;
    console.log(`第${attempts}次尝试：`, end='');
    
    try {
      // yield等待可能失败的操作
      const result = yield performAttempt();
      return `操作成功！最终结果：${result}`;
    } catch (error) {
      lastError = error;
      if (attempts >= maxRetries) {
        break; // 达到最大重试次数
      }
      // 计算退避时间：500ms * 尝试次数
      const backoffTime = 500 * attempts;
      console.log(`${error.message}，${backoffTime}ms后重试`);
      yield delay(backoffTime);
    }
  }
  
  throw new Error(`已达到最大重试次数(${maxRetries})，仍失败：${lastError.message}`);
}

// 辅助函数：包装延迟
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// 包装操作以便yield使用
function performAttempt() {
  return flakyOperation().catch(err => Promise.reject(err));
}

// 智能运行器，处理重试逻辑
function runWithRetry(generator) {
  const iterator = generator();
  let state = iterator.next();
  
  function handle(result) {
    if (result.done) {
      // 操作成功完成
      console.log(result.value);
      return Promise.resolve(result.value);
    } else {
      // 继续执行异步操作
      return Promise.resolve(result.value)
        .then(data => handle(iterator.next(data)))
        .catch(error => handle(iterator.throw(error)));
    }
  }
  
  return handle(state);
}

// 执行重试机制
console.log('尝试执行可能失败的操作...');
runWithRetry(retryOperation).catch(err => {
  console.error('最终失败:', err.message);
});