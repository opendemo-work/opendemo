// tests/userService.test.js
// 测试用户服务，演示模块模拟

// 在引入被测模块前先mock依赖
jest.mock('../src/apiClient');

const { getUserWithTimestamp } = require('../src/userService');
const { fetchUser } = require('../src/apiClient');

describe('UserService', () => {
  describe('getUserWithTimestamp', () => {
    test('should return user data with timestamp when API call succeeds', async () => {
      // Arrange
      const mockUserId = '123';
      const mockUserData = { id: '123', name: 'John Doe' };
      
      // 模拟fetchUser函数返回成功Promise
      fetchUser.mockResolvedValue(mockUserData);
      
      // 确保异步断言被执行
      expect.assertions(2);
      
      // Act
      const result = await getUserWithTimestamp(mockUserId);
      
      // Assert
      expect(result).toEqual({
        ...mockUserData,
        fetchedAt: expect.any(String) // 验证时间戳存在且为字符串
      });
      expect(fetchUser).toHaveBeenCalledWith(mockUserId);
    });
    
    test('should throw error when API call fails', async () => {
      // Arrange
      const mockUserId = '999';
      const mockError = new Error('Network error');
      
      // 模拟fetchUser函数返回拒绝的Promise
      fetchUser.mockRejectedValue(mockError);
      
      // Act & Assert
      await expect(getUserWithTimestamp(mockUserId)).rejects.toThrow('Failed to fetch user');
      expect(fetchUser).toHaveBeenCalledWith(mockUserId);
    });
    
    test('should verify mock call count', async () => {
      // Arrange
      fetchUser.mockResolvedValue({ id: '456', name: 'Jane Doe' });
      
      // Act
      await getUserWithTimestamp('456');
      await getUserWithTimestamp('456');
      
      // Assert
      expect(fetchUser).toHaveBeenCalledTimes(2);
    });
  });
});