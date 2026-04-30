package com.opendemo.java.ddd;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Order extends AggregateRoot {
    private final OrderId id;
    private final CustomerId customerId;
    private final List<OrderItem> orderLines;
    private Address shippingAddress;
    private OrderStatus status;

    public Order(OrderId id, CustomerId customerId) {
        this.id = id;
        this.customerId = customerId;
        this.orderLines = new ArrayList<>();
        this.status = OrderStatus.DRAFT;
    }

    public void addProduct(ProductId productId, int quantity, Money price) {
        if (status != OrderStatus.DRAFT) {
            throw new IllegalStateException("Cannot modify submitted order");
        }
        int lineNumber = orderLines.size() + 1;
        orderLines.add(new OrderItem(lineNumber, productId, quantity, price));
    }

    public void removeProduct(ProductId productId) {
        if (status != OrderStatus.DRAFT) {
            throw new IllegalStateException("Cannot modify submitted order");
        }
        orderLines.removeIf(item -> item.getProductId().equals(productId));
    }

    public Money getTotal() {
        return orderLines.stream()
                .map(OrderItem::getSubtotal)
                .reduce(Money.ZERO, Money::add);
    }

    public void submit() {
        if (orderLines.isEmpty()) {
            throw new IllegalStateException("Cannot submit empty order");
        }
        this.status = OrderStatus.SUBMITTED;
        registerEvent(new OrderSubmittedEvent(id));
    }

    public void confirm() {
        if (status != OrderStatus.SUBMITTED) {
            throw new IllegalStateException("Only submitted orders can be confirmed");
        }
        this.status = OrderStatus.CONFIRMED;
    }

    public void cancel() {
        if (status == OrderStatus.SHIPPED || status == OrderStatus.DELIVERED) {
            throw new IllegalStateException("Cannot cancel shipped or delivered order");
        }
        this.status = OrderStatus.CANCELLED;
    }

    public void setShippingAddress(Address address) {
        this.shippingAddress = address;
    }

    public OrderId getId() {
        return id;
    }

    public CustomerId getCustomerId() {
        return customerId;
    }

    public List<OrderItem> getOrderLines() {
        return Collections.unmodifiableList(orderLines);
    }

    public Address getShippingAddress() {
        return shippingAddress;
    }

    public OrderStatus getStatus() {
        return status;
    }
}
