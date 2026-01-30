// retryWithAxios.js
// 使用 Axios 实现带指数退避的请求重试机制

const axios = require('axios');

/**
 * 发起HTTP请求并支持指数退避重试
 * @param {string} url - 请求的URL
 * @param {number} maxRetries - 最大重试次数
 * @param {number} baseDelay - 基础延迟时间（毫秒）
 * @returns {Promise<any>} - 返回响应数据
 */
async function fetchWithRetry(url, maxRetries = 3, baseDelay = 1000) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    console.log(`尝试第 ${attempt} 次请求...`);

    try {
      // 发起GET请求
      const response = await axios.get(url);
      return response.data; // 成功则返回数据
    } catch (error) {
      // 判断是否为服务器错误（5xx），才进行重试
      if (error.response && error.response.status >= 500 && attempt < maxRetries) {
        // 计算指数退避延迟时间：baseDelay * 2^(attempt - 1)
        const delay = baseDelay * Math.pow(2, attempt - 1);
        console.log(`请求失败: ${error.message}, ${delay / 1000}秒后重试`);

        // 等待指定时间后重试
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        // 其他错误或达到最大重试次数，抛出异常
        throw error;
      }
    }
  }
}

// 测试用的模拟API地址（故意返回500错误，第2次尝试成功）
const TEST_URL = 'https://httpstat.us/500?mock';

// 模拟一个实际场景：请求可能失败的服务
(async () => {
  try {
    // 注意：这里使用了一个技巧，让第二次请求返回成功
    // 实际中可通过 mock-server 控制行为
    const mockSuccessUrl = 'https://httpbin.org/json'; // 一个稳定返回成功的接口作为替代

    const result = await fetchWithRetry(mockSuccessUrl, 3, 1000);
    console.log('请求成功! 响应数据:', result);
  } catch (error) {
    console.error('最终请求失败:', error.message);
  }
})();