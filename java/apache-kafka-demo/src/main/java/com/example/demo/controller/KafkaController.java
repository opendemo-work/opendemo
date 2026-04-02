package com.example.demo.controller;

import com.example.demo.model.KafkaMessage;
import com.example.demo.producer.KafkaMessageProducer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

/**
 * Kafka消息控制器
 */
@RestController
@RequestMapping("/api/kafka")
public class KafkaController {
    
    @Autowired
    private KafkaMessageProducer producer;
    
    /**
     * 发送简单消息
     */
    @PostMapping("/send")
    public Map<String, String> sendMessage(
            @RequestParam String topic,
            @RequestParam String message) {
        
        producer.sendMessage(topic, message);
        
        Map<String, String> result = new HashMap<>();
        result.put("status", "success");
        result.put("topic", topic);
        result.put("message", message);
        return result;
    }
    
    /**
     * 发送消息对象
     */
    @PostMapping("/send/json")
    public Map<String, String> sendMessageJson(@RequestBody KafkaMessage message) {
        producer.sendMessage(message);
        
        Map<String, String> result = new HashMap<>();
        result.put("status", "success");
        result.put("id", message.getId());
        return result;
    }
    
    /**
     * 批量发送消息
     */
    @PostMapping("/send/batch")
    public Map<String, Object> sendBatch(
            @RequestParam String topic,
            @RequestParam(defaultValue = "10") int count) {
        
        for (int i = 0; i < count; i++) {
            String message = "批量消息-" + (i + 1);
            producer.sendMessage(topic, message);
        }
        
        Map<String, Object> result = new HashMap<>();
        result.put("status", "success");
        result.put("topic", topic);
        result.put("sentCount", count);
        return result;
    }
    
    /**
     * 发送带Key的消息（保证分区顺序）
     */
    @PostMapping("/send/keyed")
    public Map<String, String> sendWithKey(
            @RequestParam String topic,
            @RequestParam String key,
            @RequestParam String message) {
        
        producer.sendMessageWithKey(topic, key, message);
        
        Map<String, String> result = new HashMap<>();
        result.put("status", "success");
        result.put("topic", topic);
        result.put("key", key);
        return result;
    }
    
    /**
     * 快速测试接口
     */
    @GetMapping("/test/{topic}")
    public Map<String, String> quickTest(@PathVariable String topic) {
        String message = "测试消息 - " + System.currentTimeMillis();
        producer.sendMessage(topic, message);
        
        Map<String, String> result = new HashMap<>();
        result.put("status", "sent");
        result.put("topic", topic);
        result.put("message", message);
        return result;
    }
}
