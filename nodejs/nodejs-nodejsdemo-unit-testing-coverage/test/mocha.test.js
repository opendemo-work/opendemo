// test/mocha.test.js
// 使用Mocha + Chai编写的BDD风格测试

const { expect } = require('chai');
const { add, fetchData } = require('../src/calculator');

// 使用Mocha的describe组织测试套件
describe('Calculator Tests', () => {
  describe('add()', () => {
    it('应正确相加两个数字', () => {
      expect(add(2, 3)).to.equal(5);
      expect(add(-1, 1)).to.equal(0);
    });

    it('应抛出非数字参数的类型错误', () => {
      expect(() => add('a', 1)).to.throw(TypeError);
    });
  });

  describe('fetchData()', () => {
    it('异步操作应成功解析', async () => {
      const result = await fetchData();
      expect(result).to.deep.equal({ id: 1, name: '测试用户' });
    });
  });
});