package com.opendemo.java.oop;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Java面向对象编程演示程序
 * 展示类的定义、对象的创建和使用，以及面向对象的核心概念
 */
public class ClassesObjectsDemo {
    private static final Logger logger = LoggerFactory.getLogger(ClassesObjectsDemo.class);
    
    public static void main(String[] args) {
        logger.info("=== Java面向对象编程演示 ===");
        
        ClassesObjectsDemo demo = new ClassesObjectsDemo();
        
        demo.demonstrateBasicObjectCreation();
        demo.demonstrateConstructors();
        demo.demonstrateEncapsulation();
        demo.demonstrateObjectRelationships();
        demo.demonstrateStaticMembers();
        demo.demonstrateMethodOverriding();
        
        logger.info("=== 演示完成 ===");
    }
    
    /**
     * 演示基本对象创建
     */
    public void demonstrateBasicObjectCreation() {
        logger.info("--- 基本对象创建演示 ---");
        
        // 使用无参构造方法创建对象
        Person person1 = new Person();
        person1.setName("张三");
        person1.setAge(25);
        person1.introduce();
        
        // 使用有参构造方法创建对象
        Person person2 = new Person("李四", 30);
        person2.introduce();
        
        // 使用完整构造方法创建对象
        Person person3 = new Person("王五", 28, "wangwu@company.com");
        person3.introduce();
        
        logger.info("");
    }
    
    /**
     * 演示构造方法的使用
     */
    public void demonstrateConstructors() {
        logger.info("--- 构造方法演示 ---");
        
        // 不同构造方法的效果
        logger.info("使用不同构造方法创建对象:");
        Person p1 = new Person();                           // 无参构造
        Person p2 = new Person("赵六", 22);                 // 两参构造
        Person p3 = new Person("钱七", 35, "qianqi@mail.com"); // 三参构造
        
        logger.info("p1: {}", p1);
        logger.info("p2: {}", p2);
        logger.info("p3: {}", p3);
        
        logger.info("");
    }
    
    /**
     * 演示封装性的实现
     */
    public void demonstrateEncapsulation() {
        logger.info("--- 封装性演示 ---");
        
        Person person = new Person("测试用户", 20);
        
        // 正常的数据访问
        logger.info("原始姓名: {}", person.getName());
        logger.info("原始年龄: {}", person.getAge());
        
        // 尝试设置有效数据
        person.setName("新名字");
        person.setAge(25);
        logger.info("更新后姓名: {}", person.getName());
        logger.info("更新后年龄: {}", person.getAge());
        
        // 尝试设置无效数据
        person.setAge(-5);    // 无效年龄
        person.setName("");   // 无效姓名
        person.setEmail("invalid-email"); // 无效邮箱
        
        logger.info("最终年龄: {}", person.getAge()); // 应该还是25
        logger.info("");
    }
    
    /**
     * 演示对象之间的关系
     */
    public void demonstrateObjectRelationships() {
        logger.info("--- 对象关系演示 ---");
        
        // 创建人物对象
        Person owner = new Person("车主", 32, "owner@auto.com");
        
        // 创建汽车对象
        Car car = new Car("丰田", "凯美瑞", 2023, "银色", 250000);
        
        // 建立关系
        car.setOwner(owner);
        
        // 展示信息
        car.showInfo();
        logger.info("所有者信息: {}", owner);
        
        // 模拟汽车操作
        logger.info("\n汽车操作演示:");
        car.start();
        car.accelerate(60);
        car.brake(20);
        car.stop();
        
        logger.info("");
    }
    
    /**
     * 演示静态成员的使用
     */
    public void demonstrateStaticMembers() {
        logger.info("--- 静态成员演示 ---");
        
        logger.info("初始Person数量: {}", Person.getPersonCount());
        
        // 创建多个对象
        Person p1 = new Person("用户1", 20);
        Person p2 = new Person("用户2", 25);
        Person p3 = new Person("用户3", 30);
        
        logger.info("创建3个对象后Person数量: {}", Person.getPersonCount());
        
        // 静态方法调用
        Car car = new Car("本田", "雅阁", 2022);
        logger.info("汽车信息: {}", Car.getCarInfo(car));
        logger.info("无效调用: {}", Car.getCarInfo(null));
        logger.info("是否新车: {}", Car.isNewCar(car));
        
        logger.info("");
    }
    
    /**
     * 演示方法重写的使用
     */
    public void demonstrateMethodOverriding() {
        logger.info("--- 方法重写演示 ---");
        
        Person person = new Person("重写测试", 25);
        Car car = new Car("奔驰", "C级", 2024);
        
        // toString()方法重写
        logger.info("Person.toString(): {}", person);
        logger.info("Car.toString(): {}", car);
        
        // equals()方法重写测试
        Person person1 = new Person("测试", 25, "test@email.com");
        Person person2 = new Person("测试", 25, "test@email.com");
        Person person3 = new Person("不同", 30, "different@email.com");
        
        logger.info("person1.equals(person2): {}", person1.equals(person2)); // 应该为true
        logger.info("person1.equals(person3): {}", person1.equals(person3)); // 应该为false
        
        // hashCode()方法
        logger.info("person1.hashCode(): {}", person1.hashCode());
        logger.info("person2.hashCode(): {}", person2.hashCode());
        logger.info("person3.hashCode(): {}", person3.hashCode());
        
        logger.info("");
    }
}