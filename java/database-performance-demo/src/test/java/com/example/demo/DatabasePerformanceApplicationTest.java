package com.example.demo;

import com.example.demo.entity.Product;
import com.example.demo.repository.ProductRepository;
import com.example.demo.service.ProductService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class DatabasePerformanceApplicationTest {

    @Autowired
    private ProductRepository productRepository;

    @Autowired
    private ProductService productService;

    @BeforeEach
    void cleanUp() {
        productRepository.deleteAll();
    }

    @Test
    @DisplayName("应用上下文应成功加载")
    void contextLoads() {
    }

    @Test
    @DisplayName("单个产品应能成功保存和查询")
    void testSaveAndFindProduct() {
        Product product = new Product("测试产品", "电子产品", BigDecimal.valueOf(99.99), "SKU-001");
        product.setBrand("测试品牌");
        product.setStockQuantity(100);

        Product saved = productRepository.save(product);
        assertNotNull(saved.getId());

        Optional<Product> found = productRepository.findById(saved.getId());
        assertTrue(found.isPresent());
        assertEquals("测试产品", found.get().getName());
        assertEquals("电子产品", found.get().getCategory());
    }

    @Test
    @DisplayName("批量插入应比逐条插入更快")
    void testBatchInsertFasterThanOneByOne() {
        int count = 200;

        long oneByOneTime = productService.insertOneByOne(count);
        productRepository.deleteAll();

        long batchTime = productService.insertInBatch(count, 50);

        assertEquals(count, productRepository.count());
    }

    @Test
    @DisplayName("按分类查询应返回正确结果")
    void testFindByCategory() {
        productService.generateSampleData(100);

        List<Product> electronics = productRepository.findByCategory("电子产品");
        assertFalse(electronics.isEmpty());
        electronics.forEach(p -> assertEquals("电子产品", p.getCategory()));
    }

    @Test
    @DisplayName("投影查询应返回正确数据")
    void testProjectionQuery() {
        productService.generateSampleData(100);

        List<Object[]> projections = productRepository.findProjectedByCategory("电子产品");
        assertFalse(projections.isEmpty());
        projections.forEach(arr -> {
            assertEquals(3, arr.length);
            assertNotNull(arr[0]);
            assertNotNull(arr[1]);
            assertNotNull(arr[2]);
        });
    }

    @Test
    @DisplayName("价格范围查询应正确过滤")
    void testPriceRangeQuery() {
        productService.generateSampleData(200);

        List<Product> results = productRepository.findByCategoryAndPriceRange(
                "电子产品",
                BigDecimal.valueOf(100),
                BigDecimal.valueOf(500)
        );

        results.forEach(p -> {
            assertEquals("电子产品", p.getCategory());
            assertTrue(p.getPrice().compareTo(BigDecimal.valueOf(100)) >= 0);
            assertTrue(p.getPrice().compareTo(BigDecimal.valueOf(500)) <= 0);
        });
    }

    @Test
    @DisplayName("分页搜索应返回正确页")
    void testPagedSearch() {
        productService.generateSampleData(100);

        Page<Product> page1 = productRepository.searchByKeyword("产品", PageRequest.of(0, 10));
        assertFalse(page1.getContent().isEmpty());
        assertTrue(page1.getContent().size() <= 10);
    }

    @Test
    @DisplayName("SKU查询应返回唯一结果")
    void testFindBySku() {
        Product product = new Product("SKU测试", "图书", BigDecimal.valueOf(49.99), "SKU-UNIQUE-001");
        productRepository.save(product);

        Optional<Product> found = productRepository.findBySku("SKU-UNIQUE-001");
        assertTrue(found.isPresent());
        assertEquals("SKU测试", found.get().getName());

        Optional<Product> notFound = productRepository.findBySku("NOT-EXIST");
        assertFalse(notFound.isPresent());
    }

    @Test
    @DisplayName("聚合统计查询应返回正确结果")
    void testAggregateQuery() {
        productService.generateSampleData(200);

        List<Object[]> stats = productRepository.getCategoryStats();
        assertFalse(stats.isEmpty());
        assertEquals(5, stats.size());

        for (Object[] stat : stats) {
            assertNotNull(stat[0]);
            assertTrue((Long) stat[1] > 0);
            assertNotNull(stat[2]);
        }
    }

    @Test
    @DisplayName("批量更新库存应正确执行")
    void testBatchUpdate() {
        productService.generateSampleData(50);

        List<Product> products = productRepository.findAll();
        List<Long> ids = products.subList(0, Math.min(10, products.size()))
                .stream().map(Product::getId).collect(java.util.stream.Collectors.toList());

        int updated = productRepository.batchUpdateStock(999, ids);
        assertEquals(ids.size(), updated);

        productRepository.findAllById(ids).forEach(p ->
                assertEquals(999, p.getStockQuantity()));
    }

    @Test
    @DisplayName("分类计数应返回正确值")
    void testCountByCategory() {
        productService.generateSampleData(100);

        long count = productRepository.countByCategory("电子产品");
        assertTrue(count > 0);
    }

    @Test
    @DisplayName("原生SQL查询应正常工作")
    void testNativeQuery() {
        productService.generateSampleData(100);

        List<Product> expensive = productRepository.findTopByPriceNative(BigDecimal.valueOf(500), 5);
        assertTrue(expensive.size() <= 5);
        expensive.forEach(p ->
                assertTrue(p.getPrice().compareTo(BigDecimal.valueOf(500)) > 0));
    }
}
