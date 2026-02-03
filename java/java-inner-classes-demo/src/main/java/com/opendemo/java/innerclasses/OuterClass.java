package com.opendemo.java.innerclasses;

public class OuterClass {
    private String outerField = "外部类字段";
    
    // 成员内部类
    public class InnerClass {
        private String innerField = "内部类字段";
        
        public void accessOuter() {
            System.out.println("访问外部类字段: " + outerField);
        }
    }
    
    // 静态嵌套类
    public static class StaticNestedClass {
        public void display() {
            System.out.println("静态嵌套类方法");
        }
    }
    
    public void createInner() {
        InnerClass inner = new InnerClass();
        inner.accessOuter();
    }
}