package com.example.demo.service;

import org.springframework.stereotype.Service;

/**
 * 订单服务类
 * 
 * 用于演示AOP切面的目标类
 */
@Service
public class OrderService {
    
    /**
     * 创建订单
     */
    public String createOrder(String productId, int quantity) {
        System.out.println("  [业务] 创建订单: productId=" + productId + ", quantity=" + quantity);
        // 模拟业务逻辑
        return "ORDER_" + System.currentTimeMillis();
    }
    
    /**
     * 取消订单
     */
    public boolean cancelOrder(String orderId) {
        System.out.println("  [业务] 取消订单: " + orderId);
        // 模拟业务逻辑
        return true;
    }
    
    /**
     * 查询订单（可能抛出异常）
     */
    public String getOrder(String orderId) {
        System.out.println("  [业务] 查询订单: " + orderId);
        if (orderId == null || orderId.isEmpty()) {
            throw new IllegalArgumentException("订单ID不能为空");
        }
        return "OrderInfo[" + orderId + "]";
    }
    
    /**
     * 模拟耗时操作
     */
    public void processOrder(String orderId) throws InterruptedException {
        System.out.println("  [业务] 处理订单: " + orderId);
        Thread.sleep(100); // 模拟耗时
    }
}
