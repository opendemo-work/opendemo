package com.opendemo.java.ddd;

public class OrderSubmittedEvent extends DomainEvent {
    private final OrderId orderId;

    public OrderSubmittedEvent(OrderId orderId) {
        super("ORD-SUB-" + orderId.getValue());
        this.orderId = orderId;
    }

    public OrderId getOrderId() {
        return orderId;
    }
}
