package com.opendemo.java.generics;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Arrays;
import java.util.List;

public class WildcardDemo {
    private static final Logger logger = LoggerFactory.getLogger(WildcardDemo.class);

    public static void printList(List<?> list) {
        logger.info("列表内容: {}", list);
    }

    public static double sumList(List<? extends Number> list) {
        double sum = 0.0;
        for (Number num : list) {
            sum += num.doubleValue();
        }
        logger.info("数值列表求和: {}", sum);
        return sum;
    }

    public static void addIntegers(List<? super Integer> list) {
        list.add(1);
        list.add(2);
        list.add(3);
        logger.info("向列表添加了3个整数");
    }

    public static boolean containsNull(List<?> list) {
        return list.contains(null);
    }

    public static <T> void copyList(List<? extends T> source, List<? super T> dest) {
        dest.addAll(source);
        logger.info("复制了 {} 个元素", source.size());
    }

    public static void printArray(Object[] array) {
        logger.info("数组内容: {}", Arrays.toString(array));
    }
}
