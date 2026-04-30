package com.example.demo.repository;

import com.example.demo.entity.Product;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class ProductRepositoryTest {

    @Autowired
    private ProductRepository productRepository;

    @Test
    void testSave() {
        Product product = new Product("测试商品", 199.00, 50, "测试分类");
        Product saved = productRepository.save(product);
        assertNotNull(saved.getId());
        assertEquals("测试商品", saved.getName());
    }

    @Test
    void testFindById() {
        Product product = new Product("查找测试", 299.00, 30, "测试");
        Product saved = productRepository.save(product);
        Optional<Product> found = productRepository.findById(saved.getId());
        assertTrue(found.isPresent());
        assertEquals("查找测试", found.get().getName());
    }

    @Test
    void testFindAll() {
        List<Product> products = productRepository.findAll();
        assertNotNull(products);
        assertTrue(products.size() >= 6);
    }

    @Test
    void testFindByCategory() {
        List<Product> electronics = productRepository.findByCategory("电子产品");
        assertNotNull(electronics);
        assertTrue(electronics.size() >= 4);
    }

    @Test
    void testUpdate() {
        Product product = new Product("更新前", 100.00, 10, "测试");
        Product saved = productRepository.save(product);
        saved.setName("更新后");
        saved.setPrice(150.00);
        int rows = productRepository.update(saved);
        assertEquals(1, rows);
        Optional<Product> updated = productRepository.findById(saved.getId());
        assertTrue(updated.isPresent());
        assertEquals("更新后", updated.get().getName());
    }

    @Test
    void testDelete() {
        Product product = new Product("待删除", 50.00, 5, "测试");
        Product saved = productRepository.save(product);
        int rows = productRepository.deleteById(saved.getId());
        assertEquals(1, rows);
        Optional<Product> found = productRepository.findById(saved.getId());
        assertFalse(found.isPresent());
    }

    @Test
    void testCount() {
        int count = productRepository.count();
        assertTrue(count > 0);
    }
}
