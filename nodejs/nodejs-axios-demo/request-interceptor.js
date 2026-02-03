// request-interceptor.js
// 演示：使用请求拦截器自动添加认证头和日志

const axios = require('axios');

// 创建自定义实例
const axiosInstance = axios.create({
  baseURL: 'https://jsonplaceholder.typicode.com',
});

// 添加请求拦截器
axiosInstance.interceptors.request.use(
  config => {
    // 在发送请求前做些什么
    console.log(`[请求拦截] 即将发送请求: ${config.url}`);
    
    // 示例：自动添加认证头
    config.headers['Authorization'] = 'Bearer fake-token';
    
    // 可扩展：添加请求时间戳、用户代理等
    config.headers['X-Request-Time'] = new Date().toISOString();
    
    return config; // 必须返回config
  },
  error => {
    // 对请求错误做些什么
    return Promise.reject(error);
  }
);

// 发起测试请求
async function testRequest() {
  try {
    const response = await axiosInstance.get('/posts/1');
    console.log(response.data);
  } catch (error) {
    console.error('请求出错:', error.message);
  }
}

testRequest();