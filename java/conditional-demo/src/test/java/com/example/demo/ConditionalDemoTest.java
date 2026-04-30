package com.example.demo;

import com.example.demo.service.FeatureToggleService;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class ConditionalDemoTest {

    @Test
    void testFeatureToggleServiceDefaults() {
        FeatureToggleService service = new FeatureToggleService();
        assertFalse(service.isSwaggerEnabled());
        assertTrue(service.isRateLimitEnabled());
        assertEquals("local", service.getCacheType());
    }

    @Test
    void testFeatureToggleServiceActiveFeatures() {
        FeatureToggleService service = new FeatureToggleService();
        List<String> features = service.getActiveFeatures();
        assertFalse(features.contains("swagger"));
        assertTrue(features.contains("rate-limit"));
        assertTrue(features.stream().anyMatch(f -> f.startsWith("cache:")));
    }

    @Test
    void testConditionalConfigBeans() {
        assertNotNull(new com.example.demo.config.ConditionalConfig());
        assertNotNull(new com.example.demo.config.ProfileConfig());
    }

    @Test
    void testDevConfigExists() {
        assertNotNull(new com.example.demo.DevConfig());
    }

    @Test
    void testProfileConfigBeanNames() {
        com.example.demo.config.ProfileConfig config = new com.example.demo.config.ProfileConfig();
        String dev = config.devDataSource();
        assertEquals("h2-datasource", dev);

        String test = config.testDataSource();
        assertEquals("h2-file-datasource", test);

        String prod = config.prodDataSource();
        assertEquals("mysql-datasource", prod);
    }

    @Test
    void testConditionalConfigBeanCreation() {
        com.example.demo.config.ConditionalConfig config = new com.example.demo.config.ConditionalConfig();
        String local = config.localCacheConfig();
        assertEquals("local-cache", local);
    }
}
