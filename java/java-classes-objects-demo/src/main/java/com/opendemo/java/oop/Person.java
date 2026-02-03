package com.opendemo.java.oop;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Person类 - 演示基本的类定义和封装
 * 展示面向对象编程的核心概念：封装、构造方法、访问控制
 */
public class Person {
    private static final Logger logger = LoggerFactory.getLogger(Person.class);
    
    // 成员变量（属性）- 使用private修饰符实现封装
    private String name;
    private int age;
    private String email;
    private static int personCount = 0; // 静态变量，记录实例数量
    
    // 无参构造方法
    public Person() {
        this.name = "未知";
        this.age = 0;
        this.email = "unknown@example.com";
        personCount++;
        logger.info("创建了一个Person对象");
    }
    
    // 有参构造方法
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
        this.email = name.toLowerCase().replace(" ", ".") + "@example.com";
        personCount++;
        logger.info("创建了Person对象: {}", name);
    }
    
    // 完整构造方法
    public Person(String name, int age, String email) {
        this.name = name;
        this.age = age;
        this.email = email;
        personCount++;
        logger.info("创建了完整Person对象: {}", name);
    }
    
    // Getter和Setter方法 - 提供受控访问
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        if (name != null && !name.trim().isEmpty()) {
            this.name = name;
        } else {
            logger.warn("姓名不能为空");
        }
    }
    
    public int getAge() {
        return age;
    }
    
    public void setAge(int age) {
        if (age >= 0 && age <= 150) {
            this.age = age;
        } else {
            logger.warn("年龄必须在0-150之间，当前值: {}", age);
        }
    }
    
    public String getEmail() {
        return email;
    }
    
    public void setEmail(String email) {
        if (email != null && email.contains("@")) {
            this.email = email;
        } else {
            logger.warn("邮箱格式不正确: {}", email);
        }
    }
    
    // 业务方法
    public void introduce() {
        logger.info("大家好，我是{}，今年{}岁", name, age);
    }
    
    public void celebrateBirthday() {
        age++;
        logger.info("{}过生日了！现在{}岁了！", name, age);
    }
    
    public boolean isAdult() {
        return age >= 18;
    }
    
    // 静态方法
    public static int getPersonCount() {
        return personCount;
    }
    
    // 重写toString方法
    @Override
    public String toString() {
        return String.format("Person{name='%s', age=%d, email='%s'}", name, age, email);
    }
    
    // 重写equals方法
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Person person = (Person) obj;
        return age == person.age && 
               name.equals(person.name) && 
               email.equals(person.email);
    }
    
    // 重写hashCode方法
    @Override
    public int hashCode() {
        return name.hashCode() + age + email.hashCode();
    }
}