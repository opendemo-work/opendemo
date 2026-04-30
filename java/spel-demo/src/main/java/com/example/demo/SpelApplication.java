package com.example.demo;

import com.example.demo.service.SpelService;
import com.example.demo.model.User;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;

import java.util.List;
import java.util.Map;

@SpringBootApplication
public class SpelApplication {
    public static void main(String[] args) {
        ConfigurableApplicationContext context = SpringApplication.run(SpelApplication.class, args);

        SpelService spelService = context.getBean(SpelService.class);

        System.out.println("=== SpEL 表达式演示 ===");

        System.out.println("\n--- 基础表达式 ---");
        List<String> basics = spelService.demonstrateBasicExpressions();
        basics.forEach(System.out::println);

        System.out.println("\n--- 对象属性访问 ---");
        User user = new User(1L, "张三", 25, "ADMIN", true);
        Map<String, Object> userResults = spelService.demonstrateUserExpressions(user);
        userResults.forEach((k, v) -> System.out.println(k + " = " + v));

        System.out.println("\n--- 集合操作 ---");
        List<String> collections = spelService.demonstrateCollectionExpressions();
        collections.forEach(System.out::println);

        System.out.println("SpEL表达式演示应用启动成功!");
    }
}
