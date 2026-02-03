/**
 * path-demo-basic.js - 基础路径操作演示
 * 展示如何使用path模块进行路径拼接、解析等基本操作
 */

// 引入Node.js内置的path模块
const path = require('path');

// 示例1: 使用path.join()安全拼接路径
// 优势：自动处理不同操作系统的路径分隔符
const joinedPath = path.join('/home/user', 'documents', 'file.txt');
console.log('拼接路径:', joinedPath);

// 示例2: 提取路径的各个部分
const fileName = path.basename(joinedPath); // 获取文件名
console.log('文件名:', fileName);

const fileExt = path.extname(joinedPath); // 获取扩展名
console.log('扩展名:', fileExt);

const dirName = path.dirname(joinedPath); // 获取目录名
console.log('目录名:', dirName);

// 示例3: 解析路径为对象
const parsedPath = path.parse(joinedPath);
console.log('解析后的路径对象:', parsedPath);

// 该对象包含：root, dir, base, ext, name
