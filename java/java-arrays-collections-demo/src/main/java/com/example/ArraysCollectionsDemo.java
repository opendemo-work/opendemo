package com.example;

import java.util.*;
import java.util.stream.Collectors;

/**
 * 数组与集合综合应用演示
 * 展示实际开发中的典型使用场景
 * 
 * @author OpenDemo Team
 * @version 1.0.0
 */
public class ArraysCollectionsDemo {
    
    public static void main(String[] args) {
        System.out.println("=== 数组与集合综合应用演示 ===\n");
        
        // 1. 数据处理场景
        demonstrateDataProcessing();
        
        // 2. 算法实现场景
        demonstrateAlgorithmScenarios();
        
        // 3. 业务应用场景
        demonstrateBusinessScenarios();
        
        // 4. 性能对比场景
        demonstratePerformanceComparison();
    }
    
    /**
     * 演示数据处理场景
     */
    private static void demonstrateDataProcessing() {
        System.out.println("1. 数据处理场景:");
        
        // 学生成绩数据处理
        Student[] students = {
            new Student("张三", 85),
            new Student("李四", 92),
            new Student("王五", 78),
            new Student("赵六", 96),
            new Student("钱七", 88)
        };
        
        // 数组转List进行处理
        List<Student> studentList = Arrays.asList(students);
        
        // 找出成绩最高的学生
        Student topStudent = studentList.stream()
            .max(Comparator.comparingInt(Student::getScore))
            .orElse(null);
        System.out.println("最高分学生: " + topStudent);
        
        // 计算平均分
        double averageScore = studentList.stream()
            .mapToInt(Student::getScore)
            .average()
            .orElse(0.0);
        System.out.println("平均分: " + String.format("%.2f", averageScore));
        
        // 筛选出优秀学生（分数>=90）
        List<Student> excellentStudents = studentList.stream()
            .filter(student -> student.getScore() >= 90)
            .collect(Collectors.toList());
        System.out.println("优秀学生: " + excellentStudents);
        
        // 按成绩排序
        List<Student> sortedStudents = studentList.stream()
            .sorted(Comparator.comparingInt(Student::getScore).reversed())
            .collect(Collectors.toList());
        System.out.println("按成绩排序: " + sortedStudents);
        
        System.out.println();
    }
    
    /**
     * 演示算法实现场景
     */
    private static void demonstrateAlgorithmScenarios() {
        System.out.println("2. 算法实现场景:");
        
        // 冒泡排序 - 数组实现
        int[] arr = {64, 34, 25, 12, 22, 11, 90};
        System.out.println("排序前: " + Arrays.toString(arr));
        bubbleSort(arr);
        System.out.println("冒泡排序后: " + Arrays.toString(arr));
        
        // 快速去重 - 集合实现
        List<Integer> numbersWithDuplicates = Arrays.asList(1, 2, 3, 2, 4, 1, 5, 3);
        System.out.println("原列表: " + numbersWithDuplicates);
        
        // 使用Set去重
        Set<Integer> uniqueNumbers = new LinkedHashSet<>(numbersWithDuplicates);
        List<Integer> deduplicatedList = new ArrayList<>(uniqueNumbers);
        System.out.println("去重后: " + deduplicatedList);
        
        // 频率统计
        List<String> words = Arrays.asList("apple", "banana", "apple", "orange", "banana", "apple");
        Map<String, Long> wordCount = words.stream()
            .collect(Collectors.groupingBy(
                word -> word,
                Collectors.counting()
            ));
        System.out.println("词频统计: " + wordCount);
        
        System.out.println();
    }
    
