package com.example.demo.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class AppProperties {

    @Value("literal-value")
    private String literalValue;

    @Value("${app.name}")
    private String appName;

    @Value("${app.version:0.0.1}")
    private String appVersion;

    @Value("${app.description:A default description}")
    private String appDescription;

    @Value("${app.timeout:5000}")
    private int timeout;

    @Value("${app.feature.enabled:true}")
    private boolean featureEnabled;

    @Value("${app.supported-locales:zh_CN,en_US}")
    private String[] supportedLocales;

    @Value("#{'${app.servers:localhost:8080}'.split(',')}")
    private List<String> servers;

    @Value("#{T(java.lang.Math).random() * 100}")
    private double randomValue;

    @Value("#{systemProperties['java.version']}")
    private String javaVersion;

    @Value("#{systemEnvironment['PATH'] != null ? 'PATH exists' : 'PATH not found'}")
    private String pathCheck;

    public String getLiteralValue() {
        return literalValue;
    }

    public String getAppName() {
        return appName;
    }

    public String getAppVersion() {
        return appVersion;
    }

    public String getAppDescription() {
        return appDescription;
    }

    public int getTimeout() {
        return timeout;
    }

    public boolean isFeatureEnabled() {
        return featureEnabled;
    }

    public String[] getSupportedLocales() {
        return supportedLocales;
    }

    public List<String> getServers() {
        return servers;
    }

    public double getRandomValue() {
        return randomValue;
    }

    public String getJavaVersion() {
        return javaVersion;
    }

    public String getPathCheck() {
        return pathCheck;
    }
}
