package com.example.demo.controller;

import com.example.demo.dto.OrderRequest;
import com.example.demo.dto.OrderResponse;
import com.example.demo.service.OrderService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/orders")
public class OrderController {

    private static final Logger log = LoggerFactory.getLogger(OrderController.class);

    @Autowired
    private OrderService orderService;

    @PostMapping
    public OrderResponse createOrder(@RequestBody OrderRequest request) {
        log.info("Received order request: productId={}, quantity={}", request.getProductId(), request.getQuantity());
        OrderResponse response = orderService.processOrder(request);
        log.info("Order processed: orderId={}, status={}", response.getOrderId(), response.getStatus());
        return response;
    }
}
