package com.example.demo.controller;

import com.example.demo.entity.Product;
import com.example.demo.service.ProductService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 商品控制器
 */
@RestController
@RequestMapping("/api/products")
public class ProductController {
    
    @Autowired
    private ProductService productService;
    
    /**
     * 添加商品
     */
    @PostMapping
    public ResponseEntity<Product> addProduct(@RequestBody Product product) {
        Product saved = productService.save(product);
        return ResponseEntity.ok(saved);
    }
    
    /**
     * 根据ID查询
     */
    @GetMapping("/{id}")
    public ResponseEntity<Product> getById(@PathVariable String id) {
        return productService.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
    
    /**
     * 查询所有
     */
    @GetMapping
    public ResponseEntity<Iterable<Product>> getAll() {
        return ResponseEntity.ok(productService.findAll());
    }
    
    /**
     * 删除
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable String id) {
        productService.deleteById(id);
        return ResponseEntity.ok().build();
    }
    
    /**
     * 关键词搜索
     */
    @GetMapping("/search")
    public ResponseEntity<List<Product>> search(@RequestParam String keyword) {
        List<Product> products = productService.search(keyword);
        return ResponseEntity.ok(products);
    }
    
    /**
     * 根据分类查询
     */
    @GetMapping("/category/{category}")
    public ResponseEntity<List<Product>> searchByCategory(@PathVariable String category) {
        List<Product> products = productService.searchByCategory(category);
        return ResponseEntity.ok(products);
    }
    
    /**
     * 分页查询
     */
    @GetMapping("/category/{category}/page")
    public ResponseEntity<Page<Product>> searchByCategoryPaged(
            @PathVariable String category,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        Page<Product> products = productService.searchByCategoryWithPaging(category, page, size);
        return ResponseEntity.ok(products);
    }
    
    /**
     * 价格范围查询
     */
    @GetMapping("/price-range")
    public ResponseEntity<List<Product>> searchByPriceRange(
            @RequestParam Double min,
            @RequestParam Double max) {
        List<Product> products = productService.searchByPriceRange(min, max);
        return ResponseEntity.ok(products);
    }
    
    /**
     * 高级搜索
     */
    @GetMapping("/advanced-search")
    public ResponseEntity<List<Product>> advancedSearch(
            @RequestParam String name,
            @RequestParam Double maxPrice) {
        List<Product> products = productService.advancedSearch(name, maxPrice);
        return ResponseEntity.ok(products);
    }
    
    /**
     * 初始化数据
     */
    @PostMapping("/init")
    public ResponseEntity<Map<String, String>> initData() {
        // 添加示例数据
        productService.save(new Product("1", "iPhone 14 Pro", 
                "苹果最新旗舰手机，支持5G网络", 7999.0, "手机", "Apple", 100));
        productService.save(new Product("2", "华为Mate 50", 
                "华为旗舰手机，徕卡影像", 5999.0, "手机", "华为", 50));
        productService.save(new Product("3", "MacBook Pro", 
                "苹果笔记本电脑，M2芯片", 12999.0, "电脑", "Apple", 30));
        productService.save(new Product("4", "小米13", 
                "小米旗舰手机，骁龙8 Gen2", 3999.0, "手机", "小米", 200));
        productService.save(new Product("5", "ThinkPad X1", 
                "联想商务笔记本", 8999.0, "电脑", "联想", 80));
        
        Map<String, String> result = new HashMap<>();
        result.put("message", "初始化数据完成");
        return ResponseEntity.ok(result);
    }
}
