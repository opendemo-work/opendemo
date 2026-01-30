// src/apiClient.js
// 模拟外部API客户端

/**
 * 从远程API获取用户数据
 * @param {string} userId - 用户ID
 * @returns {Promise<Object>} 用户信息Promise
 */
async function fetchUser(userId) {
  // 模拟实际的API请求
  const response = await fetch(`/api/users/${userId}`);
  return response.json();
}

module.exports = { fetchUser };