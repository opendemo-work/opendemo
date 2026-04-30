package com.opendemo.java.ddd;

import java.util.List;
import java.util.Optional;

public interface OrderRepository {
    Optional<Order> findById(OrderId id);
    void save(Order order);
    List<Order> findByCustomerId(CustomerId customerId);
    void delete(Order order);
}
