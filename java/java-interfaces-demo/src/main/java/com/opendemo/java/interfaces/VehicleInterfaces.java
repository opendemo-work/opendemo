package com.opendemo.java.interfaces;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

// 基础接口定义
interface Vehicle {
    Logger logger = LoggerFactory.getLogger(Vehicle.class);
    
    // 抽象方法
    void start();
    void stop();
    void accelerate(int speed);
    
    // 默认方法 (Java 8+)
    default void honk() {
        logger.info("车辆鸣笛");
    }
    
    default boolean isRunning() {
        return false;
    }
    
    // 静态方法 (Java 8+)
    static void showVehicleInfo() {
        logger.info("这是车辆接口，定义了通用的车辆行为");
    }
    
    // 私有方法 (Java 9+)
    private void logOperation(String operation) {
        logger.info("执行操作: {}", operation);
    }
}

// 函数式接口 (Java 8+) - 只有一个抽象方法
@FunctionalInterface
interface Engine {
    void startEngine();
    
    // 可以有多个默认方法和静态方法
    default void warmUp() {
        LoggerFactory.getLogger(Engine.class).info("发动机预热");
    }
    
    static Engine createElectricEngine() {
        return () -> LoggerFactory.getLogger(Engine.class).info("电动发动机启动");
    }
}

// 标记接口 - 不包含任何方法
interface SerializableMarker {}

// 多继承接口
interface FlyingVehicle extends Vehicle {
    void takeOff();
    void land();
    
    default void fly() {
        takeOff();
        LoggerFactory.getLogger(FlyingVehicle.class).info("飞行中...");
        land();
    }
}

// 服务提供者接口
interface PaymentProcessor {
    boolean processPayment(double amount);
    String getProcessorName();
    
    default void validateAmount(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("支付金额必须大于0");
        }
    }
}