    /**
     * 演示业务应用场景
     */
    private static void demonstrateBusinessScenarios() {
        System.out.println("3. 业务应用场景:");
        
        // 购物车管理
        ShoppingCart cart = new ShoppingCart();
        cart.addItem(new Product("笔记本电脑", 5999.0));
        cart.addItem(new Product("鼠标", 99.0));
        cart.addItem(new Product("键盘", 299.0));
        cart.addItem(new Product("笔记本电脑", 5999.0)); // 重复商品
        
        System.out.println("购物车商品:");
        cart.getItems().forEach(System.out::println);
        System.out.println("商品种类数: " + cart.getItemCount());
        System.out.println("总金额: ¥" + String.format("%.2f", cart.getTotalAmount()));
        
        // 库存管理
        InventoryManager inventory = new InventoryManager();
        inventory.addProduct("iPhone", 50);
        inventory.addProduct("iPad", 30);
        inventory.addProduct("MacBook", 20);
        
        System.out.println("\n库存情况:");
        inventory.displayInventory();
        
        inventory.updateStock("iPhone", -5); // 销售5台
        inventory.updateStock("iPad", 10);   // 进货10台
        
        System.out.println("\n更新后库存:");
        inventory.displayInventory();
        
        System.out.println();
    }
    
    /**
     * 演示性能对比场景
     */
    private static void demonstratePerformanceComparison() {
        System.out.println("4. 性能对比场景:");
        
        int size = 100000;
        List<Integer> dataList = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            dataList.add(i);
        }
        
        // ArrayList vs LinkedList 插入性能对比
        long startTime = System.nanoTime();
        List<Integer> arrayList = new ArrayList<>();
        for (int i = 0; i < 10000; i++) {
            arrayList.add(0, i); // 在开头插入
        }
        long arrayListTime = System.nanoTime() - startTime;
        
        startTime = System.nanoTime();
        List<Integer> linkedList = new LinkedList<>();
        for (int i = 0; i < 10000; i++) {
            linkedList.add(0, i); // 在开头插入
        }
        long linkedListTime = System.nanoTime() - startTime;
        
        System.out.println("ArrayList头部插入耗时: " + arrayListTime / 1000000 + " ms");
        System.out.println("LinkedList头部插入耗时: " + linkedListTime / 1000000 + " ms");
        
        // 查找性能对比
        startTime = System.nanoTime();
        arrayList.contains(5000);
        long arrayListSearchTime = System.nanoTime() - startTime;
        
        startTime = System.nanoTime();
        linkedList.contains(5000);
        long linkedListSearchTime = System.nanoTime() - startTime;
        
        System.out.println("ArrayList查找耗时: " + arrayListSearchTime / 1000 + " μs");
        System.out.println("LinkedList查找耗时: " + linkedListSearchTime / 1000 + " μs");
        
        System.out.println();
    }
    
    // 冒泡排序实现
    private static void bubbleSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    // 交换元素
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }
    
    // 辅助类定义
    static class Student {
        private String name;
        private int score;
        
        public Student(String name, int score) {
            this.name = name;
            this.score = score;
        }
        
        public String getName() { return name; }
        public int getScore() { return score; }
        
        @Override
        public String toString() {
            return name + "(" + score + ")";
        }
    }
    
    static class Product {
        private String name;
        private double price;
        
        public Product(String name, double price) {
            this.name = name;
            this.price = price;
        }
        
        public String getName() { return name; }
        public double getPrice() { return price; }
        
        @Override
        public String toString() {
            return name + " - ¥" + price;
        }
        
        @Override
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (obj == null || getClass() != obj.getClass()) return false;
            Product product = (Product) obj;
            return Objects.equals(name, product.name);
        }
        
        @Override
        public int hashCode() {
            return Objects.hash(name);
        }
    }
    
    static class ShoppingCart {
        private List<Product> items = new ArrayList<>();
        
        public void addItem(Product product) {
            items.add(product);
        }
        
        public List<Product> getItems() {
            return new ArrayList<>(items); // 返回副本
        }
        
        public int getItemCount() {
            return new HashSet<>(items).size(); // 去重计数
        }
        
        public double getTotalAmount() {
            return items.stream()
                .mapToDouble(Product::getPrice)
                .sum();
        }
    }
    
    static class InventoryManager {
        private Map<String, Integer> inventory = new HashMap<>();
        
        public void addProduct(String productName, int quantity) {
            inventory.merge(productName, quantity, Integer::sum);
        }
        
        public void updateStock(String productName, int change) {
            inventory.computeIfPresent(productName, (key, value) -> {
                int newQuantity = value + change;
                return newQuantity >= 0 ? newQuantity : 0;
            });
        }
        
        public void displayInventory() {
            inventory.forEach((product, quantity) -> 
                System.out.println(product + ": " + quantity + " 件"));
        }
    }
}