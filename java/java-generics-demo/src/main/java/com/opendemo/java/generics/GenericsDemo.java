package com.opendemo.java.generics;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class GenericsDemo {
    private static final Logger logger = LoggerFactory.getLogger(GenericsDemo.class);

    public static void main(String[] args) {
        GenericsDemo demo = new GenericsDemo();
        demo.runAll();
    }

    public void runAll() {
        demonstrateGenericBox();
        demonstrateGenericMethods();
        demonstrateBoundedTypes();
        demonstrateWildcards();
    }

    public void demonstrateGenericBox() {
        logger.info("=== 泛型类示例 ===");
        GenericBox<String> stringBox = new GenericBox<>("Hello");
        logger.info("String Box: {}", stringBox);
        GenericBox<Integer> intBox = new GenericBox<>(42);
        logger.info("Integer Box: {}", intBox);
        GenericBox<Double> emptyBox = new GenericBox<>();
        logger.info("空Box类型: {}", emptyBox.getType());
    }

    public void demonstrateGenericMethods() {
        logger.info("=== 泛型方法示例 ===");
        Integer[] intArray = {1, 2, 3, 4, 5};
        String[] strArray = {"apple", "banana", "cherry"};

        logger.info("数组中间元素: {}", GenericMethodDemo.getMiddle(intArray));
        logger.info("最大值: {}", GenericMethodDemo.findMax(intArray));
        logger.info("字符串最大值: {}", GenericMethodDemo.findMax(strArray));
        logger.info("数组转列表: {}", GenericMethodDemo.fromArrayToList(intArray));
        logger.info("格式化键值对: {}", GenericMethodDemo.formatPair("name", 42));

        Integer[] swapArray = {1, 2, 3};
        GenericMethodDemo.swap(swapArray, 0, 2);
        logger.info("交换后: {}", Arrays.toString(swapArray));
    }

    public void demonstrateBoundedTypes() {
        logger.info("=== 有界类型参数示例 ===");
        BoundedTypeDemo.NumberBox<Integer> intBox = new BoundedTypeDemo.NumberBox<>(100);
        BoundedTypeDemo.NumberBox<Double> doubleBox = new BoundedTypeDemo.NumberBox<>(3.14);
        logger.info("Integer Box: {} doubleValue={}", intBox, intBox.doubleValue());
        logger.info("Double Box: {} doubleValue={}", doubleBox, doubleBox.doubleValue());

        Integer[] numbers = {1, 5, 3, 8, 2};
        logger.info("大于5的个数: {}", BoundedTypeDemo.countGreaterThan(numbers, 5));

        List<Integer> intList = Arrays.asList(1, 2, 3, 4, 5);
        logger.info("Integer列表求和: {}", BoundedTypeDemo.sumOfList(intList));
    }

    public void demonstrateWildcards() {
        logger.info("=== 通配符示例 ===");
        List<Integer> intList = Arrays.asList(1, 2, 3);
        List<Double> doubleList = Arrays.asList(1.1, 2.2, 3.3);
        List<String> strList = Arrays.asList("a", "b", "c");

        WildcardDemo.printList(intList);
        WildcardDemo.printList(strList);
        WildcardDemo.sumList(intList);
        WildcardDemo.sumList(doubleList);

        List<Number> numberList = new ArrayList<>();
        WildcardDemo.addIntegers(numberList);
        logger.info("添加后的列表: {}", numberList);

        List<Object> dest = new ArrayList<>();
        WildcardDemo.copyList(intList, dest);
        logger.info("复制后的目标列表: {}", dest);
    }
}
