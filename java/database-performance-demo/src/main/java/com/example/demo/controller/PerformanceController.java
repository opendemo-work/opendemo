package com.example.demo.controller;

import com.example.demo.service.ProductService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.LongStream;

@RestController
@RequestMapping("/api/perf")
public class PerformanceController {

    private final ProductService productService;

    public PerformanceController(ProductService productService) {
        this.productService = productService;
    }

    @GetMapping("/insert-compare")
    public ResponseEntity<Map<String, Object>> compareInsertMethods(
            @RequestParam(defaultValue = "1000") int count) {

        Map<String, Object> result = new LinkedHashMap<>();

        long oneByOneTime = productService.insertOneByOne(count);
        productService.insertOneByOne(0);

        productService.generateSampleData(count);
        long batchTime = productService.insertInBatch(count, 50);

        result.put("recordCount", count);
        result.put("oneByOneTimeMs", oneByOneTime);
        result.put("batchTimeMs", batchTime);
        result.put("speedup", oneByOneTime > 0 ? String.format("%.1fx", (double) oneByOneTime / batchTime) : "N/A");
        result.put("batchSize", 50);

        return ResponseEntity.ok(result);
    }

    @GetMapping("/n-plus-1")
    public ResponseEntity<Map<String, Object>> demonstrateNPlusOne(
            @RequestParam(defaultValue = "1000") int count) {

        productService.generateSampleData(count);

        Map<String, Object> result = new LinkedHashMap<>();
        long nPlusOneTime = productService.demonstrateNPlusOne();
        long projectionTime = productService.demonstrateProjectionQuery();

        result.put("recordCount", productService.getProductCount());
        result.put("nPlusOneTimeMs", nPlusOneTime);
        result.put("projectionTimeMs", projectionTime);
        result.put("recommendation", "使用投影查询或JOIN FETCH避免N+1问题");

        return ResponseEntity.ok(result);
    }

    @GetMapping("/index-vs-scan")
    public ResponseEntity<Map<String, Object>> compareIndexVsScan(
            @RequestParam(defaultValue = "5000") int count) {

        productService.generateSampleData(count);

        Map<String, Object> result = new LinkedHashMap<>();
        long indexTime = productService.demonstrateIndexLookup("电子产品");
        long scanTime = productService.demonstrateFullScan("搜索");

        result.put("recordCount", productService.getProductCount());
        result.put("indexLookupTimeMs", indexTime);
        result.put("fullScanTimeMs", scanTime);
        result.put("recommendation", "为常用查询条件创建适当的索引");

        return ResponseEntity.ok(result);
    }

    @GetMapping("/batch-update")
    public ResponseEntity<Map<String, Object>> demonstrateBatchUpdate(
            @RequestParam(defaultValue = "1000") int count) {

        productService.generateSampleData(count);

        long productCount = productService.getProductCount();
        List<Long> ids = LongStream.rangeClosed(1, Math.min(100, productCount))
                .boxed().collect(Collectors.toList());

        Map<String, Object> result = new LinkedHashMap<>();
        long batchUpdateTime = productService.demonstrateBatchUpdate(ids, 999);

        result.put("updatedCount", ids.size());
        result.put("batchUpdateTimeMs", batchUpdateTime);
        result.put("recommendation", "使用批量UPDATE代替逐条更新");

        return ResponseEntity.ok(result);
    }

    @GetMapping("/aggregate")
    public ResponseEntity<Map<String, Object>> demonstrateAggregate() {
        productService.generateSampleData(2000);

        Map<String, Object> result = new LinkedHashMap<>();
        long aggregateTime = productService.demonstrateAggregateQuery();

        result.put("aggregateTimeMs", aggregateTime);
        result.put("recommendation", "在数据库层进行聚合计算，减少数据传输量");

        return ResponseEntity.ok(result);
    }

    @GetMapping("/summary")
    public ResponseEntity<Map<String, Object>> performanceSummary() {
        Map<String, Object> summary = new LinkedHashMap<>();

        summary.put("optimizationTechniques", new String[]{
                "1. 使用批量操作替代逐条操作 (saveAll + flush)",
                "2. 使用投影查询减少数据传输量",
                "3. 为常用查询条件创建索引",
                "4. 使用JOIN FETCH解决N+1问题",
                "5. 在数据库层进行聚合计算",
                "6. 合理配置连接池参数",
                "7. 使用@Transactional(readOnly=true)优化读操作",
                "8. 设置合适的fetchSize避免OOM"
        });

        summary.put("connectionPoolSettings", new HashMap<String, Object>() {{
            put("maximumPoolSize", 10);
            put("minimumIdle", 5);
            put("connectionTimeout", "20s");
            put("idleTimeout", "30s");
            put("maxLifetime", "30min");
        }});

        summary.put("jpaBatchSettings", new HashMap<String, Object>() {{
            put("batchSize", 50);
            put("fetchSize", 100);
            put("orderInserts", true);
            put("orderUpdates", true);
        }});

        return ResponseEntity.ok(summary);
    }
}
