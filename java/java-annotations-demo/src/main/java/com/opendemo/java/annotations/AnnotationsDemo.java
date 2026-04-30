package com.opendemo.java.annotations;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.lang.reflect.Method;
import java.util.List;

public class AnnotationsDemo {
    private static final Logger logger = LoggerFactory.getLogger(AnnotationsDemo.class);

    public static void main(String[] args) {
        AnnotationsDemo demo = new AnnotationsDemo();
        demo.runAll();
    }

    public void runAll() {
        demonstrateBuiltInAnnotations();
        demonstrateCustomAnnotations();
        demonstrateAnnotationProcessing();
    }

    public void demonstrateBuiltInAnnotations() {
        logger.info("=== 内置注解示例 ===");
        CustomAnnotations example = new CustomAnnotations();
        logger.info("toString: {}", example.toString());
        logger.info("legacyMethod: {}", example.legacyMethod());
        logger.info("annotatedMethod: {}", example.annotatedMethod("hello"));
    }

    public void demonstrateCustomAnnotations() {
        logger.info("=== 自定义注解示例 ===");
        AnnotationProcessor processor = new AnnotationProcessor();
        Class<?> clazz = CustomAnnotations.class;

        logger.info("作者信息: {}", processor.getAuthorInfo(clazz));
        logger.info("版本信息: {}", processor.getVersionInfo(clazz));
    }

    public void demonstrateAnnotationProcessing() {
        logger.info("=== 注解处理示例 ===");
        AnnotationProcessor processor = new AnnotationProcessor();
        Class<?> clazz = CustomAnnotations.class;

        List<String> classAnnotations = processor.processClassAnnotations(clazz);
        logger.info("类级别注解数: {}", classAnnotations.size());

        List<String> methodAnnotations = processor.processMethodAnnotations(clazz);
        logger.info("方法级别注解数: {}", methodAnnotations.size());

        List<String> todos = processor.getTodos(clazz);
        logger.info("待办事项:");
        for (String todo : todos) {
            logger.info("  - {}", todo);
        }

        logger.info("是否有@Author注解: {}", processor.hasAnnotation(clazz, Author.class));
        logger.info("legacyMethod是否有@Deprecated注解: {}",
                processor.methodHasAnnotation(clazz, "legacyMethod", Deprecated.class));
    }
}
