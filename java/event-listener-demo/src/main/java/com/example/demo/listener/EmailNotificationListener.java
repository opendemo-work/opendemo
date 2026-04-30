package com.example.demo.listener;

import com.example.demo.event.UserRegisteredEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;

@Component
public class EmailNotificationListener {

    private static final Logger logger = LoggerFactory.getLogger(EmailNotificationListener.class);

    @EventListener
    public void handleUserRegistered(UserRegisteredEvent event) {
        logger.info("[邮件通知] 发送欢迎邮件给: {} ({})", event.getUsername(), event.getEmail());
    }
}
