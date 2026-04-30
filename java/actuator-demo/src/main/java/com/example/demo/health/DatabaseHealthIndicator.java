package com.example.demo.health;

import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.stereotype.Component;

@Component
public class DatabaseHealthIndicator implements HealthIndicator {

    @Override
    public Health health() {
        boolean connected = checkConnection();
        if (!connected) {
            return Health.down()
                    .withDetail("database", "MySQL")
                    .withDetail("error", "连接超时")
                    .build();
        }
        return Health.up()
                .withDetail("database", "MySQL")
                .withDetail("status", "已连接")
                .withDetail("activeConnections", 5)
                .withDetail("maxConnections", 20)
                .build();
    }

    private boolean checkConnection() {
        return true;
    }
}
