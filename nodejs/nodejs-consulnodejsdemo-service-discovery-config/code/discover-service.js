/**
 * discover-service.js
 * 功能：从Consul发现指定服务的可用实例列表
 */

const Consul = require('consul');
const consul = new Consul();

// 要查找的服务名
const serviceName = 'demo-service';

// 查询健康的服务实例
async function discoverService() {
  try {
    // 查询服务的健康实例
    const result = await consul.health.service({
      service: serviceName,
      passing: true // 仅返回通过健康检查的实例
    });

    // 提取服务地址和端口
    const instances = result.map(entry => ({
      ServiceAddress: entry.Service.Address,
      ServicePort: entry.Service.Port
    }));

    console.log(`🔍 发现服务 ${serviceName} 的实例：`);
    console.log(instances);
    
  } catch (err) {
    console.error('❌ 服务发现失败:', err.message);
  }
}

// 执行发现
discoverService();