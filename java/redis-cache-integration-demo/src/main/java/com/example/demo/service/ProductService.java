package com.example.demo.service;

import com.example.demo.entity.Product;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.CachePut;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.math.BigDecimal;
import java.util.HashMap;
import java.util.Map;

/**
 * 商品服务类
 * 
 * 演示Spring Cache与Redis集成
 */
@Service
public class ProductService {
    
    private final Map<Long, Product> productStore = new HashMap<>();
    
    @PostConstruct
    public void init() {
        // 初始化数据
        productStore.put(1L, new Product(1L, "iPhone 14", "苹果手机", new BigDecimal("5999")));
        productStore.put(2L, new Product(2L, "MacBook Pro", "苹果笔记本", new BigDecimal("12999")));
        productStore.put(3L, new Product(3L, "AirPods Pro", "无线耳机", new BigDecimal("1999")));
    }
    
    /**
     * 查询商品（使用缓存）
     * 
     * @Cacheable: 先查缓存，缓存没有则执行方法并缓存结果
     * value: 缓存名称
     * key: 缓存键
     */
    @Cacheable(value = "products", key = "#id")
    public Product getProduct(Long id) {
        System.out.println("[查询数据库] 查询商品ID: " + id);
        
        // 模拟耗时操作
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        return productStore.get(id);
    }
    
    /**
     * 更新商品（更新缓存）
     * 
     * @CachePut: 执行方法，并将结果更新到缓存
     */
    @CachePut(value = "products", key = "#product.id")
    public Product updateProduct(Product product) {
        System.out.println("[更新数据库] 更新商品: " + product.getId());
        productStore.put(product.getId(), product);
        return product;
    }
    
    /**
     * 删除商品（清除缓存）
     * 
     * @CacheEvict: 执行方法，并清除缓存
     */
    @CacheEvict(value = "products", key = "#id")
    public void deleteProduct(Long id) {
        System.out.println("[删除数据库] 删除商品ID: " + id);
        productStore.remove(id);
    }
    
    /**
     * 清除所有缓存
     */
    @CacheEvict(value = "products", allEntries = true)
    public void clearCache() {
        System.out.println("[清除缓存] 清除所有商品缓存");
    }
}
