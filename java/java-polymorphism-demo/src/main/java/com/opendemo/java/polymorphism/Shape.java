package com.opendemo.java.polymorphism;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Shape抽象类 - 演示抽象类多态
 * 定义图形的通用行为和属性
 */
public abstract class Shape {
    protected static final Logger logger = LoggerFactory.getLogger(Shape.class);
    
    protected String color;
    protected boolean filled;
    
    // 构造方法
    public Shape() {
        this.color = "白色";
        this.filled = false;
        logger.info("创建了Shape对象");
    }
    
    public Shape(String color, boolean filled) {
        this.color = color;
        this.filled = filled;
        logger.info("创建了{}形状，填充状态: {}", color, filled ? "已填充" : "未填充");
    }
    
    // Getter和Setter方法
    public String getColor() {
        return color;
    }
    
    public void setColor(String color) {
        this.color = color;
    }
    
    public boolean isFilled() {
        return filled;
    }
    
    public void setFilled(boolean filled) {
        this.filled = filled;
    }
    
    // 抽象方法 - 子类必须实现
    public abstract double getArea();
    public abstract double getPerimeter();
    public abstract void draw();
    
    // 具体方法 - 子类可以继承使用
    public void displayInfo() {
        logger.info("=== 图形信息 ===");
        logger.info("颜色: {}", color);
        logger.info("填充状态: {}", filled ? "已填充" : "未填充");
        logger.info("面积: {}", String.format("%.2f", getArea()));
        logger.info("周长: {}", String.format("%.2f", getPerimeter()));
    }
    
    // 模板方法 - 定义算法骨架
    public final void render() {
        logger.info("开始渲染{}图形", color);
        prepareCanvas();
        draw();
        if (filled) {
            fill();
        }
        finishRendering();
        logger.info("图形渲染完成");
    }
    
    // 钩子方法 - 子类可以选择性重写
    protected void prepareCanvas() {
        logger.info("准备画布");
    }
    
    protected void fill() {
        logger.info("填充{}颜色", color);
    }
    
    protected void finishRendering() {
        logger.info("完成渲染");
    }
    
    @Override
    public String toString() {
        return String.format("%s[color='%s', filled=%s, area=%.2f, perimeter=%.2f]", 
                           getClass().getSimpleName(), color, filled, getArea(), getPerimeter());
    }
}