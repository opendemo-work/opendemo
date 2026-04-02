package com.example.demo.model;

import java.time.LocalDateTime;

/**
 * 聊天消息
 */
public class ChatMessage {
    
    private String type;      // JOIN, CHAT, LEAVE
    private String sender;    // 发送者
    private String content;   // 内容
    private LocalDateTime timestamp;
    
    public ChatMessage() {
        this.timestamp = LocalDateTime.now();
    }
    
    public ChatMessage(String type, String sender, String content) {
        this.type = type;
        this.sender = sender;
        this.content = content;
        this.timestamp = LocalDateTime.now();
    }
    
    // Getters and Setters
    public String getType() {
        return type;
    }
    
    public void setType(String type) {
        this.type = type;
    }
    
    public String getSender() {
        return sender;
    }
    
    public void setSender(String sender) {
        this.sender = sender;
    }
    
    public String getContent() {
        return content;
    }
    
    public void setContent(String content) {
        this.content = content;
    }
    
    public LocalDateTime getTimestamp() {
        return timestamp;
    }
    
    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }
    
    /**
     * 创建加入消息
     */
    public static ChatMessage join(String sender) {
        return new ChatMessage("JOIN", sender, sender + " 加入了聊天室");
    }
    
    /**
     * 创建离开消息
     */
    public static ChatMessage leave(String sender) {
        return new ChatMessage("LEAVE", sender, sender + " 离开了聊天室");
    }
    
    /**
     * 创建聊天消息
     */
    public static ChatMessage chat(String sender, String content) {
        return new ChatMessage("CHAT", sender, content);
    }
    
    @Override
    public String toString() {
        return "ChatMessage{" +
                "type='" + type + '\'' +
                ", sender='" + sender + '\'' +
                ", content='" + content + '\'' +
                ", timestamp=" + timestamp +
                '}';
    }
}
