package com.example.configclient.controller;

import com.example.configclient.service.ConfigService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.core.env.Environment;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
@RefreshScope
public class ConfigClientController {

    @Autowired
    private ConfigService configService;

    @Autowired
    private Environment environment;

    @GetMapping("/config")
    public Map<String, Object> getConfig() {
        Map<String, Object> config = new HashMap<>();
        config.put("appName", configService.getAppName());
        config.put("appVersion", configService.getAppVersion());
        config.put("maxItems", configService.getMaxItems());
        config.put("timeoutSeconds", configService.getTimeoutSeconds());
        config.put("defaultCurrency", configService.getDefaultCurrency());
        config.put("activeProfiles", String.join(",", environment.getActiveProfiles()));
        return config;
    }

    @GetMapping("/config/order")
    public Map<String, Object> getOrderConfig() {
        Map<String, Object> config = new HashMap<>();
        config.put("maxItems", configService.getMaxItems());
        config.put("timeoutSeconds", configService.getTimeoutSeconds());
        config.put("defaultCurrency", configService.getDefaultCurrency());
        config.put("dbHost", configService.getDatabaseHost());
        config.put("dbPort", configService.getDatabasePort());
        config.put("dbName", configService.getDatabaseName());
        return config;
    }
}
