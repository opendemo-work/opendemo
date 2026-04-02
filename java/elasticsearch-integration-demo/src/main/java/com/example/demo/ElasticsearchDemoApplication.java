package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Elasticsearch集成演示应用
 */
@SpringBootApplication
public class ElasticsearchDemoApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(ElasticsearchDemoApplication.class, args);
        System.out.println("==============================================");
        System.out.println("Elasticsearch集成演示应用启动成功!");
        System.out.println("==============================================");
        System.out.println("添加商品: POST http://localhost:8080/api/products");
        System.out.println("搜索商品: GET http://localhost:8080/api/products/search?keyword=手机");
        System.out.println("==============================================");
    }
}
