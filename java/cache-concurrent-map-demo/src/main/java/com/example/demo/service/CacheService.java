package com.example.demo.service;

import com.example.demo.cache.SimpleCacheManager;
import org.springframework.stereotype.Service;

@Service
public class CacheService {

    private final SimpleCacheManager cacheManager;

    public CacheService(SimpleCacheManager cacheManager) {
        this.cacheManager = cacheManager;
    }

    public String getProduct(String productId) {
        String cached = cacheManager.get(productId);
        if (cached != null) {
            return "[缓存] " + cached;
        }
        String product = loadFromDb(productId);
        cacheManager.put(productId, product, 60000);
        return "[数据库] " + product;
    }

    public void refreshProduct(String productId) {
        cacheManager.remove(productId);
    }

    public int getCacheSize() {
        return cacheManager.size();
    }

    public void clearCache() {
        cacheManager.clear();
    }

    public boolean isCached(String key) {
        return cacheManager.contains(key);
    }

    private String loadFromDb(String productId) {
        return "商品-" + productId + " (价格: ¥" + (Math.random() * 1000) + ")";
    }
}
