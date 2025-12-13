// 导入Node.js内置的events模块
const EventEmitter = require('events');

// 创建自定义事件发射器类
// Best Practice: 通过继承EventEmitter来封装特定业务逻辑
class LoginEmitter extends EventEmitter {}

// 实例化事件发射器
const loginEmitter = new LoginEmitter();

// 设置最大监听器数量（避免警告）
loginEmitter.setMaxListeners(15);

// 监听用户登录事件
// Best Practice: 使用有意义的事件名称
loginEmitter.on('login', (username) => {
  console.log(`用户已登录：${username}`);
});

// 监听欢迎消息事件
loginEmitter.on('welcome', () => {
  console.log('欢迎消息已发送');
});

// 使用once注册一次性事件处理器
// Best Practice: 对只需执行一次的操作使用once
loginEmitter.once('notification', () => {
  console.log('一次性通知已触发');
});

// 错误处理监听器
// Critical: 总是监听error事件防止未捕获异常
loginEmitter.on('error', (err) => {
  console.error('错误被捕获：' + err.message);
});

// 模拟事件触发流程
// 触发登录事件
loginEmitter.emit('login', 'Alice');

// 触发欢迎事件
loginEmitter.emit('welcome');

// 触发一次性通知（第二次不会执行）
loginEmitter.emit('notification');
loginEmitter.emit('notification'); // 这次不会输出

// 触发错误事件
loginEmitter.emit('error', new Error('数据加载失败'));