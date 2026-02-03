package com.opendemo.java.inheritance;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Java继承机制演示程序
 * 展示类继承、方法重写、super关键字、多层继承等核心概念
 */
public class InheritanceDemo {
    private static final Logger logger = LoggerFactory.getLogger(InheritanceDemo.class);
    
    public static void main(String[] args) {
        logger.info("=== Java继承机制完整演示 ===");
        
        InheritanceDemo demo = new InheritanceDemo();
        
        demo.demonstrateBasicInheritance();
        demo.demonstrateMethodOverriding();
        demo.demonstrateSuperKeyword();
        demo.demonstrateMultiLevelInheritance();
        demo.demonstratePolymorphism();
        demo.demonstrateStaticMembers();
        
        logger.info("=== 演示完成 ===");
    }
    
    /**
     * 演示基本继承概念
     */
    public void demonstrateBasicInheritance() {
        logger.info("--- 基本继承演示 ---");
        
        // 创建不同类型的动物
        Animal genericAnimal = new Animal("普通动物", 5, 10.5, "未知物种");
        Mammal mammal = new Mammal("哺乳动物", 3, 15.2, true, 90, "棕色");
        Dog dog = new Dog("旺财", 2, 8.0, "金毛", true, "飞盘");
        Bird bird = new Bird("小鸟", 1, 0.2, true, 30.5, "蓝色", true);
        
        // 调用各自的方法
        genericAnimal.showInfo();
        logger.info("");
        
        mammal.showInfo();
        logger.info("");
        
        dog.showInfo();
        logger.info("");
        
        bird.showInfo();
        logger.info("");
    }
    
    /**
     * 演示方法重写
     */
    public void demonstrateMethodOverriding() {
        logger.info("--- 方法重写演示 ---");
        
        Animal animal = new Animal("动物", 2, 5.0, "普通动物");
        Mammal mammal = new Mammal("哺乳动物", 3, 10.0, true, 60, "灰色");
        Dog dog = new Dog("狗狗", 1, 6.0, "拉布拉多", false, "球");
        Bird bird = new Bird("鸟儿", 2, 0.3, true, 25.0, "绿色", false);
        
        logger.info("不同动物的发声方式:");
        animal.makeSound();    // 调用Animal的方法
        mammal.makeSound();    // 调用Mammal重写的方法
        dog.makeSound();       // 调用Dog重写的方法
        bird.makeSound();      // 调用Bird重写的方法
        
        logger.info("\n不同动物的移动方式:");
        animal.move();         // 调用Animal的方法
        mammal.move();         // 调用Mammal重写的方法
        dog.move();            // 调用Dog重写的方法
        bird.move();           // 调用Bird重写的方法
        
        logger.info("");
    }
    
    /**
     * 演示super关键字的使用
     */
    public void demonstrateSuperKeyword() {
        logger.info("--- super关键字演示 ---");
        
        Mammal mammal = new Mammal("测试哺乳动物", 2, 8.5, true, 45, "黑白相间");
        Dog dog = new Dog("测试狗", 1, 5.0, "哈士奇", false, "骨头");
        
        // 演示super调用父类方法
        logger.info("Mammal使用super调用父类方法:");
        mammal.demonstrateSuperUsage();
        
        logger.info("\nDog使用super调用父类方法:");
        dog.demonstratePolymorphism(mammal);
        
        logger.info("");
    }
    
    /**
     * 演示多层继承
     */
    public void demonstrateMultiLevelInheritance() {
        logger.info("--- 多层继承演示 ---");
        
        Dog dog = new Dog("多代继承测试犬", 3, 12.0, "德国牧羊犬", true, "飞盘");
        
        logger.info("访问继承层次中的各种方法:");
        // 来自Animal类的方法
        dog.eat("狗粮");
        dog.sleep();
        
        // 来自Mammal类的方法
        dog.nurse();  // 哺乳动物特有
        dog.regulateBodyTemperature();
        
        // 来自Dog类的方法
        dog.bark();
        dog.fetch("球");
        dog.train();
        
        logger.info("\n继承链: Dog -> Mammal -> Animal");
        logger.info("Dog对象可以访问所有祖先类的方法和属性");
        logger.info("");
    }
    
    /**
     * 演示多态性
     */
    public void demonstratePolymorphism() {
        logger.info("--- 多态性演示 ---");
        
        // 同一引用类型，不同实际对象
        Animal[] animals = {
            new Animal("普通动物", 2, 5.0, "未知"),
            new Mammal("哺乳动物", 3, 10.0, true, 60, "棕色"),
            new Dog("狗狗", 1, 6.0, "边牧", true, "飞盘"),
            new Bird("鸟儿", 2, 0.3, true, 25.0, "彩色", true)
        };
        
        logger.info("多态性 - 同一方法调用产生不同行为:");
        for (Animal animal : animals) {
            logger.info("动物类型: {}", animal.getClass().getSimpleName());
            animal.makeSound();  // 运行时决定调用哪个方法
            animal.move();       // 运行时决定调用哪个方法
            logger.info("");
        }
        
        // 向上转型和向下转型演示
        logger.info("类型转换演示:");
        Animal animalRef = new Dog("转型测试犬", 2, 8.0, "金毛", true, "玩具");
        logger.info("向上转型后引用类型: {}", animalRef.getClass().getSimpleName());
        animalRef.makeSound(); // 调用Dog的重写方法
        
        // 向下转型（需要类型检查）
        if (animalRef instanceof Dog) {
            Dog dogRef = (Dog) animalRef;
            logger.info("向下转型成功");
            dogRef.fetch("飞盘"); // 可以调用Dog特有方法
        }
        
        logger.info("");
    }
    
    /**
     * 演示静态成员继承
     */
    public void demonstrateStaticMembers() {
        logger.info("--- 静态成员演示 ---");
        
        logger.info("初始动物总数: {}", Animal.getAnimalCount());
        
        // 创建多个对象
        Animal animal1 = new Animal("动物1", 1, 2.0, "物种A");
        Mammal mammal1 = new Mammal("哺乳动物1", 2, 5.0, true, 30, "黑色");
        Dog dog1 = new Dog("狗1", 1, 3.0, "泰迪", false, "球");
        Bird bird1 = new Bird("鸟1", 1, 0.1, true, 15.0, "红色", false);
        
        logger.info("创建4个对象后动物总数: {}", Animal.getAnimalCount());
        
        // 静态方法调用
        Bird eagle = new Bird("老鹰", 5, 4.0, true, 200.0, "褐色", true);
        double speed = Bird.calculateFlightSpeed(eagle);
        boolean isLarge = Bird.isLargeBird(eagle);
        
        logger.info("老鹰飞行速度: {} km/h", String.format("%.1f", speed));
        logger.info("老鹰是否为大型鸟类: {}", isLarge ? "是" : "否");
        
        logger.info("");
    }
}