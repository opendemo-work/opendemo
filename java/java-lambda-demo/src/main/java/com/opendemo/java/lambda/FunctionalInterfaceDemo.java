package com.opendemo.java.lambda;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.function.*;

public class FunctionalInterfaceDemo {
    private static final Logger logger = LoggerFactory.getLogger(FunctionalInterfaceDemo.class);

    public String demonstrateCustomFunctionalInterface() {
        logger.info("=== 自定义函数式接口 ===");
        StringProcessor toUpper = s -> s.toUpperCase();
        StringProcessor toLower = s -> s.toLowerCase();
        StringProcessor reverse = s -> new StringBuilder(s).reverse().toString();

        String input = "Hello World";
        logger.info("原文: {}", input);
        logger.info("大写: {}", toUpper.process(input));
        logger.info("小写: {}", toLower.process(input));
        logger.info("反转: {}", reverse.process(input));
        logger.info("默认方法: {}", toUpper.processWithDefault(null));

        return toUpper.process(input);
    }

    public boolean demonstratePredicate() {
        logger.info("=== Predicate示例 ===");
        Predicate<String> isEmpty = s -> s == null || s.isEmpty();
        Predicate<String> isLong = s -> s.length() > 5;
        Predicate<String> complexPredicate = isEmpty.negate().and(isLong);

        String test = "Hello World";
        logger.info("'{}' 是否非空且长度>5: {}", test, complexPredicate.test(test));
        logger.info("'hi' 是否非空且长度>5: {}", complexPredicate.test("hi"));

        return complexPredicate.test(test);
    }

    public void demonstrateConsumer() {
        logger.info("=== Consumer示例 ===");
        Consumer<String> print = s -> logger.info("消费: {}", s);
        Consumer<String> printLength = s -> logger.info("长度: {}", s.length());
        Consumer<String> combined = print.andThen(printLength);

        combined.accept("Hello");
    }

    public int demonstrateFunction() {
        logger.info("=== Function示例 ===");
        Function<String, Integer> stringLength = String::length;
        Function<Integer, String> intToString = Object::toString;
        Function<String, String> chain = stringLength.andThen(intToString);

        String input = "Hello World";
        logger.info("字符串长度: {}", stringLength.apply(input));
        logger.info("链式调用: {}", chain.apply(input));

        return stringLength.apply(input);
    }

    public String demonstrateSupplier() {
        logger.info("=== Supplier示例 ===");
        Supplier<String> greeting = () -> "Hello from Supplier";
        Supplier<Double> randomNum = Math::random;

        logger.info("Supplier结果: {}", greeting.get());
        logger.info("随机数: {}", randomNum.get());

        return greeting.get();
    }

    public int demonstrateBiFunction() {
        logger.info("=== BiFunction示例 ===");
        BiFunction<String, String, Integer> combinedLength = (s1, s2) -> s1.length() + s2.length();
        int result = combinedLength.apply("Hello", "World");
        logger.info("合并长度: {}", result);
        return result;
    }

    public void demonstrateUnaryOperator() {
        logger.info("=== UnaryOperator示例 ===");
        UnaryOperator<String> toUpper = String::toUpperCase;
        logger.info("UnaryOperator结果: {}", toUpper.apply("hello"));
    }
}
