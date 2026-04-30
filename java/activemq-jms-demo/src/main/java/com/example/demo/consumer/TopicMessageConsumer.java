package com.example.demo.consumer;

import com.example.demo.model.EmailMessage;
import com.example.demo.service.NotificationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jms.annotation.JmsListener;
import org.springframework.stereotype.Component;

@Component
public class TopicMessageConsumer {

    @Autowired
    private NotificationService notificationService;

    @JmsListener(destination = "${app.topic.broadcast}", containerFactory = "topicListenerFactory", subscription = "subscriber-one")
    public void receiveBroadcastOne(EmailMessage message) {
        notificationService.processTopicMessage("subscriber-one", message);
    }

    @JmsListener(destination = "${app.topic.broadcast}", containerFactory = "topicListenerFactory", subscription = "subscriber-two")
    public void receiveBroadcastTwo(EmailMessage message) {
        notificationService.processTopicMessage("subscriber-two", message);
    }
}
