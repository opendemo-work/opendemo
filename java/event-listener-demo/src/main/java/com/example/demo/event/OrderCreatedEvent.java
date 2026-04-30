package com.example.demo.event;

import org.springframework.context.ApplicationEvent;

public class OrderCreatedEvent extends ApplicationEvent {

    private final String orderId;
    private final String username;
    private final double amount;

    public OrderCreatedEvent(Object source, String orderId, String username, double amount) {
        super(source);
        this.orderId = orderId;
        this.username = username;
        this.amount = amount;
    }

    public String getOrderId() {
        return orderId;
    }

    public String getUsername() {
        return username;
    }

    public double getAmount() {
        return amount;
    }
}
