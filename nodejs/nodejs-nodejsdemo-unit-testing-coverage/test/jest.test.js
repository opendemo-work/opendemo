// test/jest.test.js
// 使用Jest编写的单元测试

const { add, fetchData } = require('../src/calculator');

// 测试同步函数
test('加法函数应正确相加', () => {
  expect(add(2, 3)).toBe(5);
  expect(add(-1, 1)).toBe(0);
});

// 测试异步函数
test('异步获取数据应返回正确结果', async () => {
  await expect(fetchData()).resolves.toEqual({
    id: 1,
    name: '测试用户'
  });
});