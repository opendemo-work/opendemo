package com.example.demo.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/payments")
public class PaymentController {

    private static final Logger log = LoggerFactory.getLogger(PaymentController.class);

    @PostMapping
    public Map<String, Object> processPayment(@RequestBody Map<String, Object> paymentRequest) {
        log.info("Processing payment: orderId={}, amount={}",
                paymentRequest.get("orderId"), paymentRequest.get("amount"));
        paymentRequest.put("paymentId", UUID.randomUUID().toString());
        paymentRequest.put("status", "COMPLETED");
        log.info("Payment completed: paymentId={}", paymentRequest.get("paymentId"));
        return paymentRequest;
    }
}
