package com.example.demo;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class EurekaServerApplicationTest {

    @Test
    void testMainClassExists() {
        assertDoesNotThrow(() -> {
            Class<?> clazz = Class.forName("com.example.demo.EurekaServerApplication");
            assertNotNull(clazz);
        });
    }

    @Test
    void testEnableEurekaServerAnnotation() throws ClassNotFoundException {
        Class<?> clazz = Class.forName("com.example.demo.EurekaServerApplication");
        assertNotNull(clazz.getAnnotation(org.springframework.cloud.netflix.eureka.server.EnableEurekaServer.class));
    }

    @Test
    void testSpringBootApplicationAnnotation() throws ClassNotFoundException {
        Class<?> clazz = Class.forName("com.example.demo.EurekaServerApplication");
        assertNotNull(clazz.getAnnotation(org.springframework.boot.autoconfigure.SpringBootApplication.class));
    }
}
