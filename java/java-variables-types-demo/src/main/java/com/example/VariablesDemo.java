package com.example;

/**
 * Java变量与数据类型演示程序
 * 展示各种数据类型的声明、使用和转换
 * 
 * @author OpenDemo Team
 * @version 1.0.0
 */
public class VariablesDemo {
    
    public static void main(String[] args) {
        System.out.println("=== Java变量与数据类型演示 ===\n");
        
        // 1. 整数类型演示
        demonstrateIntegerTypes();
        
        // 2. 浮点类型演示
        demonstrateFloatingPointTypes();
        
        // 3. 字符和布尔类型演示
        demonstrateCharBooleanTypes();
        
        // 4. 字符串类型演示
        demonstrateStringType();
        
        // 5. 数组类型演示
        demonstrateArrayTypes();
        
        // 6. 类型转换演示
        demonstrateTypeConversion();
        
        // 7. 常量演示
        demonstrateConstants();
    }
    
    /**
     * 演示整数类型
     */
    private static void demonstrateIntegerTypes() {
        System.out.println("1. 整数类型演示:");
        
        // byte类型 (-128 到 127)
        byte smallNumber = 100;
        System.out.println("byte: " + smallNumber);
        
        // short类型 (-32,768 到 32,767)
        short mediumNumber = 30000;
        System.out.println("short: " + mediumNumber);
        
        // int类型 (默认整数类型)
        int regularNumber = 2000000000;
        System.out.println("int: " + regularNumber);
        
        // long类型 (需要L后缀)
        long bigNumber = 9000000000L;
        System.out.println("long: " + bigNumber);
        
        System.out.println();
    }
    
    /**
     * 演示浮点类型
     */
    private static void demonstrateFloatingPointTypes() {
        System.out.println("2. 浮点类型演示:");
        
        // float类型 (需要F后缀)
        float price = 19.99F;
        System.out.println("float: " + price);
        
        // double类型 (默认小数类型)
        double preciseValue = 3.14159265359;
        System.out.println("double: " + preciseValue);
        
        System.out.println();
    }
    
    /**
     * 演示字符和布尔类型
     */
    private static void demonstrateCharBooleanTypes() {
        System.out.println("3. 字符和布尔类型演示:");
        
        // char类型 (单个字符，用单引号)
        char letter = 'A';
        char unicodeChar = '\u0041'; // Unicode表示
        System.out.println("char: " + letter + ", Unicode: " + unicodeChar);
        
        // boolean类型
        boolean isJavaFun = true;
        boolean isFinished = false;
        System.out.println("boolean true: " + isJavaFun);
        System.out.println("boolean false: " + isFinished);
        
        System.out.println();
    }
    
    /**
     * 演示字符串类型
     */
    private static void demonstrateStringType() {
        System.out.println("4. 字符串类型演示:");
        
        // String是引用类型，不是基本类型
        String greeting = "Hello";
        String name = "World";
        
        // 字符串连接
        String message = greeting + " " + name + "!";
        System.out.println("字符串连接: " + message);
        
        // 字符串长度
        System.out.println("字符串长度: " + message.length());
        
        // 字符串方法
        System.out.println("转大写: " + message.toUpperCase());
        System.out.println("包含'World': " + message.contains("World"));
        
        System.out.println();
    }
    
    /**
     * 演示数组类型
     */
    private static void demonstrateArrayTypes() {
        System.out.println("5. 数组类型演示:");
        
        // 整数数组
        int[] numbers = {1, 2, 3, 4, 5};
        System.out.println("整数数组长度: " + numbers.length);
        System.out.println("第一个元素: " + numbers[0]);
        
        // 字符串数组
        String[] fruits = {"苹果", "香蕉", "橙子"};
        System.out.println("水果数组:");
        for (String fruit : fruits) {
            System.out.println("  - " + fruit);
        }
        
        System.out.println();
    }
    
    /**
     * 演示类型转换
     */
    private static void demonstrateTypeConversion() {
        System.out.println("6. 类型转换演示:");
        
        // 自动类型转换 (隐式转换)
        int intValue = 100;
        long longValue = intValue; // int可以自动转换为long
        System.out.println("自动转换 int->long: " + longValue);
        
        // 强制类型转换 (显式转换)
        double doubleValue = 99.99;
        int convertedInt = (int) doubleValue; // 丢失小数部分
        System.out.println("强制转换 double->int: " + convertedInt);
        
        // 字符串与其他类型的转换
        String numberStr = "123";
        int parsedInt = Integer.parseInt(numberStr);
        System.out.println("字符串转整数: " + parsedInt);
        
        int age = 25;
        String ageStr = String.valueOf(age);
        System.out.println("整数转字符串: " + ageStr);
        
        System.out.println();
    }
    
    /**
     * 演示常量使用
     */
    private static void demonstrateConstants() {
        System.out.println("7. 常量演示:");
        
        // 使用final关键字声明常量
        final double PI = 3.14159;
        final String COMPANY_NAME = "OpenDemo";
        
        System.out.println("圆周率 PI = " + PI);
        System.out.println("公司名称 = " + COMPANY_NAME);
        
        // 常量一旦赋值就不能修改
        // PI = 3.14; // 这行会编译错误
        
        System.out.println();
    }
}