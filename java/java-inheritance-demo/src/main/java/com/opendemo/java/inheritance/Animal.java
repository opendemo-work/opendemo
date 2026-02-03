package com.opendemo.java.inheritance;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Animal基类 - 演示继承的基本概念
 * 作为所有动物的父类，定义通用的属性和方法
 */
public class Animal {
    protected static final Logger logger = LoggerFactory.getLogger(Animal.class);
    
    // 受保护的成员变量，子类可以访问
    protected String name;
    protected int age;
    protected double weight;
    protected String species;
    
    // 私有静态变量，记录动物总数
    private static int animalCount = 0;
    
    // 构造方法
    public Animal() {
        this.name = "未知动物";
        this.age = 0;
        this.weight = 0.0;
        this.species = "未知物种";
        animalCount++;
        logger.info("创建了动物对象: {}", this.name);
    }
    
    public Animal(String name, int age, double weight, String species) {
        this.name = name;
        this.age = age;
        this.weight = weight;
        this.species = species;
        animalCount++;
        logger.info("创建了{}: {}, 年龄: {}, 体重: {}kg", species, name, age, weight);
    }
    
    // Getter和Setter方法
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public int getAge() {
        return age;
    }
    
    public void setAge(int age) {
        if (age >= 0) {
            this.age = age;
        } else {
            logger.warn("年龄不能为负数: {}", age);
        }
    }
    
    public double getWeight() {
        return weight;
    }
    
    public void setWeight(double weight) {
        if (weight > 0) {
            this.weight = weight;
        } else {
            logger.warn("体重必须大于0: {}", weight);
        }
    }
    
    public String getSpecies() {
        return species;
    }
    
    // 静态方法
    public static int getAnimalCount() {
        return animalCount;
    }
    
    // 通用行为方法
    public void eat(String food) {
        logger.info("{}正在吃{}", name, food);
    }
    
    public void sleep() {
        logger.info("{}正在睡觉", name);
    }
    
    public void move() {
        logger.info("{}正在移动", name);
    }
    
    public void makeSound() {
        logger.info("{}发出声音", name);
    }
    
    public void showInfo() {
        logger.info("=== 动物信息 ===");
        logger.info("姓名: {}", name);
        logger.info("年龄: {}岁", age);
        logger.info("体重: {}kg", weight);
        logger.info("物种: {}", species);
    }
    
    // 重写toString方法
    @Override
    public String toString() {
        return String.format("%s[name='%s', age=%d, weight=%.1fkg, species='%s']", 
                           getClass().getSimpleName(), name, age, weight, species);
    }
    
    // 重写equals方法
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Animal animal = (Animal) obj;
        return age == animal.age && 
               Double.compare(animal.weight, weight) == 0 &&
               name.equals(animal.name) && 
               species.equals(animal.species);
    }
    
    // 重写hashCode方法
    @Override
    public int hashCode() {
        return name.hashCode() + age + (int)(weight * 100) + species.hashCode();
    }
}