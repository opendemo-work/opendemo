package com.opendemo.java.inheritance;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Dog狗类 - 演示多层继承
 * 继承Mammal类，展示更具体的动物类别
 */
public class Dog extends Mammal {
    private static final Logger logger = LoggerFactory.getLogger(Dog.class);
    
    // 狗特有属性
    private String breed;      // 品种
    private boolean isTrained; // 是否经过训练
    private String favoriteToy; // 最喜欢的玩具
    
    // 构造方法
    public Dog() {
        super(); // 调用父类构造方法
        this.breed = "混血犬";
        this.isTrained = false;
        this.favoriteToy = "球";
        this.species = "犬类";
        logger.info("创建了狗对象");
    }
    
    public Dog(String name, int age, double weight, String breed, boolean isTrained, String favoriteToy) {
        // 调用父类构造方法
        super(name, age, weight, true, 63, "多种颜色");
        this.breed = breed;
        this.isTrained = isTrained;
        this.favoriteToy = favoriteToy;
        this.species = "犬类";
        logger.info("创建了{}: {}, 品种: {}, 训练状态: {}", 
                   isTrained ? "训练犬" : "未训练犬", name, breed, isTrained ? "已训练" : "未训练");
    }
    
    // Getter和Setter方法
    public String getBreed() {
        return breed;
    }
    
    public void setBreed(String breed) {
        this.breed = breed;
    }
    
    public boolean isTrained() {
        return isTrained;
    }
    
    public void setTrained(boolean trained) {
        isTrained = trained;
    }
    
    public String getFavoriteToy() {
        return favoriteToy;
    }
    
    public void setFavoriteToy(String favoriteToy) {
        this.favoriteToy = favoriteToy;
    }
    
    // 重写父类方法
    @Override
    public void makeSound() {
        logger.info("{}汪汪叫", name);
    }
    
    @Override
    public void move() {
        logger.info("{}奔跑着移动", name);
    }
    
    @Override
    public void eat(String food) {
        logger.info("{}兴奋地吃{}", name, food);
        wagTail();
    }
    
    // 狗特有方法
    public void bark() {
        logger.info("{}大声汪汪叫", name);
    }
    
    public void wagTail() {
        logger.info("{}摇尾巴表示高兴", name);
    }
    
    public void fetch(String item) {
        logger.info("{}去捡回{}", name, item);
        wagTail();
    }
    
    public void sit() {
        logger.info("{}坐下", name);
    }
    
    public void stay() {
        logger.info("{}保持不动", name);
    }
    
    public void rollOver() {
        logger.info("{}打滚", name);
        wagTail();
    }
    
    public void train() {
        logger.info("开始训练{}", name);
        // 训练过程
        sit();
        stay();
        rollOver();
        isTrained = true;
        logger.info("{}训练完成，现在是训练犬", name);
    }
    
    @Override
    public void showInfo() {
        super.showInfo(); // 调用父类方法
        logger.info("=== 狗特有信息 ===");
        logger.info("品种: {}", breed);
        logger.info("训练状态: {}", isTrained ? "已训练" : "未训练");
        logger.info("最喜欢的食物: {}", favoriteToy);
    }
    
    // 重写toString方法
    @Override
    public String toString() {
        return String.format("Dog[name='%s', breed='%s', age=%d, trained=%s]", 
                           name, breed, age, isTrained ? "是" : "否");
    }
    
    // 演示方法重写的动态绑定
    public void demonstratePolymorphism(Animal animal) {
        logger.info("=== 多态演示 ===");
        logger.info("传入的动物: {}", animal.getClass().getSimpleName());
        animal.makeSound(); // 运行时决定调用哪个方法
        animal.move();
    }
}