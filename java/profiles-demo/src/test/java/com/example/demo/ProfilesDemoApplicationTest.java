package com.example.demo;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.core.env.Environment;
import org.springframework.test.context.ActiveProfiles;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@ActiveProfiles("dev")
class ProfilesDemoApplicationTest {

    @Value("${app.name}")
    private String appName;

    @Value("${app.env}")
    private String env;

    @Autowired
    private Environment environment;

    @Test
    void contextLoads() {
    }

    @Test
    void testAppName() {
        assertEquals("DemoApp", appName);
    }

    @Test
    void testDevEnvironment() {
        assertEquals("development", env);
    }

    @Test
    void testActiveProfile() {
        String[] activeProfiles = environment.getActiveProfiles();
        assertTrue(activeProfiles.length > 0);
        assertTrue(java.util.Arrays.asList(activeProfiles).contains("dev"));
    }

    @Test
    void testServerPort() {
        String port = environment.getProperty("server.port");
        assertEquals("8080", port);
    }
}
