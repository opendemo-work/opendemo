package com.example.demo.handler;

import com.example.demo.model.ChatMessage;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.io.IOException;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArraySet;

/**
 * 聊天WebSocket处理器
 * 
 * 处理WebSocket连接、消息和断开
 */
@Component
public class ChatWebSocketHandler extends TextWebSocketHandler {
    
    // 存储所有连接的会话
    private final Set<WebSocketSession> sessions = new CopyOnWriteArraySet<>();
    
    // 存储用户名和会话的映射
    private final Map<String, WebSocketSession> userSessions = new ConcurrentHashMap<>();
    
    private final ObjectMapper objectMapper = new ObjectMapper();
    
    /**
     * 连接建立后
     */
    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        sessions.add(session);
        System.out.println("[WebSocket] 新连接: " + session.getId() + 
                ", 当前连接数: " + sessions.size());
    }
    
    /**
     * 收到文本消息
     */
    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {
        String payload = message.getPayload();
        System.out.println("[WebSocket] 收到消息: " + payload);
        
        try {
            ChatMessage chatMessage = objectMapper.readValue(payload, ChatMessage.class);
            
            // 处理不同类型的消息
            switch (chatMessage.getType()) {
                case "JOIN":
                    handleJoin(session, chatMessage);
                    break;
                case "CHAT":
                    handleChat(session, chatMessage);
                    break;
                case "LEAVE":
                    handleLeave(session, chatMessage);
                    break;
                default:
                    System.out.println("[WebSocket] 未知消息类型: " + chatMessage.getType());
            }
        } catch (Exception e) {
            System.err.println("[WebSocket] 处理消息失败: " + e.getMessage());
            session.sendMessage(new TextMessage("错误: " + e.getMessage()));
        }
    }
    
    /**
     * 处理加入消息
     */
    private void handleJoin(WebSocketSession session, ChatMessage message) throws IOException {
        String username = message.getSender();
        userSessions.put(username, session);
        
        // 广播加入消息
        broadcast(ChatMessage.join(username));
        
        // 发送在线用户列表给新用户
        ChatMessage userListMsg = new ChatMessage("USER_LIST", "system", 
                String.join(",", userSessions.keySet()));
        session.sendMessage(new TextMessage(objectMapper.writeValueAsString(userListMsg)));
        
        System.out.println("[WebSocket] 用户加入: " + username);
    }
    
    /**
     * 处理聊天消息
     */
    private void handleChat(WebSocketSession session, ChatMessage message) throws IOException {
        // 广播消息给所有用户
        broadcast(message);
        System.out.println("[WebSocket] 聊天消息: " + message.getSender() + " -> " + message.getContent());
    }
    
    /**
     * 处理离开消息
     */
    private void handleLeave(WebSocketSession session, ChatMessage message) throws IOException {
        String username = message.getSender();
        userSessions.remove(username);
        
        // 广播离开消息
        broadcast(ChatMessage.leave(username));
        System.out.println("[WebSocket] 用户离开: " + username);
    }
    
    /**
     * 广播消息给所有连接
     */
    private void broadcast(ChatMessage message) throws IOException {
        String jsonMessage = objectMapper.writeValueAsString(message);
        TextMessage textMessage = new TextMessage(jsonMessage);
        
        for (WebSocketSession session : sessions) {
            if (session.isOpen()) {
                session.sendMessage(textMessage);
            }
        }
    }
    
    /**
     * 发送消息给特定用户
     */
    public void sendToUser(String username, ChatMessage message) throws IOException {
        WebSocketSession session = userSessions.get(username);
        if (session != null && session.isOpen()) {
            String jsonMessage = objectMapper.writeValueAsString(message);
            session.sendMessage(new TextMessage(jsonMessage));
        }
    }
    
    /**
     * 连接关闭后
     */
    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        sessions.remove(session);
        
        // 从用户映射中移除
        String usernameToRemove = null;
        for (Map.Entry<String, WebSocketSession> entry : userSessions.entrySet()) {
            if (entry.getValue().equals(session)) {
                usernameToRemove = entry.getKey();
                break;
            }
        }
        
        if (usernameToRemove != null) {
            userSessions.remove(usernameToRemove);
            broadcast(ChatMessage.leave(usernameToRemove));
            System.out.println("[WebSocket] 用户断开: " + usernameToRemove);
        }
        
        System.out.println("[WebSocket] 连接关闭: " + session.getId() + 
                ", 当前连接数: " + sessions.size());
    }
    
    /**
     * 传输错误时
     */
    @Override
    public void handleTransportError(WebSocketSession session, Throwable exception) throws Exception {
        System.err.println("[WebSocket] 传输错误: " + session.getId() + ", " + exception.getMessage());
    }
    
    /**
     * 获取在线用户数
     */
    public int getOnlineCount() {
        return userSessions.size();
    }
    
    /**
     * 获取在线用户列表
     */
    public Set<String> getOnlineUsers() {
        return userSessions.keySet();
    }
}
