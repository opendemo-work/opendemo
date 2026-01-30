/**
 * buffer-concat.js
 * 场景：安全合并多个 Buffer
 * 使用 Buffer.concat() 方法高效拼接
 */

// 创建多个分段 Buffer
const hello = Buffer.from('Hello', 'utf8');
const space = Buffer.from(' ', 'utf8');
const world = Buffer.from('World', 'utf8');

console.log('分段 Buffer:', hello, ',', space, ',', world);

// 使用 Buffer.concat() 合并
const merged = Buffer.concat([hello, space, world]);

console.log('合并后的 Buffer:', merged);

// 输出最终结果字符串
console.log('最终字符串:', merged.toString('utf8'));
