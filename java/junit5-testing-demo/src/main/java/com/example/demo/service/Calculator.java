package com.example.demo.service;

/**
 * 计算器类
 * 
 * 用于演示JUnit5基础测试
 */
public class Calculator {
    
    /**
     * 加法
     */
    public int add(int a, int b) {
        return a + b;
    }
    
    /**
     * 减法
     */
    public int subtract(int a, int b) {
        return a - b;
    }
    
    /**
     * 乘法
     */
    public int multiply(int a, int b) {
        return a * b;
    }
    
    /**
     * 除法
     * 
     * @throws ArithmeticException 除数为0时抛出
     */
    public int divide(int a, int b) {
        if (b == 0) {
            throw new ArithmeticException("除数不能为0");
        }
        return a / b;
    }
    
    /**
     * 求平方根
     */
    public double sqrt(double a) {
        if (a < 0) {
            throw new IllegalArgumentException("不能对负数求平方根");
        }
        return Math.sqrt(a);
    }
    
    /**
     * 判断是否为偶数
     */
    public boolean isEven(int number) {
        return number % 2 == 0;
    }
}
