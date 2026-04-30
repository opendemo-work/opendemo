package com.example.demo.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

@Configuration
public class ProfileConfig {

    @Bean
    @Profile("dev")
    public String devDataSource() {
        System.out.println("[Profile] 开发环境数据源 - H2内存数据库");
        return "h2-datasource";
    }

    @Bean
    @Profile("test")
    public String testDataSource() {
        System.out.println("[Profile] 测试环境数据源 - H2文件数据库");
        return "h2-file-datasource";
    }

    @Bean
    @Profile("prod")
    public String prodDataSource() {
        System.out.println("[Profile] 生产环境数据源 - MySQL");
        return "mysql-datasource";
    }

    @Bean
    @Profile({"dev", "test"})
    public String debugToolConfig() {
        System.out.println("[Profile] 调试工具已启用 (dev/test环境)");
        return "debug-tools-enabled";
    }
}
