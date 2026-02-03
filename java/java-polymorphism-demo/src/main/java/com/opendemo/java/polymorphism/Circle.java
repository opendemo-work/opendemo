package com.opendemo.java.polymorphism;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Circle圆形类 - 演示另一个具体类实现抽象类
 * 展示不同的几何图形实现
 */
public class Circle extends Shape {
    private static final Logger logger = LoggerFactory.getLogger(Circle.class);
    
    private double radius;
    
    // 构造方法
    public Circle() {
        super();
        this.radius = 1.0;
        logger.info("创建了默认圆形");
    }
    
    public Circle(double radius) {
        super();
        this.radius = radius;
        logger.info("创建了圆形: 半径={}", radius);
    }
    
    public Circle(double radius, String color, boolean filled) {
        super(color, filled);
        this.radius = radius;
        logger.info("创建了{}圆形: 半径={}", color, radius);
    }
    
    // Getter和Setter方法
    public double getRadius() {
        return radius;
    }
    
    public void setRadius(double radius) {
        if (radius > 0) {
            this.radius = radius;
        } else {
            logger.warn("半径必须大于0: {}", radius);
        }
    }
    
    // 实现抽象方法
    @Override
    public double getArea() {
        return Math.PI * radius * radius;
    }
    
    @Override
    public double getPerimeter() {
        return 2 * Math.PI * radius;
    }
    
    @Override
    public void draw() {
        logger.info("绘制圆形: 半径={}", radius);
        if (filled) {
            logger.info("使用{}颜色填充圆形", color);
        }
    }
    
    // 重写钩子方法
    @Override
    protected void prepareCanvas() {
        logger.info("准备绘图画布，设置圆心坐标");
    }
    
    @Override
    protected void fill() {
        logger.info("用{}色填充圆形区域", color);
    }
    
    // 圆形特有方法
    public double getDiameter() {
        return 2 * radius;
    }
    
    public double getCircumference() {
        return getPerimeter();
    }
    
    public boolean containsPoint(double x, double y) {
        // 假设圆心在原点(0,0)
        double distance = Math.sqrt(x * x + y * y);
        return distance <= radius;
    }
    
    public void scale(double factor) {
        if (factor > 0) {
            radius *= factor;
            logger.info("圆形缩放至半径: {}", radius);
        } else {
            logger.warn("缩放因子必须大于0: {}", factor);
        }
    }
    
    public static Circle createUnitCircle() {
        return new Circle(1.0, "黑色", false);
    }
    
    public static Circle createFromDiameter(double diameter) {
        return new Circle(diameter / 2.0);
    }
    
    @Override
    public String toString() {
        return String.format("Circle[radius=%.1f, color='%s', filled=%s]", 
                           radius, color, filled);
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Circle circle = (Circle) obj;
        return Double.compare(circle.radius, radius) == 0 &&
               filled == circle.filled &&
               color.equals(circle.color);
    }
    
    @Override
    public int hashCode() {
        return color.hashCode() + (int)(radius * 100) + (filled ? 1 : 0);
    }
}