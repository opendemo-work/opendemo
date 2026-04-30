package com.example.demo;

import com.example.demo.service.DataService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

@Component
@Order(1)
public class DataInitializationRunner implements ApplicationRunner {

    private static final Logger logger = LoggerFactory.getLogger(DataInitializationRunner.class);

    private final DataService dataService;

    public DataInitializationRunner(DataService dataService) {
        this.dataService = dataService;
    }

    @Override
    public void run(ApplicationArguments args) {
        logger.info("=== 数据初始化开始 ===");

        dataService.put("config.theme", "dark");
        dataService.put("config.language", "zh-CN");
        dataService.put("config.pageSize", "20");
        dataService.put("user.admin", "admin@example.com");
        dataService.put("user.guest", "guest@example.com");

        logger.info("初始化数据条数: {}", dataService.size());

        if (args.containsOption("env")) {
            String env = args.getOptionValues("env").get(0);
            dataService.put("config.env", env);
            logger.info("环境参数设置: env={}", env);
        }

        logger.info("=== 数据初始化完成 ===");
    }
}
