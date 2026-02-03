// retryWithFetch.js
// 使用 node-fetch 实现自定义的指数退避重试逻辑

const fetch = require('node-fetch');

/**
 * 使用 fetch 发起请求并支持指数退避重试
 * @param {string} url - 请求地址
 * @param {Object} options - fetch选项
 * @param {number} maxRetries - 最大重试次数
 * @param {number} baseDelay - 基础延迟时间（毫秒）
 * @returns {Promise<any>} - 解析后的JSON数据
 */
async function fetchWithExponentialBackoff(url, options = {}, maxRetries = 3, baseDelay = 1000) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    // 计算当前尝试的延迟时间
    const delay = baseDelay * Math.pow(2, attempt - 1);
    console.log(`尝试第 ${attempt} 次请求 (延迟 ${delay}ms)...`);

    try {
      const response = await fetch(url, options);

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      return data; // 成功则返回
    } catch (error) {
      // 如果不是最后一次尝试，则进行重试
      if (attempt < maxRetries) {
        console.log(`请求失败: ${error.message}, 重试中... 当前延迟: ${delay * 2}ms`);
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        // 所有重试均失败，抛出最终错误
        throw new Error(`请求失败，经过${maxRetries}次重试仍无法成功: ${error.message}`);
      }
    }
  }
}

// 示例使用：请求一个稳定的公共API
(async () => {
  try {
    const url = 'https://httpbin.org/json';
    const result = await fetchWithExponentialBackoff(url, {}, 3, 1000);
    console.log('请求成功:', result);
  } catch (error) {
    console.error('最终错误:', error.message);
  }
})();