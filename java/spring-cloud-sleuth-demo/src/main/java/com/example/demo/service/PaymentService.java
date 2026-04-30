package com.example.demo.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@Service
public class PaymentService {

    private static final Logger log = LoggerFactory.getLogger(PaymentService.class);

    @Autowired
    private RestTemplate restTemplate;

    public Map<String, Object> processPayment(String orderId, String productId, double amount) {
        log.info("Initiating payment for order: {}, amount: {}", orderId, amount);

        Map<String, Object> request = new HashMap<>();
        request.put("orderId", orderId);
        request.put("productId", productId);
        request.put("amount", amount);

        Map<String, Object> result = restTemplate.postForObject(
                "http://localhost:8080/payments", request, Map.class);

        log.info("Payment processed for order: {}", orderId);
        return result;
    }
}
