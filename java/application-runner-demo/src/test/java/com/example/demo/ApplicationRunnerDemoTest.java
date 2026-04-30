package com.example.demo;

import com.example.demo.service.DataService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class ApplicationRunnerDemoTest {

    private DataService dataService;

    @BeforeEach
    void setUp() {
        dataService = new DataService();
    }

    @Test
    void testDataServicePutAndGet() {
        dataService.put("key1", "value1");
        assertEquals("value1", dataService.get("key1"));
    }

    @Test
    void testDataServiceGetAll() {
        dataService.put("a", "1");
        dataService.put("b", "2");
        Map<String, String> all = dataService.getAll();
        assertEquals(2, all.size());
        assertEquals("1", all.get("a"));
        assertEquals("2", all.get("b"));
    }

    @Test
    void testDataServiceSize() {
        assertEquals(0, dataService.size());
        dataService.put("k", "v");
        assertEquals(1, dataService.size());
    }

    @Test
    void testDataServiceContains() {
        dataService.put("exists", "yes");
        assertTrue(dataService.contains("exists"));
        assertFalse(dataService.contains("notexists"));
    }

    @Test
    void testDataServiceClear() {
        dataService.put("a", "1");
        dataService.put("b", "2");
        dataService.clear();
        assertEquals(0, dataService.size());
    }

    @Test
    void testDataServiceOverwrite() {
        dataService.put("key", "old");
        dataService.put("key", "new");
        assertEquals("new", dataService.get("key"));
    }

    @Test
    void testDataServiceGetNull() {
        assertNull(dataService.get("nonexistent"));
    }

    @Test
    void testDataInitialization() {
        dataService.put("config.theme", "dark");
        dataService.put("config.language", "zh-CN");
        dataService.put("config.pageSize", "20");
        assertEquals(3, dataService.size());
        assertEquals("dark", dataService.get("config.theme"));
        assertEquals("zh-CN", dataService.get("config.language"));
    }
}
