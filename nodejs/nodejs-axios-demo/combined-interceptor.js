// combined-interceptor.js
// 演示：综合使用请求和响应拦截器，并展示如何清除拦截器

const axios = require('axios');

// 创建自定义实例
const axiosInstance = axios.create({
  baseURL: 'https://jsonplaceholder.typicode.com',
});

// 存储拦截器ID以便后续移除
let requestInterceptorId;
let responseInterceptorId;

// 设置请求拦截器
function setupRequestInterceptor() {
  requestInterceptorId = axiosInstance.interceptors.request.use(
    config => {
      console.log(`[请求] --> ${config.method.toUpperCase()} ${config.url}`);
      config.headers['Authorization'] = 'Bearer temp-token';
      return config;
    },
    error => Promise.reject(error)
  );
}

// 设置响应拦截器
function setupResponseInterceptor() {
  responseInterceptorId = axiosInstance.interceptors.response.use(
    response => {
      console.log(`[响应] <-- ${response.status} ${response.config.url}`);
      return response;
    },
    error => {
      console.error(`[错误] <-- ${error.message}`);
      return Promise.reject(error);
    }
  );
}

// 清除所有拦截器（防止内存泄漏）
function ejectInterceptors() {
  if (requestInterceptorId !== undefined) {
    axiosInstance.interceptors.request.eject(requestInterceptorId);
    console.log('已移除请求拦截器');
  }
  if (responseInterceptorId !== undefined) {
    axiosInstance.interceptors.response.eject(responseInterceptorId);
    console.log('已移除响应拦截器');
  }
}

async function runTest() {
  setupRequestInterceptor();
  setupResponseInterceptor();

  try {
    const response = await axiosInstance.get('/posts/1');
    console.log('数据:', Object.keys(response.data));
  } catch (error) {
    console.error('请求失败:', error.message);
  } finally {
    ejectInterceptors(); // 清理
  }
}

runTest();