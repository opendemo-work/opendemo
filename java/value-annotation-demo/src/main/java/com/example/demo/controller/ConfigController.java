package com.example.demo.controller;

import com.example.demo.service.ConfigService;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/config")
public class ConfigController {

    private final ConfigService configService;

    public ConfigController(ConfigService configService) {
        this.configService = configService;
    }

    @GetMapping("/basic")
    public ResponseEntity<Map<String, Object>> getBasicConfig() {
        return ResponseEntity.ok(configService.getBasicConfig());
    }

    @GetMapping("/numeric")
    public ResponseEntity<Map<String, Object>> getNumericConfig() {
        return ResponseEntity.ok(configService.getNumericConfig());
    }

    @GetMapping("/spel")
    public ResponseEntity<Map<String, Object>> getSpelConfig() {
        return ResponseEntity.ok(configService.getSpelConfig());
    }

    @GetMapping("/collections")
    public ResponseEntity<Map<String, Object>> getCollectionConfig() {
        return ResponseEntity.ok(configService.getCollectionConfig());
    }

    @GetMapping("/all")
    public ResponseEntity<Map<String, Object>> getAllConfig() {
        return ResponseEntity.ok(configService.getAllConfig());
    }
}
