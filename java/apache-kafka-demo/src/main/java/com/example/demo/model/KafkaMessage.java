package com.example.demo.model;

import java.time.LocalDateTime;

/**
 * Kafka消息实体
 */
public class KafkaMessage {
    
    private String id;
    private String message;
    private String topic;
    private LocalDateTime timestamp;
    
    public KafkaMessage() {
        this.timestamp = LocalDateTime.now();
    }
    
    public KafkaMessage(String id, String message, String topic) {
        this.id = id;
        this.message = message;
        this.topic = topic;
        this.timestamp = LocalDateTime.now();
    }
    
    public String getId() {
        return id;
    }
    
    public void setId(String id) {
        this.id = id;
    }
    
    public String getMessage() {
        return message;
    }
    
    public void setMessage(String message) {
        this.message = message;
    }
    
    public String getTopic() {
        return topic;
    }
    
    public void setTopic(String topic) {
        this.topic = topic;
    }
    
    public LocalDateTime getTimestamp() {
        return timestamp;
    }
    
    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }
    
    @Override
    public String toString() {
        return "KafkaMessage{" +
                "id='" + id + '\'' +
                ", message='" + message + '\'' +
                ", topic='" + topic + '\'' +
                ", timestamp=" + timestamp +
                '}';
    }
}
