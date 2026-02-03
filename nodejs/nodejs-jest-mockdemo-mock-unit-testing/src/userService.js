// src/userService.js
// 用户服务业务逻辑

const { fetchUser } = require('./apiClient');

/**
 * 获取用户并添加处理时间戳
 * @param {string} userId - 用户ID
 * @returns {Promise<Object>} 包含用户信息和获取时间的对象
 */
async function getUserWithTimestamp(userId) {
  try {
    const user = await fetchUser(userId);
    return {
      ...user,
      fetchedAt: new Date().toISOString()
    };
  } catch (error) {
    throw new Error(`Failed to fetch user: ${error.message}`);
  }
}

module.exports = { getUserWithTimestamp };