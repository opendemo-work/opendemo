// response-interceptor.js
// 演示：使用响应拦截器统一处理成功和错误响应

const axios = require('axios');

// 创建自定义实例
const axiosInstance = axios.create({
  baseURL: 'https://jsonplaceholder.typicode.com',
});

// 添加响应拦截器
axiosInstance.interceptors.response.use(
  response => {
    // 对响应数据做点什么
    console.log(`[响应拦截] 请求成功: ${response.status} ${response.statusText}`);
    return response; // 必须返回response
  },
  error => {
    // 对响应错误做点什么
    if (error.response) {
      // 服务器返回了非2xx状态码
      console.error(`[响应拦截] HTTP错误: ${error.response.status} ${error.response.statusText}`);
    } else if (error.request) {
      // 请求已发出但无响应
      console.error('[响应拦截] 网络错误: 无法连接到服务器');
    } else {
      // 其他错误
      console.error(`[响应拦截] 请求设置错误: ${error.message}`);
    }
    return Promise.reject(error);
  }
);

// 发起测试请求
async function testResponse() {
  try {
    const response = await axiosInstance.get('/posts/1');
    console.log(response.data);
  } catch (error) {
    console.error('最终捕获错误:', error.message);
  }
}

testResponse();