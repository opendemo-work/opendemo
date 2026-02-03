package com.opendemo.java.inheritance;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Bird鸟类 - 演示不同的继承路径
 * 继承Animal类，展示鸟类特有的属性和方法
 */
public class Bird extends Animal {
    private static final Logger logger = LoggerFactory.getLogger(Bird.class);
    
    // 鸟类特有属性
    private boolean canFly;
    private double wingspan;   // 翼展（厘米）
    private String featherColor;
    private boolean migrates;  // 是否迁徙
    
    // 构造方法
    public Bird() {
        super();
        this.canFly = true;
        this.wingspan = 0.0;
        this.featherColor = "彩色";
        this.migrates = false;
        this.species = "鸟类";
        logger.info("创建了鸟对象");
    }
    
    public Bird(String name, int age, double weight, boolean canFly, double wingspan, 
                String featherColor, boolean migrates) {
        super(name, age, weight, "鸟类");
        this.canFly = canFly;
        this.wingspan = wingspan;
        this.featherColor = featherColor;
        this.migrates = migrates;
        logger.info("创建了{}: {}, 飞行能力: {}, 翼展: {}cm", 
                   migrates ? "候鸟" : "留鸟", name, canFly ? "会飞" : "不会飞", wingspan);
    }
    
    // Getter和Setter方法
    public boolean canFly() {
        return canFly;
    }
    
    public void setCanFly(boolean canFly) {
        this.canFly = canFly;
    }
    
    public double getWingspan() {
        return wingspan;
    }
    
    public void setWingspan(double wingspan) {
        if (wingspan >= 0) {
            this.wingspan = wingspan;
        } else {
            logger.warn("翼展不能为负数: {}", wingspan);
        }
    }
    
    public String getFeatherColor() {
        return featherColor;
    }
    
    public void setFeatherColor(String featherColor) {
        this.featherColor = featherColor;
    }
    
    public boolean isMigrates() {
        return migrates;
    }
    
    public void setMigrates(boolean migrates) {
        this.migrates = migrates;
    }
    
    // 重写父类方法
    @Override
    public void makeSound() {
        logger.info("{}啾啾叫", name);
    }
    
    @Override
    public void move() {
        if (canFly) {
            logger.info("{}在空中飞翔", name);
        } else {
            logger.info("{}在地上行走", name);
        }
    }
    
    @Override
    public void eat(String food) {
        logger.info("{}啄食{}", name, food);
        preenFeathers();
    }
    
    // 鸟类特有方法
    public void fly() {
        if (canFly) {
            logger.info("{}展开{}cm的翅膀开始飞翔", name, wingspan);
        } else {
            logger.info("{}是不能飞行的鸟类", name);
        }
    }
    
    public void sing() {
        logger.info("{}美妙地歌唱", name);
    }
    
    public void buildNest() {
        logger.info("{}正在筑巢", name);
    }
    
    public void layEggs(int eggCount) {
        logger.info("{}产下了{}个蛋", name, eggCount);
    }
    
    public void migrate() {
        if (migrates) {
            logger.info("{}开始季节性迁徙", name);
        } else {
            logger.info("{}是留鸟，不进行迁徙", name);
        }
    }
    
    public void preenFeathers() {
        logger.info("{}正在梳理{}的羽毛", name, featherColor);
    }
    
    @Override
    public void showInfo() {
        super.showInfo();
        logger.info("=== 鸟类特有信息 ===");
        logger.info("飞行能力: {}", canFly ? "会飞" : "不会飞");
        logger.info("翼展: {}cm", wingspan);
        logger.info("羽毛颜色: {}", featherColor);
        logger.info("迁徙习性: {}", migrates ? "候鸟" : "留鸟");
    }
    
    // 重写toString方法
    @Override
    public String toString() {
        return String.format("Bird[name='%s', fly=%s, wingspan=%.1fcm, color='%s']", 
                           name, canFly ? "会飞" : "不会飞", wingspan, featherColor);
    }
    
    // 静态工具方法
    public static double calculateFlightSpeed(Bird bird) {
        if (bird == null || !bird.canFly()) {
            return 0.0;
        }
        // 简单的飞行速度计算公式
        return bird.wingspan * 0.5; // 翼展的一半作为速度（km/h）
    }
    
    public static boolean isLargeBird(Bird bird) {
        if (bird == null) return false;
        return bird.wingspan > 150; // 翼展超过150cm为大型鸟类
    }
}