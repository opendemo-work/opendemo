/**
 * path-demo-advanced.js - 高级路径操作演示
 * 展示resolve、normalize、relative等高级功能
 */

const path = require('path');

// 示例1: path.resolve() —— 生成绝对路径
// 从右往左解析，直到构成一个绝对路径
const absolutePath = path.resolve('folder', 'sub', 'file.txt');
console.log('绝对路径:', absolutePath);

// 示例2: path.normalize() —— 规范化路径
// 处理多余的.、..和斜杠
const messyPath = '/folder///sub/./file.txt';
const normalizedPath = path.normalize(messyPath);
console.log('规范化路径:', normalizedPath);

// 示例3: path.relative() —— 计算相对路径
const from = path.resolve('./current');
const to = path.resolve('./current/folder/sub');
const relativePath = path.relative(from, to);
console.log('从当前目录到目标目录的相对路径:', relativePath);

// 示例4: 使用系统特定的路径分隔符
console.log('路径分隔符（根据系统）:', path.sep);

// 小贴士：path.delimiter用于环境变量分隔符（如PATH）
console.log('环境变量分隔符:', path.delimiter);