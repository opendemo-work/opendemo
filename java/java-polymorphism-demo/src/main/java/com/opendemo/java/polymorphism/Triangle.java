package com.opendemo.java.polymorphism;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Triangle三角形类 - 演示多重继承（实现多个接口）
 * 同时实现Shape抽象类和多个接口
 */
public class Triangle extends Shape implements Drawable, Resizable {
    private static final Logger logger = LoggerFactory.getLogger(Triangle.class);
    
    private double sideA;
    private double sideB;
    private double sideC;
    
    // 构造方法
    public Triangle() {
        super();
        this.sideA = 1.0;
        this.sideB = 1.0;
        this.sideC = 1.0;
        logger.info("创建了默认三角形");
    }
    
    public Triangle(double sideA, double sideB, double sideC) {
        super();
        this.sideA = sideA;
        this.sideB = sideB;
        this.sideC = sideC;
        logger.info("创建了三角形: 边长={}, {}, {}", sideA, sideB, sideC);
    }
    
    public Triangle(double sideA, double sideB, double sideC, String color, boolean filled) {
        super(color, filled);
        this.sideA = sideA;
        this.sideB = sideB;
        this.sideC = sideC;
        logger.info("创建了{}三角形: 边长={}, {}, {}", color, sideA, sideB, sideC);
    }
    
    // Getter和Setter方法
    public double getSideA() {
        return sideA;
    }
    
    public void setSideA(double sideA) {
        if (sideA > 0) {
            this.sideA = sideA;
        } else {
            logger.warn("边长必须大于0: {}", sideA);
        }
    }
    
    public double getSideB() {
        return sideB;
    }
    
    public void setSideB(double sideB) {
        if (sideB > 0) {
            this.sideB = sideB;
        } else {
            logger.warn("边长必须大于0: {}", sideB);
        }
    }
    
    public double getSideC() {
        return sideC;
    }
    
    public void setSideC(double sideC) {
        if (sideC > 0) {
            this.sideC = sideC;
        } else {
            logger.warn("边长必须大于0: {}", sideC);
        }
    }
    
    // 实现Shape抽象方法
    @Override
    public double getArea() {
        // 使用海伦公式计算三角形面积
        double s = getPerimeter() / 2;
        return Math.sqrt(s * (s - sideA) * (s - sideB) * (s - sideC));
    }
    
    @Override
    public double getPerimeter() {
        return sideA + sideB + sideC;
    }
    
    @Override
    public void draw() {
        logger.info("绘制三角形: 边长={}, {}, {}", sideA, sideB, sideC);
        if (filled) {
            logger.info("使用{}颜色填充三角形", color);
        }
    }
    
    // 实现Drawable接口方法
    @Override
    public void erase() {
        logger.info("擦除三角形");
    }
    
    // 实现Resizable接口方法
    @Override
    public void resize(double factor) {
        if (factor > 0) {
            sideA *= factor;
            sideB *= factor;
            sideC *= factor;
            logger.info("三角形缩放至: 边长={}, {}, {}", sideA, sideB, sideC);
        } else {
            logger.warn("缩放因子必须大于0: {}", factor);
        }
    }
    
    @Override
    public double getSize() {
        return getArea(); // 以面积作为大小指标
    }
    
    // 三角形特有方法
    public boolean isValid() {
        // 三角形存在条件：任意两边之和大于第三边
        return (sideA + sideB > sideC) && 
               (sideA + sideC > sideB) && 
               (sideB + sideC > sideA);
    }
    
    public boolean isEquilateral() {
        // 等边三角形
        return Math.abs(sideA - sideB) < 0.001 && 
               Math.abs(sideB - sideC) < 0.001;
    }
    
    public boolean isIsosceles() {
        // 等腰三角形
        return Math.abs(sideA - sideB) < 0.001 || 
               Math.abs(sideA - sideC) < 0.001 || 
               Math.abs(sideB - sideC) < 0.001;
    }
    
    public boolean isRightTriangle() {
        // 直角三角形（勾股定理）
        double[] sides = {sideA, sideB, sideC};
        java.util.Arrays.sort(sides);
        double a = sides[0];
        double b = sides[1];
        double c = sides[2]; // 最长边
        return Math.abs(a*a + b*b - c*c) < 0.001;
    }
    
    public void rotate(double angle) {
        logger.info("旋转三角形{}度", angle);
    }
    
    @Override
    public String toString() {
        return String.format("Triangle[a=%.1f, b=%.1f, c=%.1f, color='%s', filled=%s]", 
                           sideA, sideB, sideC, color, filled);
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Triangle triangle = (Triangle) obj;
        return Double.compare(triangle.sideA, sideA) == 0 &&
               Double.compare(triangle.sideB, sideB) == 0 &&
               Double.compare(triangle.sideC, sideC) == 0 &&
               filled == triangle.filled &&
               color.equals(triangle.color);
    }
    
    @Override
    public int hashCode() {
        return color.hashCode() + 
               (int)(sideA * 100) + 
               (int)(sideB * 100) + 
               (int)(sideC * 100) + 
               (filled ? 1 : 0);
    }
}