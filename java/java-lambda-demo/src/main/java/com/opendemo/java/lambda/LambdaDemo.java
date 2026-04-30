package com.opendemo.java.lambda;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Arrays;
import java.util.List;
import java.util.function.Function;

public class LambdaDemo {
    private static final Logger logger = LoggerFactory.getLogger(LambdaDemo.class);

    public static void main(String[] args) {
        LambdaDemo demo = new LambdaDemo();
        demo.runAll();
    }

    public void runAll() {
        demonstrateBasicLambda();
        demonstrateMethodReference();
        demonstrateFunctionalInterfaces();
        demonstrateStreamApi();
    }

    public String demonstrateBasicLambda() {
        logger.info("=== 基础Lambda表达式 ===");

        Function<String, Integer> stringLength = str -> str.length();
        logger.info("字符串长度: {}", stringLength.apply("Hello"));

        Function<String, String> toUpper = str -> str.toUpperCase();
        logger.info("大写: {}", toUpper.apply("hello"));

        Function<Integer, Integer> square = x -> x * x;
        logger.info("平方: {}", square.apply(5));

        return toUpper.apply("hello");
    }

    public String demonstrateMethodReference() {
        logger.info("=== 方法引用 ===");

        Function<String, String> upperRef = String::toUpperCase;
        logger.info("实例方法引用: {}", upperRef.apply("hello"));

        Function<String, Integer> parseRef = Integer::parseInt;
        logger.info("静态方法引用: {}", parseRef.apply("42"));

        List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
        logger.info("构造方法引用:");
        names.stream().map(String::new).forEach(name -> logger.info("  {}", name));

        return upperRef.apply("world");
    }

    public void demonstrateFunctionalInterfaces() {
        logger.info("=== 函数式接口 ===");
        FunctionalInterfaceDemo fiDemo = new FunctionalInterfaceDemo();
        fiDemo.demonstrateCustomFunctionalInterface();
        fiDemo.demonstratePredicate();
        fiDemo.demonstrateConsumer();
        fiDemo.demonstrateFunction();
        fiDemo.demonstrateSupplier();
        fiDemo.demonstrateBiFunction();
        fiDemo.demonstrateUnaryOperator();
    }

    public void demonstrateStreamApi() {
        logger.info("=== Stream API ===");
        StreamApiDemo streamDemo = new StreamApiDemo();
        streamDemo.demonstrateFilter();
        streamDemo.demonstrateMap();
        streamDemo.demonstrateReduce();
        streamDemo.demonstrateSorted();
        streamDemo.demonstrateCount();
        streamDemo.demonstrateMatch();
        streamDemo.demonstrateFlatMap();
        streamDemo.demonstrateDistinct();
    }
}
