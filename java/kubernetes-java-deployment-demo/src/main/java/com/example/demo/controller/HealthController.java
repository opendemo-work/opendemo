package com.example.demo.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.LinkedHashMap;
import java.util.Map;

@RestController
public class HealthController {

    @Value("${spring.application.name:kubernetes-demo}")
    private String applicationName;

    @GetMapping("/health")
    public Map<String, Object> health() {
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("status", "UP");
        result.put("application", applicationName);
        result.put("timestamp", LocalDateTime.now().toString());
        return result;
    }

    @GetMapping("/readiness")
    public Map<String, Object> readiness() {
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("status", "READY");
        result.put("message", "应用已就绪，可以接收流量");
        return result;
    }

    @GetMapping("/liveness")
    public Map<String, Object> liveness() {
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("status", "ALIVE");
        result.put("message", "应用运行正常");
        return result;
    }
}
