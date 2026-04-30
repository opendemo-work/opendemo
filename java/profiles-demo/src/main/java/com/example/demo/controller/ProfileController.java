package com.example.demo.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.env.Environment;
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

    @Autowired
    private Environment environment;

    @Autowired(required = false)
    private String profileMessage;

    @GetMapping("/info")
    public Map<String, String> info() {
        Map<String, String> info = new HashMap<>();
        info.put("appName", appName);
        info.put("env", env);
        info.put("activeProfile", String.join(",", environment.getActiveProfiles()));
        if (profileMessage != null) {
            info.put("message", profileMessage);
        }
        return info;
    }

    @GetMapping("/info/beans")
    public Map<String, String> beans() {
        Map<String, String> result = new HashMap<>();
        result.put("appName", appName);
        result.put("env", env);
        result.put("activeProfile", String.join(",", environment.getActiveProfiles()));
        result.put("profileMessage", profileMessage != null ? profileMessage : "无 Profile Bean");
        return result;
    }
}
