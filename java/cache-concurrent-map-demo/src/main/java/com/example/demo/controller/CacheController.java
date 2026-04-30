package com.example.demo.controller;

import com.example.demo.service.CacheService;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/cache")
public class CacheController {

    private final CacheService cacheService;

    public CacheController(CacheService cacheService) {
        this.cacheService = cacheService;
    }

    @GetMapping("/product/{id}")
    public Map<String, String> getProduct(@PathVariable String id) {
        Map<String, String> result = new HashMap<>();
        result.put("productId", id);
        result.put("data", cacheService.getProduct(id));
        result.put("cached", String.valueOf(cacheService.isCached(id)));
        return result;
    }

    @DeleteMapping("/product/{id}")
    public Map<String, String> refreshProduct(@PathVariable String id) {
        cacheService.refreshProduct(id);
        Map<String, String> result = new HashMap<>();
        result.put("message", "缓存已刷新");
        result.put("productId", id);
        return result;
    }

    @GetMapping("/stats")
    public Map<String, Object> getStats() {
        Map<String, Object> stats = new HashMap<>();
        stats.put("cacheSize", cacheService.getCacheSize());
        return stats;
    }

    @DeleteMapping("/clear")
    public Map<String, String> clearCache() {
        cacheService.clearCache();
        Map<String, String> result = new HashMap<>();
        result.put("message", "缓存已清空");
        return result;
    }
}
