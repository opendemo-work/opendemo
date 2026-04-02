package com.example.demo.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.config.EnableMongoAuditing;

/**
 * MongoDB配置
 * 
 * @EnableMongoAuditing: 启用审计功能（自动填充创建时间、更新时间）
 */
@Configuration
@EnableMongoAuditing
public class MongoConfig {
}
