package com.opendemo.java.ddd;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

public class InMemoryOrderRepository implements OrderRepository {
    private final Map<String, Order> store = new ConcurrentHashMap<>();

    @Override
    public Optional<Order> findById(OrderId id) {
        return Optional.ofNullable(store.get(id.getValue()));
    }

    @Override
    public void save(Order order) {
        store.put(order.getId().getValue(), order);
    }

    @Override
    public List<Order> findByCustomerId(CustomerId customerId) {
        return store.values().stream()
                .filter(o -> o.getCustomerId().equals(customerId))
                .collect(Collectors.toList());
    }

    @Override
    public void delete(Order order) {
        store.remove(order.getId().getValue());
    }
}
