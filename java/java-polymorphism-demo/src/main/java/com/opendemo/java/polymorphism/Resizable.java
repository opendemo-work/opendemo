package com.opendemo.java.polymorphism;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Resizable接口 - 演示多重接口实现
 * 定义可调整大小对象的行为
 */
public interface Resizable {
    Logger logger = LoggerFactory.getLogger(Resizable.class);
    
    // 抽象方法
    void resize(double factor);
    double getSize();
    
    // 默认方法
    default void scaleUp() {
        resize(1.5);
        logger.info("放大1.5倍");
    }
    
    default void scaleDown() {
        resize(0.5);
        logger.info("缩小至0.5倍");
    }
    
    default boolean isResizable() {
        return true;
    }
    
    // 静态方法
    static Resizable createResizable(double initialSize) {
        return new Resizable() {
            private double size = initialSize;
            
            @Override
            public void resize(double factor) {
                if (factor > 0) {
                    size *= factor;
                    logger.info("调整大小至: {}", size);
                }
            }
            
            @Override
            public double getSize() {
                return size;
            }
        };
    }
    
    // 私有辅助方法
    private void validateFactor(double factor) {
        if (factor <= 0) {
            throw new IllegalArgumentException("缩放因子必须大于0: " + factor);
        }
    }
}