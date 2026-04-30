package com.example.demo.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.env.Environment;

@Configuration
public class AppConfig {

    private final Environment environment;

    @Value("${app.name:default-app}")
    private String appName;

    @Value("${app.version:1.0.0}")
    private String appVersion;

    @Value("${app.feature.enabled:false}")
    private boolean featureEnabled;

    public AppConfig(Environment environment) {
        this.environment = environment;
    }

    public String getAppName() {
        return appName;
    }

    public String getAppVersion() {
        return appVersion;
    }

    public boolean isFeatureEnabled() {
        return featureEnabled;
    }

    public String getProperty(String key) {
        return environment.getProperty(key);
    }

    public String getProperty(String key, String defaultValue) {
        return environment.getProperty(key, defaultValue);
    }

    public String[] getActiveProfiles() {
        return environment.getActiveProfiles();
    }

    public String getDefaultProfiles() {
        return String.join(",", environment.getDefaultProfiles());
    }

    public boolean containsProperty(String key) {
        return environment.containsProperty(key);
    }

    public Environment getEnvironment() {
        return environment;
    }
}
