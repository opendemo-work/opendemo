package com.opendemo.java.modules.web.controller;

import com.opendemo.java.modules.service.OrderService;
import com.opendemo.java.modules.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.Map;

public class UserController {

    private static final Logger logger = LoggerFactory.getLogger(UserController.class);

    private final UserService userService;
    private final OrderService orderService;

    public UserController(UserService userService, OrderService orderService) {
        this.userService = userService;
        this.orderService = orderService;
    }

    public Map<String, Object> getUserDetail(Long userId) {
        UserService.UserInfo user = userService.getUserById(userId);
        List<OrderService.OrderInfo> orders = orderService.getOrdersByUserId(userId);
        double totalSpent = orders.stream()
                .mapToDouble(OrderService.OrderInfo::getTotalAmount)
                .sum();
        logger.info("查询用户详情: userId={}, orders={}, totalSpent={}", userId, orders.size(), totalSpent);
        return Map.of(
                "user", user,
                "orderCount", orders.size(),
                "totalSpent", totalSpent
        );
    }

    public UserService.UserInfo createUser(String username, String email) {
        return userService.createUser(username, email);
    }

    public List<UserService.UserInfo> listUsers() {
        return userService.getAllUsers();
    }
}
