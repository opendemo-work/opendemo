package com.opendemo.java.polymorphism;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Drawable接口 - 演示接口多态
 * 定义可绘制对象的标准行为
 */
public interface Drawable {
    Logger logger = LoggerFactory.getLogger(Drawable.class);
    
    // 抽象方法
    void draw();
    void erase();
    
    // 默认方法 - Java 8+特性
    default void display() {
        logger.info("显示可绘制对象");
        draw();
    }
    
    default void hide() {
        logger.info("隐藏可绘制对象");
        erase();
    }
    
    // 静态方法 - Java 8+特性
    static void showInfo() {
        logger.info("Drawable接口 - 定义可绘制对象的标准");
    }
    
    // 私有方法 - Java 9+特性
    private void logOperation(String operation) {
        logger.info("执行操作: {}", operation);
    }
    
    // 私有静态方法 - Java 9+特性
    private static void validateDrawing() {
        logger.info("验证绘图参数");
    }
}