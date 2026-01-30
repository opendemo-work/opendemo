/**
 * buffer-stream.js
 * 场景：使用 Buffer 模拟流式数据传输
 * 演示如何将 Buffer 分块通过可读流发送
 */

const { Readable } = require('stream');

// 创建包含文本的 Buffer
const data = Buffer.from('Hello', 'utf8');

// 创建自定义可读流
const stream = new Readable({
  read() {
    // 每次推送一个字节
    for (let i = 0; i < data.length; i++) {
      this.push(data.slice(i, i + 1)); // 推送单字节 Buffer
    }
    // 发送结束信号
    this.push(null);
  }
});

// 监听数据事件
console.log('正在通过流发送数据块...');
stream.on('data', (chunk) => {
  console.log('数据块接收:', chunk.toString());
});

// 监听结束事件
stream.on('end', () => {
  console.log('流结束，传输完成。');
});
