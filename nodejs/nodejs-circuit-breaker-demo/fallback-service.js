// fallback-service.js
// 降级服务：在主服务不可用时提供默认响应

/**
 * 获取降级数据
 * @returns {Object} 默认的安全响应对象
 */
function getFallbackData() {
  return {
    message: '服务暂时不可用，请稍后重试',
    code: 503,
    data: null,
    timestamp: new Date().toISOString()
  };
}

module.exports = { getFallbackData };