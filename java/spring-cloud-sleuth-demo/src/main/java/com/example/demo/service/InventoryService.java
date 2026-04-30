package com.example.demo.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@Service
public class InventoryService {

    private static final Logger log = LoggerFactory.getLogger(InventoryService.class);

    @Autowired
    private RestTemplate restTemplate;

    public Map<String, Object> checkInventory(String productId, int quantity) {
        log.info("Checking inventory for product: {}, quantity: {}", productId, quantity);

        Map<String, Object> request = new HashMap<>();
        request.put("productId", productId);
        request.put("quantity", quantity);

        Map<String, Object> result = restTemplate.postForObject(
                "http://localhost:8080/inventory", request, Map.class);

        log.info("Inventory check completed for product: {}", productId);
        return result;
    }
}
