package com.opendemo.java.reflection;

public class ReflectionDemo {
    private String name;
    public int age;
    
    public ReflectionDemo(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public void display() {
        System.out.println("Name: " + name + ", Age: " + age);
    }
}