package com.example.demo.controller;

import com.example.demo.handler.ChatWebSocketHandler;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

/**
 * 聊天控制器
 * 
 * 提供REST API查询在线状态
 */
@RestController
public class ChatController {
    
    @Autowired
    private ChatWebSocketHandler chatWebSocketHandler;
    
    /**
     * 获取在线人数
     */
    @GetMapping("/api/online/count")
    public ResponseEntity<Map<String, Object>> getOnlineCount() {
        Map<String, Object> result = new HashMap<>();
        result.put("count", chatWebSocketHandler.getOnlineCount());
        return ResponseEntity.ok(result);
    }
    
    /**
     * 获取在线用户列表
     */
    @GetMapping("/api/online/users")
    public ResponseEntity<Map<String, Object>> getOnlineUsers() {
        Set<String> users = chatWebSocketHandler.getOnlineUsers();
        Map<String, Object> result = new HashMap<>();
        result.put("users", users);
        result.put("count", users.size());
        return ResponseEntity.ok(result);
    }
}
