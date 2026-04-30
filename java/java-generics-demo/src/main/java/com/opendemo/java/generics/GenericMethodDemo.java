package com.opendemo.java.generics;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;

public class GenericMethodDemo {
    private static final Logger logger = LoggerFactory.getLogger(GenericMethodDemo.class);

    public static <T> T getMiddle(T[] array) {
        if (array == null || array.length == 0) {
            return null;
        }
        return array[array.length / 2];
    }

    public static <T extends Comparable<T>> T findMax(T[] array) {
        if (array == null || array.length == 0) {
            return null;
        }
        T max = array[0];
        for (T item : array) {
            if (item.compareTo(max) > 0) {
                max = item;
            }
        }
        return max;
    }

    public static <T extends Comparable<T>> T findMin(T[] array) {
        if (array == null || array.length == 0) {
            return null;
        }
        T min = array[0];
        for (T item : array) {
            if (item.compareTo(min) < 0) {
                min = item;
            }
        }
        return min;
    }

    public static <T> List<T> fromArrayToList(T[] array) {
        List<T> list = new ArrayList<>();
        for (T item : array) {
            list.add(item);
        }
        logger.info("数组转列表: {} -> 大小 {}", array.getClass().getComponentType().getSimpleName(), list.size());
        return list;
    }

    public static <T, U> String formatPair(T first, U second) {
        String result = "(" + first + ", " + second + ")";
        logger.info("格式化键值对: {}", result);
        return result;
    }

    public static <T> void swap(T[] array, int i, int j) {
        if (array == null || i < 0 || j < 0 || i >= array.length || j >= array.length) {
            throw new IllegalArgumentException("无效的索引参数");
        }
        T temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}
