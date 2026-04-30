package com.example.demo.endpoint;

import org.springframework.boot.actuate.endpoint.annotation.Endpoint;
import org.springframework.boot.actuate.endpoint.annotation.ReadOperation;
import org.springframework.boot.actuate.endpoint.annotation.WriteOperation;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;

@Endpoint(id = "appstatus")
@Component
public class CustomActuatorEndpoint {

    private final AtomicLong requestCount = new AtomicLong(0);
    private volatile LocalDateTime lastAccessTime = LocalDateTime.now();

    @ReadOperation
    public Map<String, Object> appStatus() {
        requestCount.incrementAndGet();
        lastAccessTime = LocalDateTime.now();
        Map<String, Object> status = new HashMap<>();
        status.put("application", "Actuator Demo");
        status.put("version", "1.0.0");
        status.put("status", "RUNNING");
        status.put("uptime", getUptime());
        status.put("requestCount", requestCount.get());
        status.put("lastAccessTime", lastAccessTime.toString());
        status.put("timestamp", LocalDateTime.now().toString());
        return status;
    }

    @WriteOperation
    public void resetCounter() {
        requestCount.set(0);
    }

    private String getUptime() {
        long uptime = System.currentTimeMillis();
        long hours = (uptime / 3600000) % 24;
        long minutes = (uptime / 60000) % 60;
        return hours + "h " + minutes + "m";
    }
}
