package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * WebSocket实时通信演示应用
 */
@SpringBootApplication
public class WebSocketDemoApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(WebSocketDemoApplication.class, args);
        System.out.println("==============================================");
        System.out.println("WebSocket实时通信演示应用启动成功!");
        System.out.println("==============================================");
        System.out.println("打开浏览器访问: http://localhost:8080");
        System.out.println("==============================================");
    }
}
