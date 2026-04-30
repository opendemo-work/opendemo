package com.example.demo.service;

import com.example.demo.entity.Product;
import com.example.demo.repository.ProductRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

@Service
public class ProductService {

    private static final Logger logger = LoggerFactory.getLogger(ProductService.class);

    private final ProductRepository productRepository;

    public ProductService(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    @Transactional
    public long insertOneByOne(int count) {
        long start = System.currentTimeMillis();

        String[] categories = {"电子产品", "服装", "食品", "图书", "家居"};
        for (int i = 0; i < count; i++) {
            Product p = new Product(
                    "产品-" + i,
                    categories[i % categories.length],
                    BigDecimal.valueOf(10 + Math.random() * 990),
                    "SKU-" + String.format("%06d", i)
            );
            p.setDescription("这是产品" + i + "的详细描述信息，包含多个关键字用于搜索测试。");
            p.setStockQuantity((int) (Math.random() * 1000));
            p.setBrand("品牌" + (i % 20));
            productRepository.save(p);
        }

        long duration = System.currentTimeMillis() - start;
        logger.info("逐条插入 {} 条记录耗时: {} ms", count, duration);
        return duration;
    }

    @Transactional
    public long insertInBatch(int count, int batchSize) {
        long start = System.currentTimeMillis();

        String[] categories = {"电子产品", "服装", "食品", "图书", "家居"};
        List<Product> batch = new ArrayList<>(batchSize);

        for (int i = 0; i < count; i++) {
            Product p = new Product(
                    "产品-B" + i,
                    categories[i % categories.length],
                    BigDecimal.valueOf(10 + Math.random() * 990),
                    "SKU-B" + String.format("%06d", i)
            );
            p.setDescription("这是批量产品" + i + "的详细描述信息。");
            p.setStockQuantity((int) (Math.random() * 1000));
            p.setBrand("品牌" + (i % 20));
            batch.add(p);

            if (batch.size() >= batchSize) {
                productRepository.saveAll(batch);
                productRepository.flush();
                batch.clear();
            }
        }

        if (!batch.isEmpty()) {
            productRepository.saveAll(batch);
            productRepository.flush();
        }

        long duration = System.currentTimeMillis() - start;
        logger.info("批量插入 {} 条记录(batchSize={})耗时: {} ms", count, batchSize, duration);
        return duration;
    }

    @Transactional(readOnly = true)
    public long demonstrateNPlusOne() {
        long start = System.currentTimeMillis();

        List<Product> products = productRepository.findAll();
        long total = products.stream()
                .mapToLong(p -> p.getCategory().length())
                .sum();

        long duration = System.currentTimeMillis() - start;
        logger.info("N+1查询: 加载 {} 条记录耗时 {} ms (ignore: {})", products.size(), duration, total);
        return duration;
    }

    @Transactional(readOnly = true)
    public long demonstrateProjectionQuery() {
        long start = System.currentTimeMillis();

        List<Object[]> projections = productRepository.findProjectedByCategory("电子产品");
        long total = projections.size();

        long duration = System.currentTimeMillis() - start;
        logger.info("投影查询: 返回 {} 条记录耗时 {} ms", total, duration);
        return duration;
    }

    @Transactional(readOnly = true)
    public long demonstrateIndexLookup(String category) {
        long start = System.currentTimeMillis();

        List<Product> products = productRepository.findByCategory(category);

        long duration = System.currentTimeMillis() - start;
        logger.info("索引查找(category={}): 返回 {} 条记录耗时 {} ms", category, products.size(), duration);
        return duration;
    }

    @Transactional(readOnly = true)
    public long demonstrateFullScan(String keyword) {
        long start = System.currentTimeMillis();

        String[] categories = {"电子产品", "服装", "食品", "图书", "家居"};
        List<Product> results = new ArrayList<>();
        for (String cat : categories) {
            results.addAll(productRepository.findByCategory(cat));
        }
        List<Product> filtered = results.stream()
                .filter(p -> p.getDescription() != null && p.getDescription().contains(keyword))
                .collect(Collectors.toList());

        long duration = System.currentTimeMillis() - start;
        logger.info("全表扫描(keyword={}): 过滤出 {} 条记录耗时 {} ms", keyword, filtered.size(), duration);
        return duration;
    }

    @Transactional
    public long demonstrateBatchUpdate(List<Long> ids, Integer quantity) {
        long start = System.currentTimeMillis();

        int updated = productRepository.batchUpdateStock(quantity, ids);

        long duration = System.currentTimeMillis() - start;
        logger.info("批量更新: 更新 {} 条记录耗时 {} ms", updated, duration);
        return duration;
    }

    @Transactional(readOnly = true)
    public long demonstrateAggregateQuery() {
        long start = System.currentTimeMillis();

        List<Object[]> stats = productRepository.getCategoryStats();
        stats.forEach(stat ->
                logger.info("分类: {}, 数量: {}, 平均价格: {}", stat[0], stat[1], stat[2])
        );

        long duration = System.currentTimeMillis() - start;
        logger.info("聚合查询耗时: {} ms", duration);
        return duration;
    }

    @Transactional
    public void generateSampleData(int count) {
        insertInBatch(count, 50);
    }

    public long getProductCount() {
        return productRepository.count();
    }
}
