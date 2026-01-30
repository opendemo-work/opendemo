/**
 * 示例2：实现自定义迭代器
 * 
 * 演示如何使用Symbol.iterator让对象支持for...of和扩展运算符
 */

/**
 * 范围类 - 表示一个整数区间，并可逐个迭代
 */
class Range {
  /**
   * 构造函数
   * @param {number} start - 起始值（包含）
   * @param {number} end - 结束值（不包含）
   */
  constructor(start, end) {
    this.start = start;
    this.end = end;
  }

  /**
   * 实现迭代器协议
   * 当对象需要被迭代时（如for...of），JS引擎会调用此方法
   * @returns {Iterator} 返回一个迭代器对象
   */
  [Symbol.iterator]() {
    let current = this.start;
    const end = this.end;

    // 返回符合迭代器协议的对象
    return {
      next() {
        // 控制迭代结束条件
        if (current < end) {
          return { value: current++, done: false };
        } else {
          return { done: true };
        }
      }
    };
  }
}

// 创建一个范围对象：从1到5
const range = new Range(1, 6); // 1,2,3,4,5

// 使用for...of遍历（依赖Symbol.iterator）
console.log('使用for...of遍历范围对象:');
for (const value of range) {
  console.log(value);
}

// 也可以用于扩展运算符
const arrayFromRange = [...range];
console.log('转换为数组:', arrayFromRange);

// 验证其可迭代性
console.log('对象是否可迭代:', typeof range[Symbol.iterator] === 'function');