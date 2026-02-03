// 异步事件通信示例
const EventEmitter = require('events');

// 创建数据获取事件发射器
class DataFetcher extends EventEmitter {}

const fetcher = new DataFetcher();

// 模拟异步数据获取过程
function fetchData(userId) {
  console.log('开始获取用户数据...');

  // 模拟网络延迟
  setTimeout(() => {
    // 模拟随机错误
    if (Math.random() < 0.3) {
      fetcher.emit('error', new Error('网络请求超时'));
      return;
    }

    // 模拟缓存命中
    fetcher.emit('cacheHit', `user_${userId}`);

    // 模拟数据返回
    const userData = { id: `user_${userId}`, name: 'Alice' };
    fetcher.emit('data', userData);
  }, 1000);
}

// 监听缓存命中事件
fetcher.on('cacheHit', (cacheKey) => {
  console.log(`缓存命中：${cacheKey}`);
});

// 监听数据接收事件
fetcher.on('data', (data) => {
  console.log(`数据验证通过：`, data);
});

// 统一结果处理
fetcher.on('data', (data) => {
  console.log(`最终接收到的数据：`, data);
});

// 错误处理
fetcher.on('error', (err) => {
  console.error('数据获取失败：', err.message);
});

// 启动数据获取
fetchData('123');