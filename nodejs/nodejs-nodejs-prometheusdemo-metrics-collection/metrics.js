// metrics.js - 自定义Prometheus指标定义
const client = require('prom-client');

// 清空默认指标注册表（避免测试干扰）
client.register.clear();

// 创建HTTP请求计数器
// 用于统计按方法、路径和状态码划分的请求数量
const httpRequestCounter = new client.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests made',
  labelNames: ['method', 'route', 'status_code'],
});

// 创建API响应时间直方图
// 用于观测接口延迟分布
const responseTimeHistogram = new client.Histogram({
  name: 'api_response_time_milliseconds',
  help: 'API请求响应时间（毫秒）',
  labelNames: ['route'],
  buckets: [10, 50, 100, 200, 500] // 定义时间桶（ms）
});

// 示例：业务事件计数器
const userLoginCounter = new client.Counter({
  name: 'user_login_attempts_total',
  help: 'Total number of user login attempts',
  labelNames: ['success'] // 区分成功与失败
});

// 注册一个动态指标（例如当前活跃用户）
const activeUsers = new client.Gauge({
  name: 'active_users',
  help: '当前活跃用户数量'
});

// 模拟活跃用户数波动
setInterval(() => {
  activeUsers.set(Math.floor(Math.random() * 10) + 1);
}, 3000);

// 导出指标实例供其他模块使用
module.exports = {
  httpRequestCounter,
  responseTimeHistogram,
  userLoginCounter,
  activeUsers
};