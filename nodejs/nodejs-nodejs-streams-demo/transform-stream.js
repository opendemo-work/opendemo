// transform-stream.js - 使用 Transform 流实时处理数据
// 示例：将输入文本转换为大写并写入文件

const { Transform } = require('stream');
const fs = require('fs');
const path = require('path');

// 创建一个自定义的 Transform 流，用于将数据转为大写
class ToUpperCaseTransform extends Transform {
  constructor(options = {}) {
    super({ ...options, encoding: 'utf8' });
  }

  // _transform 是核心方法，接收数据块进行处理
  _transform(chunk, encoding, callback) {
    try {
      // 将当前数据块转换为大写并推送到输出
      this.push(chunk.toString().toUpperCase());
      // 调用 callback 表示处理完成
      callback();
    } catch (err) {
      // 如果出错，传递错误给回调
      callback(err);
    }
  }

  // _flush 可选，用于在流结束前执行最后的写入操作
  _flush(callback) {
    // 当前示例不需要额外刷新操作
    callback();
  }
}

// 定义文件路径
const inputFile = path.resolve(__dirname, 'input.txt');
const outputFile = path.resolve(__dirname, 'output.txt');

// 创建可读流、转换流和可写流
const readStream = fs.createReadStream(inputFile, { encoding: 'utf8' });
const transformStream = new ToUpperCaseTransform();
const writeStream = fs.createWriteStream(outputFile, { encoding: 'utf8' });

// 构建数据处理管道：读取 → 转换 → 写入
readStream
  .pipe(transformStream)
  .pipe(writeStream);

// 监听完成事件
writeStream.on('finish', () => {
  console.log('数据处理完成，结果已写入 output.txt');
});

// 统一错误处理
[readStream, transformStream, writeStream].forEach(stream => {
  stream.on('error', (err) => {
    console.error('流处理过程中发生错误:', err.message);
  });
});