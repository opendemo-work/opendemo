// copy-stream.js - 使用流安全复制大文件
// 适用于处理 GB 级别文件而不占用过多内存

const fs = require('fs');
const path = require('path');

// 定义输入输出文件路径
const inputFile = path.resolve(__dirname, 'input.txt');
const outputFile = path.resolve(__dirname, 'output.txt');

// 创建可读流（从源文件读取数据）
const readableStream = fs.createReadStream(inputFile, {
  encoding: 'utf8',
  highWaterMark: 64 * 1024 // 每次读取 64KB，可根据需要调整
});

// 创建可写流（向目标文件写入数据）
const writableStream = fs.createWriteStream(outputFile, {
  encoding: 'utf8'
});

// 使用 pipe 连接读取流和写入流
// pipe 会自动处理背压（backpressure），确保不会因速度不匹配导致内存溢出
readableStream.pipe(writableStream);

// 监听写入完成事件
writableStream.on('finish', () => {
  console.log(`文件复制完成：${inputFile} → ${outputFile}`);
});

// 错误处理：任一流出现错误时及时捕获
readableStream.on('error', (err) => {
  console.error('读取文件时出错:', err.message);
});

writableStream.on('error', (err) => {
  console.error('写入文件时出错:', err.message);
});