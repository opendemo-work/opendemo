package com.example.demo.service;

import com.example.demo.event.OrderCreatedEvent;
import com.example.demo.event.UserRegisteredEvent;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;

@Service
public class EventPublisherService {

    private final ApplicationEventPublisher eventPublisher;

    public EventPublisherService(ApplicationEventPublisher eventPublisher) {
        this.eventPublisher = eventPublisher;
    }

    public void publishUserRegistered(String username, String email) {
        UserRegisteredEvent event = new UserRegisteredEvent(this, username, email);
        eventPublisher.publishEvent(event);
    }

    public void publishOrderCreated(String orderId, String username, double amount) {
        OrderCreatedEvent event = new OrderCreatedEvent(this, orderId, username, amount);
        eventPublisher.publishEvent(event);
    }
}
