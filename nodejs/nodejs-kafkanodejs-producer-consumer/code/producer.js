// producer.js - Kafka 生产者示例

const { Kafka } = require('kafkajs');

// 创建 Kafka 实例，连接本地 Kafka 服务
const kafka = new Kafka({
  clientId: 'my-producer',
  brokers: ['localhost:9092'] // Kafka broker 地址
});

// 创建生产者
const producer = kafka.producer();

// 异步函数：发送消息
async function sendMessage() {
  const topic = 'hello-kafka';
  const now = new Date().toISOString();
  const messageValue = `Hello Kafka! (${now})`;

  try {
    // 连接生产者
    await producer.connect();
    console.log('✅ 生产者已连接');

    // 发送消息
    console.log(`📤 消息已发送：${messageValue}`);
    await producer.send({
      topic,
      messages: [
        { value: messageValue }
      ],
    });
    console.log('✅ 消息发送成功');
  } catch (error) {
    console.error('❌ 消息发送失败:', error);
  } finally {
    // 断开连接
    await producer.disconnect();
    console.log('✨ 断开生产者连接');
  }
}

// 执行发送
sendMessage().catch(err => {
  console.error('执行出错:', err);
});