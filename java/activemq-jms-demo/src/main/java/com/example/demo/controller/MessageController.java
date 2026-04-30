package com.example.demo.controller;

import com.example.demo.model.EmailMessage;
import com.example.demo.producer.MessageProducer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/messages")
public class MessageController {

    @Autowired
    private MessageProducer messageProducer;

    @PostMapping("/queue/email")
    public ResponseEntity<Map<String, String>> sendEmailToQueue(@RequestBody EmailMessage message) {
        messageProducer.sendToQueue("email-queue", message);
        Map<String, String> response = new HashMap<>();
        response.put("status", "sent");
        response.put("destination", "email-queue");
        response.put("type", "queue");
        return ResponseEntity.ok(response);
    }

    @PostMapping("/queue/notification")
    public ResponseEntity<Map<String, String>> sendNotificationToQueue(@RequestBody Map<String, String> payload) {
        messageProducer.sendTextToQueue("notification-queue", payload.get("message"));
        Map<String, String> response = new HashMap<>();
        response.put("status", "sent");
        response.put("destination", "notification-queue");
        response.put("type", "queue");
        return ResponseEntity.ok(response);
    }

    @PostMapping("/topic/broadcast")
    public ResponseEntity<Map<String, String>> sendToTopic(@RequestBody EmailMessage message) {
        messageProducer.sendToTopic("broadcast-topic", message);
        Map<String, String> response = new HashMap<>();
        response.put("status", "sent");
        response.put("destination", "broadcast-topic");
        response.put("type", "topic");
        return ResponseEntity.ok(response);
    }
}
