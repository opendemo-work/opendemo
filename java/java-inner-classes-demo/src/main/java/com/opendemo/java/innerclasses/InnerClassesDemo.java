package com.opendemo.java.innerclasses;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class InnerClassesDemo {
    private static final Logger logger = LoggerFactory.getLogger(InnerClassesDemo.class);

    public static void main(String[] args) {
        InnerClassesDemo demo = new InnerClassesDemo();
        demo.runAll();
    }

    public void runAll() {
        demonstrateMemberInnerClass();
        demonstrateStaticNestedClass();
        demonstrateLocalClass();
        demonstrateAnonymousClass();
    }

    public String demonstrateMemberInnerClass() {
        logger.info("=== 成员内部类示例 ===");
        OuterClass outer = new OuterClass();
        OuterClass.InnerClass inner = outer.createInner();
        inner.accessOuter();
        String result = inner.getOuterField() + " + " + inner.getInnerField();
        logger.info("组合结果: {}", result);
        return result;
    }

    public String demonstrateStaticNestedClass() {
        logger.info("=== 静态嵌套类示例 ===");
        OuterClass.StaticNestedClass nested = new OuterClass.StaticNestedClass();
        nested.display();
        OuterClass.StaticNestedClass.staticMethod();
        String result = nested.getNestedField();
        logger.info("静态嵌套类字段: {}", result);
        return result;
    }

    public String demonstrateLocalClass() {
        logger.info("=== 局部内部类示例 ===");
        OuterClass outer = new OuterClass();
        String result = outer.demonstrateLocalClass("前缀");
        logger.info("局部内部类结果: {}", result);
        return result;
    }

    public String demonstrateAnonymousClass() {
        logger.info("=== 匿名内部类示例 ===");
        OuterClass outer = new OuterClass();
        Runnable runnable = outer.createAnonymousRunnable("测试消息");
        runnable.run();
        return "匿名内部类执行完成";
    }

    public String demonstrateAnonymousInterface() {
        java.util.function.Function<String, String> transformer = new java.util.function.Function<String, String>() {
            @Override
            public String apply(String s) {
                return s.toUpperCase();
            }
        };
        return transformer.apply("hello");
    }
}
