package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Apache Kafka消息流处理演示应用
 * 
 * 演示Spring Kafka的Producer和Consumer
 */
@SpringBootApplication
public class KafkaDemoApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(KafkaDemoApplication.class, args);
        System.out.println("==============================================");
        System.out.println("Kafka消息流处理演示应用启动成功!");
        System.out.println("==============================================");
        System.out.println("发送消息: POST http://localhost:8080/api/kafka/send");
        System.out.println("请求体: {\"message\": \"Hello Kafka\", \"topic\": \"demo-topic\"}");
        System.out.println("==============================================");
    }
}
