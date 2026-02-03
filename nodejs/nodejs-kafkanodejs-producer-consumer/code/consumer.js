// consumer.js - Kafka 消费者示例

const { Kafka } = require('kafkajs');

// 创建 Kafka 实例
const kafka = new Kafka({
  clientId: 'my-consumer',
  brokers: ['localhost:9092']
});

// 创建消费者，属于消费者组 'my-group'
const consumer = kafka.consumer({ groupId: 'my-group' });

// 异步函数：运行消费者
async function consumeMessages() {
  const topic = 'hello-kafka';

  try {
    // 连接消费者
    await consumer.connect();
    console.log('✅ 消费者已连接');

    // 订阅主题
    await consumer.subscribe({ topic, fromBeginning: true });
    console.log('✅ 消费者已订阅主题', topic);
    console.log('🚀 等待接收消息...');

    // 开始消费消息
    await consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        const value = message.value.toString();
        console.log(`\n📨 收到消息：${value}`);
        console.log('内容:', {
          key: message.key?.toString(),
          value: value
        });
      },
    });
  } catch (error) {
    console.error('❌ 消费者出错:', error);
  }
}

// 启动消费者
consumeMessages().catch(err => {
  console.error('执行出错:', err);
});