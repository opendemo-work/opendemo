package com.opendemo.java.ddd;

public class OrderService {
    private final OrderRepository orderRepository;

    public OrderService(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    public Order createOrder(OrderId orderId, CustomerId customerId) {
        Order order = new Order(orderId, customerId);
        orderRepository.save(order);
        return order;
    }

    public Order addProductToOrder(OrderId orderId, ProductId productId, int quantity, Money price) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));
        order.addProduct(productId, quantity, price);
        orderRepository.save(order);
        return order;
    }

    public Order submitOrder(OrderId orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));
        order.submit();
        orderRepository.save(order);
        return order;
    }

    public Order confirmOrder(OrderId orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));
        order.confirm();
        orderRepository.save(order);
        return order;
    }

    public Order cancelOrder(OrderId orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));
        order.cancel();
        orderRepository.save(order);
        return order;
    }
}
