package com.opendemo.java.inheritance;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Mammal哺乳动物类 - 演示继承和方法重写
 * 继承Animal类，添加哺乳动物特有的属性和方法
 */
public class Mammal extends Animal {
    private static final Logger logger = LoggerFactory.getLogger(Mammal.class);
    
    // 哺乳动物特有属性
    private boolean hasFur;
    private int gestationPeriod; // 妊娠期（天）
    private String furColor;
    
    // 构造方法
    public Mammal() {
        super(); // 调用父类无参构造方法
        this.hasFur = true;
        this.gestationPeriod = 0;
        this.furColor = "棕色";
        this.species = "哺乳动物";
        logger.info("创建了哺乳动物对象");
    }
    
    public Mammal(String name, int age, double weight, boolean hasFur, int gestationPeriod, String furColor) {
        // 调用父类四参构造方法
        super(name, age, weight, "哺乳动物");
        this.hasFur = hasFur;
        this.gestationPeriod = gestationPeriod;
        this.furColor = furColor;
        logger.info("创建了哺乳动物: {}, 毛发: {}, 妊娠期: {}天", name, hasFur ? "有" : "无", gestationPeriod);
    }
    
    // Getter和Setter方法
    public boolean hasFur() {
        return hasFur;
    }
    
    public void setHasFur(boolean hasFur) {
        this.hasFur = hasFur;
    }
    
    public int getGestationPeriod() {
        return gestationPeriod;
    }
    
    public void setGestationPeriod(int gestationPeriod) {
        if (gestationPeriod >= 0) {
            this.gestationPeriod = gestationPeriod;
        } else {
            logger.warn("妊娠期不能为负数: {}", gestationPeriod);
        }
    }
    
    public String getFurColor() {
        return furColor;
    }
    
    public void setFurColor(String furColor) {
        this.furColor = furColor;
    }
    
    // 重写父类方法
    @Override
    public void makeSound() {
        logger.info("{}发出哺乳动物特有的声音", name);
    }
    
    @Override
    public void move() {
        logger.info("{}用四肢行走", name);
    }
    
    // 哺乳动物特有方法
    public void nurse() {
        logger.info("{}正在哺乳幼崽", name);
    }
    
    public void regulateBodyTemperature() {
        logger.info("{}正在调节体温", name);
    }
    
    public void giveBirth() {
        if (gestationPeriod > 0) {
            logger.info("{}经过{}天妊娠期后诞下幼崽", name, gestationPeriod);
        } else {
            logger.info("{}是卵生哺乳动物", name);
        }
    }
    
    @Override
    public void showInfo() {
        super.showInfo(); // 调用父类方法显示基本信息
        logger.info("=== 哺乳动物特有信息 ===");
        logger.info("是否有毛发: {}", hasFur ? "是" : "否");
        logger.info("毛发颜色: {}", furColor);
        logger.info("妊娠期: {}天", gestationPeriod);
    }
    
    // 重写toString方法
    @Override
    public String toString() {
        return String.format("Mammal[name='%s', age=%d, weight=%.1fkg, fur=%s, color='%s']", 
                           name, age, weight, hasFur ? "有" : "无", furColor);
    }
    
    // 使用super关键字的示例方法
    public void demonstrateSuperUsage() {
        logger.info("=== super关键字使用演示 ===");
        // 调用父类方法
        super.makeSound();
        // 调用父类变量（通过getter）
        logger.info("父类species: {}", super.getSpecies());
        // 调用父类构造方法已在构造器中演示
    }
}