package com.example.demo.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/inventory")
public class InventoryController {

    private static final Logger log = LoggerFactory.getLogger(InventoryController.class);

    @PostMapping
    public Map<String, Object> checkInventory(@RequestBody Map<String, Object> request) {
        String productId = (String) request.get("productId");
        int quantity = (Integer) request.get("quantity");
        log.info("Checking inventory: productId={}, quantity={}", productId, quantity);
        request.put("available", true);
        request.put("stock", 1000);
        log.info("Inventory check completed: productId={}, available={}", productId, true);
        return request;
    }
}
