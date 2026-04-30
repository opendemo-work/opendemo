package com.example.demo.consumer;

import com.example.demo.model.EmailMessage;
import com.example.demo.service.NotificationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jms.annotation.JmsListener;
import org.springframework.stereotype.Component;

@Component
public class MessageConsumer {

    @Autowired
    private NotificationService notificationService;

    @JmsListener(destination = "${app.queue.email}", containerFactory = "queueListenerFactory")
    public void receiveEmailMessage(EmailMessage message) {
        notificationService.processEmail(message);
    }

    @JmsListener(destination = "${app.queue.notification}", containerFactory = "queueListenerFactory")
    public void receiveNotification(String message) {
        notificationService.processNotification(message);
    }
}
