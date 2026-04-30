package com.example.demo.service;

import com.example.demo.dto.OrderRequest;
import com.example.demo.dto.OrderResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@Service
public class OrderService {

    private static final Logger log = LoggerFactory.getLogger(OrderService.class);

    @Autowired
    private PaymentService paymentService;

    @Autowired
    private InventoryService inventoryService;

    public OrderResponse processOrder(OrderRequest request) {
        log.info("Processing order for product: {}", request.getProductId());

        Map<String, Object> inventoryResult = inventoryService.checkInventory(
                request.getProductId(), request.getQuantity());

        if (!(Boolean) inventoryResult.get("available")) {
            log.warn("Product not available: {}", request.getProductId());
            return new OrderResponse(null, request.getProductId(), "OUT_OF_STOCK", null);
        }

        String orderId = UUID.randomUUID().toString();

        Map<String, Object> paymentResult = paymentService.processPayment(
                orderId, request.getProductId(), request.getAmount());

        log.info("Order completed: orderId={}", orderId);

        return new OrderResponse(
                orderId,
                request.getProductId(),
                "COMPLETED",
                (String) paymentResult.get("paymentId"));
    }
}
