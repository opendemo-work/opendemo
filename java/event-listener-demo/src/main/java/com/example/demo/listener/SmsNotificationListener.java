package com.example.demo.listener;

import com.example.demo.event.UserRegisteredEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

@Component
public class SmsNotificationListener {

    private static final Logger logger = LoggerFactory.getLogger(SmsNotificationListener.class);

    @Async
    @EventListener
    public void handleUserRegistered(UserRegisteredEvent event) {
        logger.info("[短信通知] 发送注册成功短信给: {}", event.getUsername());
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        logger.info("[短信通知] 短信发送完成: {}", event.getUsername());
    }
}
