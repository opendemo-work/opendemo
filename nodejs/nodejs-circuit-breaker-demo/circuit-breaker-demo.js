// circuit-breaker-demo.js
// 主程序：演示熔断器在异常场景下的保护机制

const { CircuitBreaker } = require('circuit-breaker-js');
const { getFallbackData } = require('./fallback-service');

// 模拟不稳定的远程服务调用
function unstableServiceCall() {
  return new Promise((resolve, reject) => {
    // 随机模拟成功或失败（70% 失败率）
    const fail = Math.random() < 0.7;
    setTimeout(() => {
      if (fail) {
        reject(new Error('模拟网络超时'));
      } else {
        resolve('成功响应');
      }
    }, 1000);
  });
}

// 创建熔断器实例
// 当连续2次失败后，触发熔断，持续5秒
const circuitBreaker = new CircuitBreaker(unstableServiceCall, {
  threshold: 2,           // 失败次数阈值
  timeout: 5000,          // 熔断开启时间（毫秒）
  fallback: () => {
    console.log(`${new Date().toISOString()} 调用服务... 熔断器已开启，执行降级逻辑`);
    return getFallbackData();
  }
});

// 循环调用服务，观察熔断行为
async function runDemo() {
  for (let i = 0; i < 6; i++) {
    try {
      console.log(`${new Date().toISOString()} 调用服务...`);
      const result = await circuitBreaker.call();
      console.log(`响应: ${result}`);
    } catch (err) {
      console.error(`错误: ${err.message}`);
    }
    await new Promise(resolve => setTimeout(resolve, 1200)); // 控制调用频率
  }
}

// 启动演示
runDemo().catch(console.error);