package com.example.demo;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class EurekaClientApplicationTest {

    @Test
    void testMainClassExists() {
        assertDoesNotThrow(() -> {
            Class<?> clazz = Class.forName("com.example.demo.EurekaClientApplication");
            assertNotNull(clazz);
        });
    }

    @Test
    void testEnableEurekaClientAnnotation() throws ClassNotFoundException {
        Class<?> clazz = Class.forName("com.example.demo.EurekaClientApplication");
        assertNotNull(clazz.getAnnotation(org.springframework.cloud.netflix.eureka.EnableEurekaClient.class));
    }

    @Test
    void testSpringBootApplicationAnnotation() throws ClassNotFoundException {
        Class<?> clazz = Class.forName("com.example.demo.EurekaClientApplication");
        assertNotNull(clazz.getAnnotation(org.springframework.boot.autoconfigure.SpringBootApplication.class));
    }
}
