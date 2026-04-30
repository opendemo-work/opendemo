package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;

import com.example.demo.service.UserService;

@SpringBootApplication
public class AopLoggingApplication {
    public static void main(String[] args) {
        ConfigurableApplicationContext context = SpringApplication.run(AopLoggingApplication.class, args);

        UserService userService = context.getBean(UserService.class);

        System.out.println("=== AOP日志演示 ===");
        userService.findById(1L);
        userService.findAll();
        userService.createUser(4L, "赵六");
        userService.updateUser(1L, "张三丰");
        userService.deleteUser(2L);

        System.out.println("AOP日志演示应用启动成功!");
    }
}
