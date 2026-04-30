package com.example.demo.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class FeatureToggleService {

    @Autowired
    private Environment environment;

    @Value("${feature.swagger.enabled:false}")
    private boolean swaggerEnabled;

    @Value("${feature.rate-limit.enabled:true}")
    private boolean rateLimitEnabled;

    @Value("${feature.cache.type:local}")
    private String cacheType;

    public Map<String, Object> getFeatureStatus() {
        Map<String, Object> status = new HashMap<>();
        status.put("swaggerEnabled", swaggerEnabled);
        status.put("rateLimitEnabled", rateLimitEnabled);
        status.put("cacheType", cacheType);
        status.put("activeProfiles", String.join(",", environment.getActiveProfiles()));
        return status;
    }

    public boolean isFeatureEnabled(String featureName) {
        return environment.getProperty("feature." + featureName + ".enabled", Boolean.class, false);
    }

    public List<String> getActiveFeatures() {
        List<String> features = new ArrayList<>();
        if (swaggerEnabled) features.add("swagger");
        if (rateLimitEnabled) features.add("rate-limit");
        features.add("cache:" + cacheType);
        return features;
    }

    public boolean isSwaggerEnabled() {
        return swaggerEnabled;
    }

    public boolean isRateLimitEnabled() {
        return rateLimitEnabled;
    }

    public String getCacheType() {
        return cacheType;
    }
}
