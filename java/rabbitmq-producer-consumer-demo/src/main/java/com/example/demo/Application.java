package com.example.demo;

import com.example.demo.producer.MessageProducer;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

/**
 * RabbitMQ演示应用
 */
@SpringBootApplication
public class Application {
    
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
    
    @Bean
    public CommandLineRunner demo(MessageProducer producer) {
        return args -> {
            System.out.println("\n=== RabbitMQ 生产者消费者演示 ===\n");
            
            // 发送多条消息
            for (int i = 1; i <= 5; i++) {
                producer.sendMessage("Hello RabbitMQ " + i);
                Thread.sleep(1000);
            }
            
            System.out.println("\n=== 演示结束 ===");
        };
    }
}
