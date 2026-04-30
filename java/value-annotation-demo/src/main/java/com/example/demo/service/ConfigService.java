package com.example.demo.service;

import com.example.demo.config.AppProperties;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@Service
public class ConfigService {

    private final AppProperties appProperties;

    @Value("${app.retry.max-attempts:3}")
    private int maxRetryAttempts;

    @Value("${app.retry.delay:1000}")
    private long retryDelay;

    public ConfigService(AppProperties appProperties) {
        this.appProperties = appProperties;
    }

    public Map<String, Object> getBasicConfig() {
        Map<String, Object> config = new LinkedHashMap<>();
        config.put("literalValue", appProperties.getLiteralValue());
        config.put("appName", appProperties.getAppName());
        config.put("appVersion", appProperties.getAppVersion());
        config.put("appDescription", appProperties.getAppDescription());
        return config;
    }

    public Map<String, Object> getNumericConfig() {
        Map<String, Object> config = new LinkedHashMap<>();
        config.put("timeout", appProperties.getTimeout());
        config.put("featureEnabled", appProperties.isFeatureEnabled());
        config.put("maxRetryAttempts", maxRetryAttempts);
        config.put("retryDelay", retryDelay);
        return config;
    }

    public Map<String, Object> getSpelConfig() {
        Map<String, Object> config = new LinkedHashMap<>();
        config.put("randomValue", appProperties.getRandomValue());
        config.put("javaVersion", appProperties.getJavaVersion());
        config.put("pathCheck", appProperties.getPathCheck());
        return config;
    }

    public Map<String, Object> getCollectionConfig() {
        Map<String, Object> config = new HashMap<>();
        config.put("supportedLocales", appProperties.getSupportedLocales());
        config.put("servers", appProperties.getServers());
        return config;
    }

    public Map<String, Object> getAllConfig() {
        Map<String, Object> all = new LinkedHashMap<>();
        all.put("basic", getBasicConfig());
        all.put("numeric", getNumericConfig());
        all.put("spel", getSpelConfig());
        all.put("collections", getCollectionConfig());
        return all;
    }
}
