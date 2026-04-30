package com.example.demo.service;

import com.example.demo.model.EmailMessage;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Service
public class NotificationService {

    private static final Logger log = LoggerFactory.getLogger(NotificationService.class);

    public void processEmail(EmailMessage message) {
        log.info("Processing email: to={}, subject={}", message.getTo(), message.getSubject());
        log.info("Email body: {}", message.getBody());
        log.info("Email sent successfully from: {}", message.getFrom());
    }

    public void processNotification(String message) {
        log.info("Processing notification: {}", message);
    }

    public void processTopicMessage(String subscriberId, EmailMessage message) {
        log.info("[{}] Received broadcast: to={}, subject={}", subscriberId, message.getTo(), message.getSubject());
        log.info("[{}] Broadcast content: {}", subscriberId, message.getBody());
    }
}
