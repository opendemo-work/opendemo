package com.opendemo.java.exceptions;

import java.util.ArrayList;
import java.util.List;

public class ExceptionBestPracticesDemo {
    public static void main(String[] args) {
        System.out.println("=== 异常处理最佳实践演示 ===\n");
        demonstrateEarlyValidation();
        demonstrateSpecificExceptions();
        demonstrateMeaningfulMessages();
        demonstrateResourceManagement();
        demonstrateFinallyReturn();
    }

    private static void demonstrateEarlyValidation() {
        System.out.println("1. 早期验证和快速失败:");
        try {
            processData("valid_data", 5);
            System.out.println("数据处理成功");
        } catch (IllegalArgumentException e) {
            System.out.println("参数验证失败: " + e.getMessage());
        }

        try {
            processData(null, -1);
        } catch (IllegalArgumentException e) {
            System.out.println("参数验证失败: " + e.getMessage());
        }
        System.out.println();
    }

    private static void demonstrateSpecificExceptions() {
        System.out.println("2. 具体异常优于通用异常:");
        try {
            findUserById(123);
        } catch (UserNotFoundException e) {
            System.out.println("用户未找到: " + e.getMessage());
        } catch (DatabaseConnectionException e) {
            System.out.println("数据库连接失败: " + e.getMessage());
        }

        try {
            findUserById(456);
        } catch (UserNotFoundException e) {
            System.out.println("用户未找到: " + e.getMessage());
        } catch (DatabaseConnectionException e) {
            System.out.println("数据库连接失败: " + e.getMessage());
        }
        System.out.println();
    }

    private static void demonstrateMeaningfulMessages() {
        System.out.println("3. 有意义的异常信息:");
        try {
            processOrder(null);
        } catch (InvalidOrderException e) {
            System.out.println("订单处理失败: " + e.getMessage());
        }

        Order order = new Order();
        try {
            processOrder(order);
        } catch (InvalidOrderException e) {
            System.out.println("订单处理失败: " + e.getMessage());
        }
        System.out.println();
    }

    private static void demonstrateResourceManagement() {
        System.out.println("4. try-with-resources资源管理:");
        try (FakeResource r1 = new FakeResource("DB连接");
             FakeResource r2 = new FakeResource("文件流")) {
            r1.doWork();
            r2.doWork();
        }
        System.out.println();
    }

    private static void demonstrateFinallyReturn() {
        System.out.println("5. finally中的返回值陷阱:");
        System.out.println("getResult() = " + getResult() + " (期望10，实际被finally覆盖为20)");
        System.out.println();
    }

    private static void processData(String data, int count) {
        if (data == null) {
            throw new IllegalArgumentException("数据不能为空");
        }
        if (count <= 0) {
            throw new IllegalArgumentException("计数必须大于0，当前值: " + count);
        }
        for (int i = 0; i < count; i++) {
            System.out.println("处理数据: " + data + " #" + (i + 1));
        }
    }

    private static void findUserById(long userId) throws UserNotFoundException, DatabaseConnectionException {
        if (userId == 123) {
            System.out.println("找到用户: 张三");
        } else if (userId == 789) {
            throw new DatabaseConnectionException("数据库连接超时");
        } else {
            throw new UserNotFoundException("用户ID " + userId + " 不存在");
        }
    }

    private static void processOrder(Order order) throws InvalidOrderException {
        if (order == null) {
            throw new InvalidOrderException("订单对象不能为空");
        }
        if (order.getItems().isEmpty()) {
            throw new InvalidOrderException("订单必须包含至少一个商品项");
        }
        System.out.println("订单处理成功");
    }

    private static int getResult() {
        try {
            return 10;
        } finally {
            return 20;
        }
    }

    static class FakeResource implements AutoCloseable {
        private final String name;
        FakeResource(String name) { this.name = name; System.out.println("打开: " + name); }
        void doWork() { System.out.println("使用: " + name); }
        @Override public void close() { System.out.println("关闭: " + name); }
    }

    static class UserNotFoundException extends Exception {
        UserNotFoundException(String message) { super(message); }
    }

    static class DatabaseConnectionException extends Exception {
        DatabaseConnectionException(String message) { super(message); }
    }

    static class InvalidOrderException extends Exception {
        InvalidOrderException(String message) { super(message); }
    }

    static class Order {
        private final List<String> items = new ArrayList<>();
        List<String> getItems() { return items; }
    }
}
