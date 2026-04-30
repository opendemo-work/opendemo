package com.opendemo.java.exceptions;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.sql.SQLException;

public class ExceptionBasicsDemo {
    public static void main(String[] args) {
        System.out.println("=== Java异常处理基础演示 ===\n");
        demonstrateTryCatchFinally();
        demonstrateMultiCatch();
        demonstrateThrowsKeyword();
        demonstrateThrowKeyword();
        demonstrateTryWithResources();
    }

    private static void demonstrateTryCatchFinally() {
        System.out.println("1. try-catch-finally基本用法:");
        try {
            int result = 10 / 0;
            System.out.println("结果: " + result);
        } catch (ArithmeticException e) {
            System.out.println("捕获到算术异常: " + e.getMessage());
        } finally {
            System.out.println("finally块总是执行");
        }

        try {
            int[] numbers = {1, 2, 3};
            System.out.println("访问数组元素: " + numbers[5]);
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("数组越界异常: " + e.getMessage());
        }

        try {
            String str = null;
            System.out.println("字符串长度: " + str.length());
        } catch (NullPointerException e) {
            System.out.println("空指针异常: " + e.getMessage());
        }
        System.out.println();
    }

    private static void demonstrateMultiCatch() {
        System.out.println("2. 多重catch块演示:");
        try {
            int[] array = {1, 2, 3};
            int idx = 5;
            int val = array[idx];
            int result = 10 / val;
            System.out.println("结果: " + result);
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("数组越界: " + e.getMessage());
        } catch (ArithmeticException e) {
            System.out.println("算术错误: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("其他异常: " + e.getMessage());
        }

        try {
            Object obj = "hello";
            Integer num = (Integer) obj;
        } catch (ClassCastException e) {
            System.out.println("类型转换异常: " + e.getMessage());
        }
        System.out.println();
    }

    private static void demonstrateThrowsKeyword() {
        System.out.println("3. throws关键字演示:");
        try {
            readFile("nonexistent.txt");
        } catch (FileNotFoundException e) {
            System.out.println("文件未找到: " + e.getMessage());
        } catch (IOException e) {
            System.out.println("IO异常: " + e.getMessage());
        }

        try {
            connectToDatabase();
        } catch (SQLException e) {
            System.out.println("数据库连接失败: " + e.getMessage());
        }
        System.out.println();
    }

    private static void demonstrateThrowKeyword() {
        System.out.println("4. throw关键字演示:");
        try {
            validateAge(15);
        } catch (IllegalArgumentException e) {
            System.out.println("年龄验证失败: " + e.getMessage());
        }

        try {
            processUserData(null);
        } catch (NullPointerException e) {
            System.out.println("用户数据处理异常: " + e.getMessage());
        }
        System.out.println();
    }

    private static void demonstrateTryWithResources() {
        System.out.println("5. try-with-resources演示:");
        try (FakeResource resource = new FakeResource("test-resource")) {
            resource.doWork();
        } catch (Exception e) {
            System.out.println("资源使用异常: " + e.getMessage());
        }
        System.out.println();
    }

    private static void readFile(String filename) throws FileNotFoundException, IOException {
        FileInputStream fis = new FileInputStream(filename);
        fis.close();
    }

    private static void connectToDatabase() throws SQLException {
        throw new SQLException("无法连接到数据库服务器");
    }

    private static void validateAge(int age) {
        if (age < 18) {
            throw new IllegalArgumentException("年龄必须大于等于18岁，当前年龄: " + age);
        }
        System.out.println("年龄验证通过: " + age);
    }

    private static void processUserData(String userData) {
        if (userData == null) {
            throw new NullPointerException("用户数据不能为空");
        }
        System.out.println("处理用户数据: " + userData);
    }

    static class FakeResource implements AutoCloseable {
        private final String name;

        FakeResource(String name) {
            this.name = name;
            System.out.println("打开资源: " + name);
        }

        void doWork() {
            System.out.println("使用资源: " + name);
        }

        @Override
        public void close() {
            System.out.println("自动关闭资源: " + name);
        }
    }
}
