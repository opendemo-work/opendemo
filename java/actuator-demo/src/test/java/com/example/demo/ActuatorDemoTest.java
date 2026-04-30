package com.example.demo;

import com.example.demo.health.CustomHealthIndicator;
import com.example.demo.health.DatabaseHealthIndicator;
import com.example.demo.endpoint.CustomActuatorEndpoint;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class ActuatorDemoTest {

    @Test
    void testCustomHealthIndicator() {
        CustomHealthIndicator indicator = new CustomHealthIndicator();
        assertNotNull(indicator.health());
        assertNotNull(indicator.health().getStatus());
    }

    @Test
    void testDatabaseHealthIndicator() {
        DatabaseHealthIndicator indicator = new DatabaseHealthIndicator();
        assertNotNull(indicator.health());
        assertEquals("UP", indicator.health().getStatus().getCode());
        Map<String, Object> details = indicator.health().getDetails();
        assertTrue(details.containsKey("database"));
        assertEquals("MySQL", details.get("database"));
    }

    @Test
    void testCustomEndpoint() {
        CustomActuatorEndpoint endpoint = new CustomActuatorEndpoint();
        Map<String, Object> status = endpoint.appStatus();
        assertNotNull(status);
        assertEquals("Actuator Demo", status.get("application"));
        assertEquals("1.0.0", status.get("version"));
        assertEquals("RUNNING", status.get("status"));
        assertTrue(status.containsKey("requestCount"));
        assertTrue(status.containsKey("lastAccessTime"));
    }

    @Test
    void testCustomEndpointCounterIncrement() {
        CustomActuatorEndpoint endpoint = new CustomActuatorEndpoint();
        endpoint.appStatus();
        endpoint.appStatus();
        Map<String, Object> status = endpoint.appStatus();
        assertEquals(3L, status.get("requestCount"));
    }

    @Test
    void testCustomEndpointReset() {
        CustomActuatorEndpoint endpoint = new CustomActuatorEndpoint();
        endpoint.appStatus();
        endpoint.appStatus();
        endpoint.resetCounter();
        Map<String, Object> status = endpoint.appStatus();
        assertEquals(1L, status.get("requestCount"));
    }

    @Test
    void testDatabaseHealthDetails() {
        DatabaseHealthIndicator indicator = new DatabaseHealthIndicator();
        Map<String, Object> details = indicator.health().getDetails();
        assertTrue(details.containsKey("activeConnections"));
        assertTrue(details.containsKey("maxConnections"));
        assertEquals(5, details.get("activeConnections"));
        assertEquals(20, details.get("maxConnections"));
    }
}
