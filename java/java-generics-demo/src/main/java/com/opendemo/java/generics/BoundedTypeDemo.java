package com.opendemo.java.generics;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class BoundedTypeDemo {
    private static final Logger logger = LoggerFactory.getLogger(BoundedTypeDemo.class);

    public static class NumberBox<T extends Number> {
        private T value;

        public NumberBox(T value) {
            this.value = value;
        }

        public T getValue() {
            return value;
        }

        public double doubleValue() {
            return value.doubleValue();
        }

        public int intValue() {
            return value.intValue();
        }

        public boolean isGreaterThan(NumberBox<T> other) {
            return this.doubleValue() > other.doubleValue();
        }

        @Override
        public String toString() {
            return "NumberBox{" + value + "}";
        }
    }

    public static <T extends Comparable<T>> int countGreaterThan(T[] array, T element) {
        int count = 0;
        for (T item : array) {
            if (item.compareTo(element) > 0) {
                count++;
            }
        }
        logger.info("大于 {} 的元素个数: {}", element, count);
        return count;
    }

    public static double sumOfList(java.util.List<? extends Number> list) {
        double sum = 0.0;
        for (Number n : list) {
            sum += n.doubleValue();
        }
        logger.info("列表求和: {}", sum);
        return sum;
    }

    public static void addNumbers(java.util.List<? super Integer> list, int... numbers) {
        for (int num : numbers) {
            list.add(num);
        }
        logger.info("添加 {} 个数字到列表", numbers.length);
    }
}
