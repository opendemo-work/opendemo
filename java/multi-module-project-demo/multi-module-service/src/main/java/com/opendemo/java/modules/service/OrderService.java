package com.opendemo.java.modules.service;

import com.opendemo.java.modules.common.exception.BusinessException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.atomic.AtomicLong;

public class OrderService {

    private static final Logger logger = LoggerFactory.getLogger(OrderService.class);

    private final List<OrderInfo> orders = new ArrayList<>();
    private final AtomicLong idGenerator = new AtomicLong(1001);

    public OrderInfo createOrder(Long userId, String productName, int quantity, double price) {
        if (userId == null) {
            throw new BusinessException("INVALID_PARAM", "用户ID不能为空");
        }
        if (quantity <= 0) {
            throw new BusinessException("INVALID_PARAM", "数量必须大于0");
        }

        OrderInfo order = new OrderInfo(
                idGenerator.getAndIncrement(),
                userId,
                productName,
                quantity,
                price,
                quantity * price
        );
        orders.add(order);
        logger.info("创建订单: {}", order);
        return order;
    }

    public List<OrderInfo> getOrdersByUserId(Long userId) {
        List<OrderInfo> result = new ArrayList<>();
        for (OrderInfo order : orders) {
            if (order.getUserId().equals(userId)) {
                result.add(order);
            }
        }
        return result;
    }

    public List<OrderInfo> getAllOrders() {
        return Collections.unmodifiableList(orders);
    }

    public double getTotalRevenue() {
        return orders.stream()
                .mapToDouble(OrderInfo::getTotalAmount)
                .sum();
    }

    public static class OrderInfo {
        private final Long id;
        private final Long userId;
        private final String productName;
        private final int quantity;
        private final double unitPrice;
        private final double totalAmount;

        public OrderInfo(Long id, Long userId, String productName, int quantity, double unitPrice, double totalAmount) {
            this.id = id;
            this.userId = userId;
            this.productName = productName;
            this.quantity = quantity;
            this.unitPrice = unitPrice;
            this.totalAmount = totalAmount;
        }

        public Long getId() { return id; }
        public Long getUserId() { return userId; }
        public String getProductName() { return productName; }
        public int getQuantity() { return quantity; }
        public double getUnitPrice() { return unitPrice; }
        public double getTotalAmount() { return totalAmount; }

        @Override
        public String toString() {
            return "OrderInfo{id=" + id + ", userId=" + userId + ", product='" + productName + "', total=" + totalAmount + "}";
        }
    }
}
