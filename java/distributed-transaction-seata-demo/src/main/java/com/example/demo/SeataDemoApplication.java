package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;

/**
 * Seata分布式事务演示应用
 * 
 * 演示场景：电商下单
 * - 订单服务：创建订单
 * - 库存服务：扣减库存
 * - 账户服务：扣减余额
 * 
 * 使用Seata AT模式保证分布式事务一致性
 */
@SpringBootApplication
@EnableFeignClients
public class SeataDemoApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(SeataDemoApplication.class, args);
        System.out.println("==============================================");
        System.out.println("Seata分布式事务演示应用启动成功!");
        System.out.println("==============================================");
        System.out.println("Seata Server: http://localhost:8091");
        System.out.println("测试下单: POST http://localhost:8080/order/create");
        System.out.println("==============================================");
    }
}
