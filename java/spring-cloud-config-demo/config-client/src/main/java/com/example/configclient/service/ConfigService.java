package com.example.configclient.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.stereotype.Service;

@Service
@RefreshScope
public class ConfigService {

    @Value("${app.name:unknown}")
    private String appName;

    @Value("${app.version:unknown}")
    private String appVersion;

    @Value("${order.max-items:50}")
    private int maxItems;

    @Value("${order.timeout-seconds:10}")
    private int timeoutSeconds;

    @Value("${order.default-currency:USD}")
    private String defaultCurrency;

    @Value("${database.host:localhost}")
    private String databaseHost;

    @Value("${database.port:3306}")
    private int databasePort;

    @Value("${database.name:default_db}")
    private String databaseName;

    public String getAppName() {
        return appName;
    }

    public String getAppVersion() {
        return appVersion;
    }

    public int getMaxItems() {
        return maxItems;
    }

    public int getTimeoutSeconds() {
        return timeoutSeconds;
    }

    public String getDefaultCurrency() {
        return defaultCurrency;
    }

    public String getDatabaseHost() {
        return databaseHost;
    }

    public int getDatabasePort() {
        return databasePort;
    }

    public String getDatabaseName() {
        return databaseName;
    }
}
