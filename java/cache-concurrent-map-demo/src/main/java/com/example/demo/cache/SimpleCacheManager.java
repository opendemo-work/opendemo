package com.example.demo.cache;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

@Component
public class SimpleCacheManager {

    private static final Logger logger = LoggerFactory.getLogger(SimpleCacheManager.class);

    private final Map<String, CacheEntry> cache = new ConcurrentHashMap<>();
    private final ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor();
    private final long defaultTtlMillis;

    public SimpleCacheManager() {
        this(300000);
    }

    public SimpleCacheManager(long defaultTtlMillis) {
        this.defaultTtlMillis = defaultTtlMillis;
        scheduler.scheduleAtFixedRate(this::evictExpired, 60, 60, TimeUnit.SECONDS);
    }

    public void put(String key, Object value) {
        put(key, value, defaultTtlMillis);
    }

    public void put(String key, Object value, long ttlMillis) {
        CacheEntry entry = new CacheEntry(value, System.currentTimeMillis() + ttlMillis);
        cache.put(key, entry);
        logger.debug("缓存写入: key={}, ttl={}ms", key, ttlMillis);
    }

    @SuppressWarnings("unchecked")
    public <T> T get(String key) {
        CacheEntry entry = cache.get(key);
        if (entry == null) {
            logger.debug("缓存未命中: key={}", key);
            return null;
        }
        if (entry.isExpired()) {
            cache.remove(key);
            logger.debug("缓存过期: key={}", key);
            return null;
        }
        logger.debug("缓存命中: key={}", key);
        return (T) entry.getValue();
    }

    public boolean contains(String key) {
        CacheEntry entry = cache.get(key);
        if (entry == null) return false;
        if (entry.isExpired()) {
            cache.remove(key);
            return false;
        }
        return true;
    }

    public void remove(String key) {
        cache.remove(key);
    }

    public void clear() {
        cache.clear();
    }

    public int size() {
        return (int) cache.entrySet().stream().filter(e -> !e.getValue().isExpired()).count();
    }

    public Set<String> keys() {
        return cache.keySet();
    }

    private void evictExpired() {
        int count = 0;
        for (Map.Entry<String, CacheEntry> entry : cache.entrySet()) {
            if (entry.getValue().isExpired()) {
                cache.remove(entry.getKey());
                count++;
            }
        }
        if (count > 0) {
            logger.info("清理过期缓存: {}条", count);
        }
    }

    private static class CacheEntry {
        private final Object value;
        private final long expireTime;

        CacheEntry(Object value, long expireTime) {
            this.value = value;
            this.expireTime = expireTime;
        }

        Object getValue() {
            return value;
        }

        boolean isExpired() {
            return System.currentTimeMillis() > expireTime;
        }
    }
}
