/**
 * Node.js 测试模板
 *
 * 使用方法:
 * 1. 将此文件复制到 demo 目录下
 * 2. 重命名为 *.test.js 或 *.spec.js
 * 3. 运行测试: npx jest
 *
 * 测试命名规范:
 * - 测试文件: <module>.test.js 或 <module>.spec.js
 * - 测试套件: describe('<功能名>', ...)
 * - 测试用例: test('<场景>', ...) 或 it('<场景>', ...)
 */

// ============================================================================
// 简单的测试示例
// ============================================================================

describe('Array Operations', () => {
  // 每个测试前的设置
  beforeEach(() => {
    console.log('测试前设置');
  });

  // 每个测试后的清理
  afterEach(() => {
    console.log('测试后清理');
  });

  // 所有测试前的设置
  beforeAll(() => {
    console.log('所有测试前设置');
  });

  // 所有测试后的清理
  afterAll(() => {
    console.log('所有测试后清理');
  });

  test('should add item to array', () => {
    // Arrange
    const arr = [1, 2, 3];
    
    // Act
    arr.push(4);
    
    // Assert
    expect(arr).toHaveLength(4);
    expect(arr).toContain(4);
    expect(arr).toEqual([1, 2, 3, 4]);
  });

  test('should remove item from array', () => {
    // Arrange
    const arr = [1, 2, 3];
    
    // Act
    const removed = arr.pop();
    
    // Assert
    expect(removed).toBe(3);
    expect(arr).toHaveLength(2);
  });
});

// ============================================================================
// 异步测试示例
// ============================================================================

describe('Async Operations', () => {
  test('should resolve with data', async () => {
    // Arrange
    const fetchData = () => Promise.resolve({ id: 1, name: 'Test' });
    
    // Act
    const result = await fetchData();
    
    // Assert
    expect(result).toHaveProperty('id');
    expect(result).toHaveProperty('name');
    expect(result.id).toBe(1);
  });

  test('should reject with error', async () => {
    // Arrange
    const throwError = () => Promise.reject(new Error('Network error'));
    
    // Act & Assert
    await expect(throwError()).rejects.toThrow('Network error');
  });

  test('should handle callback', (done) => {
    function asyncOperation(callback) {
      setTimeout(() => callback(null, 'success'), 100);
    }

    asyncOperation((err, result) => {
      expect(err).toBeNull();
      expect(result).toBe('success');
      done();
    });
  });
});

// ============================================================================
// Mock 测试示例
// ============================================================================

describe('Mock Functions', () => {
  test('should call mock function', () => {
    // Arrange
    const mockFn = jest.fn();
    
    // Act
    mockFn('arg1', 'arg2');
    
    // Assert
    expect(mockFn).toHaveBeenCalled();
    expect(mockFn).toHaveBeenCalledTimes(1);
    expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
  });

  test('should return mock value', () => {
    // Arrange
    const mockFn = jest.fn().mockReturnValue('mocked');
    
    // Act
    const result = mockFn();
    
    // Assert
    expect(result).toBe('mocked');
  });

  test('should mock module', () => {
    // 使用 jest.mock 来模拟模块
    // jest.mock('./module', () => ({
    //   someFunction: jest.fn().mockReturnValue('mocked')
    // }));
  });
});

// ============================================================================
// 参数化测试示例
// ============================================================================

describe('Parameterized Tests', () => {
  const testCases = [
    { input: [1, 2], expected: 3 },
    { input: [2, 3], expected: 5 },
    { input: [0, 0], expected: 0 },
  ];

  test.each(testCases)('add(%p) = %p', ({ input, expected }) => {
    const [a, b] = input;
    expect(a + b).toBe(expected);
  });

  // 使用 it.each 语法
  it.each`
    a    | b    | expected
    ${1} | ${2} | ${3}
    ${2} | ${3} | ${5}
    ${0} | ${0} | ${0}
  `('add($a, $b) = $expected', ({ a, b, expected }) => {
    expect(a + b).toBe(expected);
  });
});

// ============================================================================
// 边界条件测试
// ============================================================================

describe('Edge Cases', () => {
  test('should handle empty input', () => {
    const arr = [];
    expect(arr).toHaveLength(0);
    expect(arr).toEqual([]);
  });

  test('should handle null/undefined', () => {
    expect(null).toBeNull();
    expect(undefined).toBeUndefined();
    expect(undefined).toBeFalsy();
  });

  test('should handle large input', () => {
    const largeArray = new Array(100000).fill(0);
    expect(largeArray).toHaveLength(100000);
  });
});

// ============================================================================
// 自定义匹配器示例
// ============================================================================

expect.extend({
  toBeWithinRange(received, floor, ceiling) {
    const pass = received >= floor && received <= ceiling;
    if (pass) {
      return {
        message: () => `expected ${received} not to be within range ${floor} - ${ceiling}`,
        pass: true,
      };
    } else {
      return {
        message: () => `expected ${received} to be within range ${floor} - ${ceiling}`,
        pass: false,
      };
    }
  },
});

describe('Custom Matchers', () => {
  test('should be within range', () => {
    expect(10).toBeWithinRange(5, 15);
  });
});

// ============================================================================
// 快照测试示例
// ============================================================================

describe('Snapshot Testing', () => {
  test('should match snapshot', () => {
    const data = {
      id: 1,
      name: 'Test',
      items: ['a', 'b', 'c'],
    };
    expect(data).toMatchSnapshot();
  });
});

// ============================================================================
// 性能测试示例
// ============================================================================

describe('Performance', () => {
  test('should complete within timeout', () => {
    const start = Date.now();
    
    // 执行操作
    for (let i = 0; i < 1000000; i++) {
      Math.sqrt(i);
    }
    
    const end = Date.now();
    const elapsed = end - start;
    
    expect(elapsed).toBeLessThan(1000); // 1秒内完成
  });
});

// ============================================================================
// 跳过和条件测试
// ============================================================================

describe('Skip and Conditional', () => {
  test.skip('skipped test', () => {
    // 这个测试会被跳过
  });

  test('only run on CI', () => {
    if (!process.env.CI) {
      test.skip('Skip on local');
    }
    expect(true).toBe(true);
  });
});
