/**
 * register-service.js
 * 功能：将当前服务注册到Consul，支持健康检查
 */

// 引入Consul客户端库
const Consul = require('consul');

// 创建Consul实例，默认连接 http://localhost:8500
const consul = new Consul();

// 定义服务信息
const serviceOptions = {
  name: 'demo-service', // 服务名称
  address: '127.0.0.1', // 服务IP
  port: 3000,           // 服务端口
  check: {
    http: `http://127.0.0.1:3000/health`, // 健康检查路径
    interval: '10s',   // 检查间隔
    timeout: '5s'
  }
};

// 注册服务到Consul
async function registerService() {
  try {
    await consul.agent.service.register(serviceOptions);
    console.log('✅ 服务 \'' + serviceOptions.name + '\' 已成功注册到Consul');
    
    // 模拟健康检查响应（实际应在Web服务器中实现 /health 接口）
    setInterval(() => {
      console.log('→ 每10秒发送一次健康检查心跳');
    }, 10000);
  } catch (err) {
    console.error('❌ 服务注册失败:', err.message);
    process.exit(1);
  }
}

// 执行注册
registerService();

// 优雅关闭（可选）
process.on('SIGINT', async () => {
  try {
    await consul.agent.service.deregister(serviceOptions.name);
    console.log('\n🛑 服务已注销');
    process.exit(0);
  } catch (err) {
    console.error('注销失败:', err.message);
  }
});