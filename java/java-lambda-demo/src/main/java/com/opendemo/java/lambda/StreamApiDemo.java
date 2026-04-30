package com.opendemo.java.lambda;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

public class StreamApiDemo {
    private static final Logger logger = LoggerFactory.getLogger(StreamApiDemo.class);

    public List<String> demonstrateFilter() {
        logger.info("=== Stream filter示例 ===");
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David", "Eve");
        List<String> filtered = names.stream()
                .filter(name -> name.length() > 3)
                .collect(Collectors.toList());
        logger.info("过滤后(长度>3): {}", filtered);
        return filtered;
    }

    public List<String> demonstrateMap() {
        logger.info("=== Stream map示例 ===");
        List<String> names = Arrays.asList("alice", "bob", "charlie");
        List<String> upperNames = names.stream()
                .map(String::toUpperCase)
                .collect(Collectors.toList());
        logger.info("映射后(大写): {}", upperNames);
        return upperNames;
    }

    public String demonstrateReduce() {
        logger.info("=== Stream reduce示例 ===");
        List<String> names = Arrays.asList("Hello", " ", "World", "!");
        String result = names.stream()
                .reduce("", (a, b) -> a + b);
        logger.info("合并结果: {}", result);
        return result;
    }

    public List<String> demonstrateSorted() {
        logger.info("=== Stream sorted示例 ===");
        List<String> names = Arrays.asList("Charlie", "Alice", "Bob", "David");
        List<String> sorted = names.stream()
                .sorted()
                .collect(Collectors.toList());
        logger.info("排序后: {}", sorted);

        List<String> sortedByLength = names.stream()
                .sorted(Comparator.comparingInt(String::length))
                .collect(Collectors.toList());
        logger.info("按长度排序: {}", sortedByLength);

        return sorted;
    }

    public long demonstrateCount() {
        logger.info("=== Stream count示例 ===");
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        long count = numbers.stream()
                .filter(n -> n % 2 == 0)
                .count();
        logger.info("偶数个数: {}", count);
        return count;
    }

    public boolean demonstrateMatch() {
        logger.info("=== Stream match示例 ===");
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
        boolean allPositive = numbers.stream().allMatch(n -> n > 0);
        boolean anyEven = numbers.stream().anyMatch(n -> n % 2 == 0);
        boolean noneNegative = numbers.stream().noneMatch(n -> n < 0);
        logger.info("全部正数: {}", allPositive);
        logger.info("存在偶数: {}", anyEven);
        logger.info("没有负数: {}", noneNegative);
        return allPositive && anyEven && noneNegative;
    }

    public List<Integer> demonstrateFlatMap() {
        logger.info("=== Stream flatMap示例 ===");
        List<List<Integer>> nested = Arrays.asList(
                Arrays.asList(1, 2, 3),
                Arrays.asList(4, 5, 6),
                Arrays.asList(7, 8, 9));
        List<Integer> flattened = nested.stream()
                .flatMap(List::stream)
                .collect(Collectors.toList());
        logger.info("展平后: {}", flattened);
        return flattened;
    }

    public Integer demonstrateFindFirst() {
        logger.info("=== Stream findFirst示例 ===");
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
        Integer first = numbers.stream()
                .filter(n -> n > 3)
                .findFirst()
                .orElse(null);
        logger.info("第一个大于3的: {}", first);
        return first;
    }

    public List<Integer> demonstrateDistinct() {
        logger.info("=== Stream distinct示例 ===");
        List<Integer> numbers = Arrays.asList(1, 2, 2, 3, 3, 3, 4);
        List<Integer> distinct = numbers.stream()
                .distinct()
                .collect(Collectors.toList());
        logger.info("去重后: {}", distinct);
        return distinct;
    }

    public Integer demonstrateSum() {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
        int sum = numbers.stream()
                .mapToInt(Integer::intValue)
                .sum();
        logger.info("求和: {}", sum);
        return sum;
    }
}
