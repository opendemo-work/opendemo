// Jest 测试配置
// 安装: npm install --save-dev jest @types/jest
// 使用: npx jest

module.exports = {
  // 测试环境
  testEnvironment: 'node',
  
  // 测试文件匹配模式
  testMatch: [
    '**/*.test.js',
    '**/*.spec.js',
  ],
  
  // 覆盖率收集
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: [
    'text',
    'lcov',
    'html',
  ],
  
  // 覆盖率阈值
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  
  // 忽略的文件
  testPathIgnorePatterns: [
    '/node_modules/',
    '/coverage/',
    '/dist/',
  ],
  
  // 模块路径别名
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
    '^@core/(.*)$': '<rootDir>/core/$1',
    '^@utils/(.*)$': '<rootDir>/utils/$1',
  },
  
  // 设置文件
  setupFilesAfterEnv: [
    '<rootDir>/jest.setup.js',
  ],
  
  // 转换器
  transform: {
    '^.+\\.js$': 'babel-jest',
  },
  
  // 模块文件扩展名
  moduleFileExtensions: [
    'js',
    'json',
    'jsx',
    'ts',
    'tsx',
    'node',
  ],
  
  // 清除 mock
  clearMocks: true,
  
  // 详细输出
  verbose: true,
  
  // 测试超时
  testTimeout: 10000,
  
  // 失败停止
  bail: 1,
  
  // 缓存
  cache: true,
  cacheDirectory: '.jest-cache',
};
