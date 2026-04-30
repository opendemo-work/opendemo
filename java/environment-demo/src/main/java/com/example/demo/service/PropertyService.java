package com.example.demo.service;

import com.example.demo.config.AppConfig;

import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

@Service
public class PropertyService {

    private final AppConfig appConfig;

    public PropertyService(AppConfig appConfig) {
        this.appConfig = appConfig;
    }

    public Map<String, Object> getAllAppProperties() {
        Map<String, Object> props = new HashMap<>();
        props.put("appName", appConfig.getAppName());
        props.put("appVersion", appConfig.getAppVersion());
        props.put("featureEnabled", appConfig.isFeatureEnabled());
        return props;
    }

    public Map<String, Object> getEnvironmentInfo() {
        Map<String, Object> info = new HashMap<>();
        info.put("activeProfiles", appConfig.getActiveProfiles());
        info.put("defaultProfiles", appConfig.getDefaultProfiles());
        info.put("javaVersion", appConfig.getProperty("java.version"));
        info.put("osName", appConfig.getProperty("os.name"));
        info.put("userDir", appConfig.getProperty("user.dir"));
        info.put("serverPort", appConfig.getProperty("server.port", "8080"));
        return info;
    }

    public String getPropertyByKey(String key) {
        return appConfig.getProperty(key);
    }

    public String getPropertyByKey(String key, String defaultValue) {
        return appConfig.getProperty(key, defaultValue);
    }

    public boolean hasProperty(String key) {
        return appConfig.containsProperty(key);
    }
}
