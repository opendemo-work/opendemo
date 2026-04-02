package com.example.demo.producer;

import com.example.demo.model.KafkaMessage;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.stereotype.Service;
import org.springframework.util.concurrent.ListenableFuture;
import org.springframework.util.concurrent.ListenableFutureCallback;

import java.util.UUID;

/**
 * Kafka消息生产者
 */
@Service
public class KafkaMessageProducer {
    
    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;
    
    /**
     * 发送消息到指定Topic
     * 
     * @param topic 目标Topic
     * @param message 消息内容
     */
    public void sendMessage(String topic, String message) {
        String key = UUID.randomUUID().toString();
        
        ListenableFuture<SendResult<String, String>> future = 
            kafkaTemplate.send(topic, key, message);
        
        future.addCallback(new ListenableFutureCallback<>() {
            @Override
            public void onSuccess(SendResult<String, String> result) {
                System.out.println("[Producer] 消息发送成功: " + 
                    "topic=" + result.getRecordMetadata().topic() +
                    ", partition=" + result.getRecordMetadata().partition() +
                    ", offset=" + result.getRecordMetadata().offset());
            }
            
            @Override
            public void onFailure(Throwable ex) {
                System.err.println("[Producer] 消息发送失败: " + ex.getMessage());
            }
        });
    }
    
    /**
     * 发送消息（带Key，保证分区顺序）
     */
    public void sendMessageWithKey(String topic, String key, String message) {
        kafkaTemplate.send(topic, key, message);
        System.out.println("[Producer] 发送消息到 " + topic + ", key=" + key);
    }
    
    /**
     * 发送消息对象
     */
    public void sendMessage(KafkaMessage message) {
        if (message.getId() == null) {
            message.setId(UUID.randomUUID().toString());
        }
        
        String payload = String.format("[%s] %s", message.getId(), message.getMessage());
        sendMessage(message.getTopic(), payload);
    }
}
