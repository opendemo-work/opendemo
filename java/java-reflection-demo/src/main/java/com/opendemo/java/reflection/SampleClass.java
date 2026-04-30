package com.opendemo.java.reflection;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SampleClass {
    private static final Logger logger = LoggerFactory.getLogger(SampleClass.class);

    private String name;
    public int age;
    protected String email;
    private boolean active;

    public SampleClass() {
        this.name = "default";
        this.age = 0;
        this.active = true;
    }

    public SampleClass(String name, int age) {
        this.name = name;
        this.age = age;
        this.active = true;
    }

    private SampleClass(String name) {
        this.name = name;
        this.age = 0;
    }

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
        this.age = age;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public boolean isActive() {
        return active;
    }

    public void setActive(boolean active) {
        this.active = active;
    }

    public String greet(String greeting) {
        return greeting + ", I am " + name;
    }

    private String privateMethod(String input) {
        logger.info("私有方法被调用: {}", input);
        return "processed: " + input;
    }

    public static String staticMethod() {
        return "static result";
    }

    @Override
    public String toString() {
        return "SampleClass{name='" + name + "', age=" + age + ", email='" + email + "', active=" + active + "}";
    }
}
