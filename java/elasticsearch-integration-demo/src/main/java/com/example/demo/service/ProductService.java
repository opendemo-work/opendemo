package com.example.demo.service;

import com.example.demo.entity.Product;
import com.example.demo.repository.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

/**
 * 商品服务
 */
@Service
public class ProductService {
    
    @Autowired
    private ProductRepository productRepository;
    
    /**
     * 保存商品
     */
    public Product save(Product product) {
        return productRepository.save(product);
    }
    
    /**
     * 根据ID查询
     */
    public Optional<Product> findById(String id) {
        return productRepository.findById(id);
    }
    
    /**
     * 查询所有
     */
    public Iterable<Product> findAll() {
        return productRepository.findAll();
    }
    
    /**
     * 删除
     */
    public void deleteById(String id) {
        productRepository.deleteById(id);
    }
    
    /**
     * 根据名称搜索
     */
    public List<Product> searchByName(String name) {
        return productRepository.findByNameContaining(name);
    }
    
    /**
     * 根据分类查询
     */
    public List<Product> searchByCategory(String category) {
        return productRepository.findByCategory(category);
    }
    
    /**
     * 根据价格范围查询
     */
    public List<Product> searchByPriceRange(Double minPrice, Double maxPrice) {
        return productRepository.findByPriceBetween(minPrice, maxPrice);
    }
    
    /**
     * 综合搜索（名称或描述）
     */
    public List<Product> search(String keyword) {
        return productRepository.findByNameContainingOrDescriptionContaining(keyword, keyword);
    }
    
    /**
     * 分页查询
     */
    public Page<Product> searchByCategoryWithPaging(String category, int page, int size) {
        Pageable pageable = PageRequest.of(page, size);
        return productRepository.findByCategory(category, pageable);
    }
    
    /**
     * 高级搜索（名称+最大价格）
     */
    public List<Product> advancedSearch(String name, Double maxPrice) {
        return productRepository.findByNameAndMaxPrice(name, maxPrice);
    }
}
