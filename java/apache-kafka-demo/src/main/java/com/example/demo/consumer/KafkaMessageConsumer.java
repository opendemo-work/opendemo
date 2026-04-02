package com.example.demo.consumer;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Component;

/**
 * Kafka消息消费者
 * 
 * 演示多种消费模式
 */
@Component
public class KafkaMessageConsumer {
    
    /**
     * 基础消息消费
     * 
     * @KafkaListener: 监听指定topic
     * groupId: 消费者组ID
     */
    @KafkaListener(topics = "demo-topic", groupId = "demo-group")
    public void consumeDemoTopic(String message) {
        System.out.println("[Consumer-1] 收到消息: " + message);
    }
    
    /**
     * 带消息元数据的消费
     */
    @KafkaListener(topics = "demo-topic", groupId = "demo-group-2")
    public void consumeWithMetadata(
            @Payload String message,
            @Header(KafkaHeaders.RECEIVED_PARTITION_ID) int partition,
            @Header(KafkaHeaders.OFFSET) long offset,
            @Header(KafkaHeaders.RECEIVED_KEY) String key) {
        
        System.out.println("[Consumer-2] 收到消息: " + message +
                ", partition=" + partition +
                ", offset=" + offset +
                ", key=" + key);
    }
    
    /**
     * 订单Topic消费
     */
    @KafkaListener(topics = "order-topic", groupId = "order-group")
    public void consumeOrder(String message) {
        System.out.println("[OrderConsumer] 处理订单: " + message);
        // 模拟订单处理
        processOrder(message);
    }
    
    /**
     * 日志Topic消费（批量消费示例）
     */
    @KafkaListener(topics = "log-topic", groupId = "log-group")
    public void consumeLog(String message) {
        System.out.println("[LogConsumer] 记录日志: " + message);
    }
    
    /**
     * 多Topic监听
     */
    @KafkaListener(topics = {"demo-topic", "order-topic"}, groupId = "multi-group")
    public void consumeMultipleTopics(String message) {
        System.out.println("[MultiConsumer] 收到消息: " + message);
    }
    
    private void processOrder(String message) {
        try {
            // 模拟处理时间
            Thread.sleep(100);
            System.out.println("[OrderConsumer] 订单处理完成");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
