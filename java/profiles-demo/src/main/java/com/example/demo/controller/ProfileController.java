package com.example.demo.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
public class ProfileController {
    
    @Value("${app.name}")
    private String appName;
    
    @Value("${app.env}")
    private String env;
    
    @GetMapping("/info")
    public Map<String, String> info() {
        Map<String, String> info = new HashMap<>();
        info.put("appName", appName);
        info.put("env", env);
        return info;
    }
}
