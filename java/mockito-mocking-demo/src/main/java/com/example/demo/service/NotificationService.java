package com.example.demo.service;

import com.example.demo.model.User;

/**
 * 通知服务接口
 */
public interface NotificationService {
    
    /**
     * 发送欢迎邮件
     * 
     * @param user 新用户
     * @return 是否发送成功
     */
    boolean sendWelcomeEmail(User user);
    
    /**
     * 发送密码重置邮件
     * 
     * @param email 目标邮箱
     * @param token 重置令牌
     * @return 是否发送成功
     */
    boolean sendPasswordResetEmail(String email, String token);
}
