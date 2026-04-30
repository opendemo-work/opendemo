package com.example.demo.health;

import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.stereotype.Component;

import java.util.concurrent.ThreadLocalRandom;

@Component
public class CustomHealthIndicator implements HealthIndicator {

    @Override
    public Health health() {
        int errorCode = checkExternalService();
        if (errorCode != 0) {
            return Health.down()
                    .withDetail("errorCode", errorCode)
                    .withDetail("description", "外部服务不可用")
                    .build();
        }
        return Health.up()
                .withDetail("externalService", "可用")
                .withDetail("responseTime", ThreadLocalRandom.current().nextInt(10, 100) + "ms")
                .build();
    }

    private int checkExternalService() {
        return ThreadLocalRandom.current().nextBoolean() ? 0 : 503;
    }
}
