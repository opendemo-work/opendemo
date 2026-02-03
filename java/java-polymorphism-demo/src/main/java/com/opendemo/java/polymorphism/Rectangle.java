package com.opendemo.java.polymorphism;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Rectangle矩形类 - 演示具体类实现抽象类
 * 实现Shape抽象类的所有抽象方法
 */
public class Rectangle extends Shape {
    private static final Logger logger = LoggerFactory.getLogger(Rectangle.class);
    
    private double width;
    private double height;
    
    // 构造方法
    public Rectangle() {
        super();
        this.width = 1.0;
        this.height = 1.0;
        logger.info("创建了默认矩形");
    }
    
    public Rectangle(double width, double height) {
        super();
        this.width = width;
        this.height = height;
        logger.info("创建了矩形: {}×{}", width, height);
    }
    
    public Rectangle(double width, double height, String color, boolean filled) {
        super(color, filled);
        this.width = width;
        this.height = height;
        logger.info("创建了{}矩形: {}×{}", color, width, height);
    }
    
    // Getter和Setter方法
    public double getWidth() {
        return width;
    }
    
    public void setWidth(double width) {
        if (width > 0) {
            this.width = width;
        } else {
            logger.warn("宽度必须大于0: {}", width);
        }
    }
    
    public double getHeight() {
        return height;
    }
    
    public void setHeight(double height) {
        if (height > 0) {
            this.height = height;
        } else {
            logger.warn("高度必须大于0: {}", height);
        }
    }
    
    // 实现抽象方法
    @Override
    public double getArea() {
        return width * height;
    }
    
    @Override
    public double getPerimeter() {
        return 2 * (width + height);
    }
    
    @Override
    public void draw() {
        logger.info("绘制矩形: 宽度={}, 高度={}", width, height);
        if (filled) {
            logger.info("使用{}颜色填充矩形", color);
        }
    }
    
    // 重写钩子方法
    @Override
    protected void prepareCanvas() {
        logger.info("准备绘图区域，设置坐标系");
    }
    
    @Override
    protected void fill() {
        logger.info("用{}色填充矩形区域", color);
    }
    
    // 矩形特有方法
    public boolean isSquare() {
        return Math.abs(width - height) < 0.001; // 考虑浮点数精度
    }
    
    public void resize(double scale) {
        if (scale > 0) {
            width *= scale;
            height *= scale;
            logger.info("矩形缩放至: {}×{}", width, height);
        } else {
            logger.warn("缩放比例必须大于0: {}", scale);
        }
    }
    
    @Override
    public String toString() {
        return String.format("Rectangle[width=%.1f, height=%.1f, color='%s', filled=%s]", 
                           width, height, color, filled);
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Rectangle rectangle = (Rectangle) obj;
        return Double.compare(rectangle.width, width) == 0 &&
               Double.compare(rectangle.height, height) == 0 &&
               filled == rectangle.filled &&
               color.equals(rectangle.color);
    }
    
    @Override
    public int hashCode() {
        return color.hashCode() + (int)(width * 100) + (int)(height * 100) + (filled ? 1 : 0);
    }
}