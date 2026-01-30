// tests/math.test.js
// 测试数学函数及其回调处理

const { add, processWithCallback } = require('../src/math');

describe('Math Functions', () => {
  describe('add', () => {
    test('should return the sum of two numbers', () => {
      // Arrange
      const a = 2;
      const b = 3;
      const expected = 5;
      
      // Act
      const result = add(a, b);
      
      // Assert
      expect(result).toBe(expected);
    });
  });

  describe('processWithCallback', () => {
    test('should call callback and add its result to value', () => {
      // Arrange
      // 创建一个模拟函数
      const mockCallback = jest.fn();
      mockCallback.mockReturnValue(10); // 设置模拟函数返回值为10
      const value = 5;
      const expected = 15; // 10 + 5
      
      // Act
      const result = processWithCallback(mockCallback, value);
      
      // Assert
      expect(result).toBe(expected);
      expect(mockCallback).toHaveBeenCalled(); // 验证回调被调用
      expect(mockCallback).toHaveBeenCalledTimes(1); // 验证被调用一次
    });
    
    test('should pass when using different mock return values', () => {
      // Arrange
      const mockCallback = jest.fn(() => 20); // 直接定义返回值
      const value = 8;
      
      // Act
      const result = processWithCallback(mockCallback, value);
      
      // Assert
      expect(result).toBe(28);
      expect(mockCallback).toHaveBeenCalled();
    });
  });
});