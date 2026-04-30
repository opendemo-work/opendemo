package com.example.demo;

import com.example.demo.cache.SimpleCacheManager;
import com.example.demo.service.CacheService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class CacheConcurrentMapDemoTest {

    private SimpleCacheManager cacheManager;
    private CacheService cacheService;

    @BeforeEach
    void setUp() {
        cacheManager = new SimpleCacheManager(300000);
        cacheService = new CacheService(cacheManager);
    }

    @Test
    void testCachePutAndGet() {
        cacheManager.put("key1", "value1");
        assertEquals("value1", cacheManager.get("key1"));
    }

    @Test
    void testCacheMiss() {
        assertNull(cacheManager.get("nonexistent"));
    }

    @Test
    void testCacheContains() {
        cacheManager.put("key1", "value1");
        assertTrue(cacheManager.contains("key1"));
        assertFalse(cacheManager.contains("nonexistent"));
    }

    @Test
    void testCacheRemove() {
        cacheManager.put("key1", "value1");
        cacheManager.remove("key1");
        assertFalse(cacheManager.contains("key1"));
    }

    @Test
    void testCacheClear() {
        cacheManager.put("a", "1");
        cacheManager.put("b", "2");
        cacheManager.clear();
        assertEquals(0, cacheManager.size());
    }

    @Test
    void testCacheSize() {
        cacheManager.put("a", "1");
        cacheManager.put("b", "2");
        cacheManager.put("c", "3");
        assertEquals(3, cacheManager.size());
    }

    @Test
    void testCacheTtl() throws InterruptedException {
        SimpleCacheManager shortLived = new SimpleCacheManager(50);
        shortLived.put("short", "data", 50);
        assertNotNull(shortLived.get("short"));
        Thread.sleep(100);
        assertNull(shortLived.get("short"));
    }

    @Test
    void testCacheOverwrite() {
        cacheManager.put("key", "old");
        cacheManager.put("key", "new");
        assertEquals("new", cacheManager.get("key"));
    }

    @Test
    void testCacheDifferentTypes() {
        cacheManager.put("string", "hello");
        cacheManager.put("integer", 42);
        cacheManager.put("boolean", true);
        assertEquals("hello", cacheManager.<String>get("string"));
        assertEquals(42, cacheManager.<Integer>get("integer"));
        assertEquals(true, cacheManager.<Boolean>get("boolean"));
    }

    @Test
    void testCacheServiceGetProduct() {
        String first = cacheService.getProduct("P001");
        assertTrue(first.contains("[数据库]"));
        String second = cacheService.getProduct("P001");
        assertTrue(second.contains("[缓存]"));
    }

    @Test
    void testCacheServiceRefresh() {
        cacheService.getProduct("P001");
        assertTrue(cacheService.isCached("P001"));
        cacheService.refreshProduct("P001");
        assertFalse(cacheService.isCached("P001"));
    }

    @Test
    void testCacheServiceClear() {
        cacheService.getProduct("P001");
        cacheService.getProduct("P002");
        assertTrue(cacheService.getCacheSize() >= 2);
        cacheService.clearCache();
        assertEquals(0, cacheService.getCacheSize());
    }

    @Test
    void testCacheKeys() {
        cacheManager.put("a", "1");
        cacheManager.put("b", "2");
        assertTrue(cacheManager.keys().contains("a"));
        assertTrue(cacheManager.keys().contains("b"));
    }
}
