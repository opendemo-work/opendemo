package com.example.demo;

import com.example.demo.service.DataService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

@Component
@Order(2)
public class CacheWarmUpRunner implements ApplicationRunner {

    private static final Logger logger = LoggerFactory.getLogger(CacheWarmUpRunner.class);

    private final DataService dataService;

    public CacheWarmUpRunner(DataService dataService) {
        this.dataService = dataService;
    }

    @Override
    public void run(ApplicationArguments args) {
        logger.info("=== 缓存预热开始 ===");

        for (Map.Entry<String, String> entry : dataService.getAll().entrySet()) {
            logger.info("缓存加载: {} = {}", entry.getKey(), entry.getValue());
        }

        logger.info("缓存预热条数: {}", dataService.size());
        logger.info("=== 缓存预热完成 ===");

        logger.info("普通参数 (NonOptionArgs): {}", args.getNonOptionArgs());
        logger.info("选项参数 (OptionNames): {}", args.getOptionNames());
        for (String optionName : args.getOptionNames()) {
            logger.info("  --{} = {}", optionName, args.getOptionValues(optionName));
        }
    }
}
