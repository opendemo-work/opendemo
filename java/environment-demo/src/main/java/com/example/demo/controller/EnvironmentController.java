package com.example.demo.controller;

import com.example.demo.service.PropertyService;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/env")
public class EnvironmentController {

    private final PropertyService propertyService;

    public EnvironmentController(PropertyService propertyService) {
        this.propertyService = propertyService;
    }

    @GetMapping("/app-properties")
    public ResponseEntity<Map<String, Object>> getAppProperties() {
        return ResponseEntity.ok(propertyService.getAllAppProperties());
    }

    @GetMapping("/system-info")
    public ResponseEntity<Map<String, Object>> getSystemInfo() {
        return ResponseEntity.ok(propertyService.getEnvironmentInfo());
    }

    @GetMapping("/property")
    public ResponseEntity<Map<String, String>> getProperty(@RequestParam String key,
                                                            @RequestParam(required = false) String defaultValue) {
        Map<String, String> result = new HashMap<>();
        if (defaultValue != null) {
            result.put(key, propertyService.getPropertyByKey(key, defaultValue));
        } else {
            result.put(key, propertyService.getPropertyByKey(key));
        }
        return ResponseEntity.ok(result);
    }

    @GetMapping("/has-property")
    public ResponseEntity<Map<String, Object>> hasProperty(@RequestParam String key) {
        Map<String, Object> result = new HashMap<>();
        result.put("key", key);
        result.put("exists", propertyService.hasProperty(key));
        return ResponseEntity.ok(result);
    }
}
