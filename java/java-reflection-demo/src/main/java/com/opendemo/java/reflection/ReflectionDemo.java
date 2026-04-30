package com.opendemo.java.reflection;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

public class ReflectionDemo {
    private static final Logger logger = LoggerFactory.getLogger(ReflectionDemo.class);

    public static void main(String[] args) {
        ReflectionDemo demo = new ReflectionDemo();
        demo.runAll();
    }

    public void runAll() {
        demonstrateClassInfo();
        demonstrateFieldAccess();
        demonstrateMethodInvocation();
        demonstrateConstructorAccess();
    }

    public void demonstrateClassInfo() {
        logger.info("=== 类信息获取 ===");
        Class<?> clazz = SampleClass.class;
        List<String> classInfo = ReflectionUtils.getClassInfo(clazz);
        for (String info : classInfo) {
            logger.info(info);
        }

        logger.info("--- 字段列表 ---");
        ReflectionUtils.getFields(clazz);

        logger.info("--- 方法列表 ---");
        ReflectionUtils.getMethods(clazz);

        logger.info("--- 构造器列表 ---");
        ReflectionUtils.getConstructors(clazz);
    }

    public void demonstrateFieldAccess() {
        logger.info("=== 字段访问 ===");
        try {
            SampleClass sample = new SampleClass("张三", 25);
            String name = (String) ReflectionUtils.getFieldValue(sample, "name");
            int age = (int) ReflectionUtils.getFieldValue(sample, "age");
            logger.info("反射获取 name: {}", name);
            logger.info("反射获取 age: {}", age);

            ReflectionUtils.setFieldValue(sample, "name", "李四");
            ReflectionUtils.setFieldValue(sample, "age", 30);
            logger.info("修改后的对象: {}", sample);
        } catch (Exception e) {
            logger.error("字段访问错误", e);
        }
    }

    public void demonstrateMethodInvocation() {
        logger.info("=== 方法调用 ===");
        try {
            SampleClass sample = new SampleClass("王五", 28);
            String result = (String) ReflectionUtils.invokeMethod(
                    sample, "greet", new Class[]{String.class}, new Object[]{"你好"});
            logger.info("调用greet方法: {}", result);

            String privateResult = (String) ReflectionUtils.invokeMethod(
                    sample, "privateMethod", new Class[]{String.class}, new Object[]{"test"});
            logger.info("调用私有方法: {}", privateResult);

            String staticResult = (String) ReflectionUtils.invokeMethod(
                    null, "staticMethod", new Class[]{}, new Object[]{});
            logger.info("调用静态方法: {}", staticResult);
        } catch (Exception e) {
            logger.error("方法调用错误", e);
        }
    }

    public void demonstrateConstructorAccess() {
        logger.info("=== 构造器访问 ===");
        try {
            Object instance1 = ReflectionUtils.createInstance(
                    SampleClass.class, new Class[]{}, new Object[]{});
            logger.info("无参构造: {}", instance1);

            Object instance2 = ReflectionUtils.createInstance(
                    SampleClass.class, new Class[]{String.class, int.class}, new Object[]{"赵六", 35});
            logger.info("有参构造: {}", instance2);

            Object instance3 = ReflectionUtils.createInstance(
                    SampleClass.class, new Class[]{String.class}, new Object[]{"私有构造"});
            logger.info("私有构造: {}", instance3);
        } catch (Exception e) {
            logger.error("构造器访问错误", e);
        }
    }
}
