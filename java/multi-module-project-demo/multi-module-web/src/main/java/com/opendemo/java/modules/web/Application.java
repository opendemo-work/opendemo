package com.opendemo.java.modules.web;

import com.opendemo.java.modules.service.OrderService;
import com.opendemo.java.modules.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Application {

    private static final Logger logger = LoggerFactory.getLogger(Application.class);

    public static void main(String[] args) {
        logger.info("=== Multi Module Project Demo ===");
        logger.info("启动多模块应用...");
        logger.info("");

        UserService userService = new UserService();
        OrderService orderService = new OrderService();

        UserService.UserInfo user1 = userService.createUser("张三", "zhangsan@example.com");
        UserService.UserInfo user2 = userService.createUser("李四", "lisi@example.com");
        logger.info("已创建 {} 个用户", userService.getAllUsers().size());

        logger.info("");

        orderService.createOrder(user1.getId(), "Java编程思想", 1, 99.0);
        orderService.createOrder(user1.getId(), "设计模式", 2, 59.0);
        orderService.createOrder(user2.getId(), "Spring实战", 1, 79.0);
        logger.info("已创建 {} 个订单", orderService.getAllOrders().size());

        logger.info("");

        logger.info("用户 '{}' 的订单: {}", user1.getUsername(), orderService.getOrdersByUserId(user1.getId()));
        logger.info("总营收: {}", orderService.getTotalRevenue());
    }
}
