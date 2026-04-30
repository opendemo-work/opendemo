package com.example.demo.producer;

import com.example.demo.model.EmailMessage;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jms.core.JmsTemplate;
import org.springframework.stereotype.Component;

@Component
public class MessageProducer {

    @Autowired
    private JmsTemplate jmsTemplate;

    @Autowired
    private JmsTemplate topicJmsTemplate;

    public void sendToQueue(String destination, EmailMessage message) {
        jmsTemplate.convertAndSend(destination, message);
    }

    public void sendToTopic(String destination, EmailMessage message) {
        topicJmsTemplate.convertAndSend(destination, message);
    }

    public void sendTextToQueue(String destination, String text) {
        jmsTemplate.convertAndSend(destination, text);
    }
}
