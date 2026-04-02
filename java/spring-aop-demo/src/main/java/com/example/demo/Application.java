package com.example.demo;

import com.example.demo.config.AopConfig;
import com.example.demo.service.OrderService;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

/**
 * Spring AOP演示应用
 * 
 * 展示各种AOP Advice的执行顺序和效果
 */
public class Application {
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("╔══════════════════════════════════════════════════════════╗");
        System.out.println("║          Spring AOP 面向切面编程演示                      ║");
        System.out.println("╚══════════════════════════════════════════════════════════╝\n");
        
        // 创建容器
        AnnotationConfigApplicationContext context = 
                new AnnotationConfigApplicationContext(AopConfig.class);
        
        // 获取OrderService
        OrderService orderService = context.getBean(OrderService.class);
        
        System.out.println("📦 示例1: 正常方法调用\n");
        String orderId = orderService.createOrder("PROD_001", 2);
        
        System.out.println("📦 示例2: 方法抛出异常\n");
        try {
            orderService.getOrder("");  // 传入空字符串，会抛出异常
        } catch (IllegalArgumentException e) {
            System.out.println("  [捕获] 异常: " + e.getMessage() + "\n");
        }
        
        System.out.println("📦 示例3: 环绕通知（性能监控）\n");
        orderService.processOrder(orderId);
        
        System.out.println("═══════════════════════════════════════════════════════════");
        System.out.println("AOP Advice执行顺序总结:");
        System.out.println("  1. @Around (前置部分)");
        System.out.println("  2. @Before");
        System.out.println("  3. 目标方法执行");
        System.out.println("  4. @Around (后置部分)");
        System.out.println("  5. @AfterReturning 或 @AfterThrowing");
        System.out.println("  6. @After");
        System.out.println("═══════════════════════════════════════════════════════════");
        
        context.close();
    }
}
