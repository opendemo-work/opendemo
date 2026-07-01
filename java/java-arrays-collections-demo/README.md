<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Java数组与集合操作演示

## 🎯 学习目标

通过本案例你将掌握：
- 数组的声明、初始化和基本操作
- 多维数组的使用方法
- 集合框架的核心接口和实现类
- List、Set、Map等常用集合的特性和使用场景
- 集合的遍历、排序和转换操作
- 泛型在集合中的应用

## 🛠️ 环境准备

### 系统要求
- JDK 11或更高版本
- 支持Java的IDE或文本编辑器
- Java基础语法知识

### 依赖检查
```bash
# 验证Java环境
java -version
javac -version
```

## 📁 项目结构

```
java-arrays-collections-demo/
├── src/
│   └── main/
│       └── java/
│           └── com/
│               └── example/
│                   ├── ArraysDemo.java
│                   ├── CollectionsDemo.java
│                   └── ArraysCollectionsDemo.java
├── README.md
└── metadata.json
```

## 🚀 快速开始

### 步骤1：创建项目结构
```bash
mkdir java-arrays-collections-demo
cd java-arrays-collections-demo
mkdir -p src/main/java/com/example
```

### 步骤2：创建数组演示类
创建 `src/main/java/com/example/ArraysDemo.java` 文件：

```java
package com.example;

import java.util.Arrays;

/**
 * Java数组操作演示类
 * 展示数组的声明、初始化、遍历和常用操作
 */
public class ArraysDemo {
    
    public static void main(String[] args) {
        System.out.println("=== Java数组操作演示 ===\n");
        
        // 1. 一维数组基础操作
        demonstrateOneDimensionalArrays();
        
        // 2. 多维数组操作
        demonstrateMultiDimensionalArrays();
        
        // 3. 数组工具类使用
        demonstrateArrayUtils();
        
        // 4. 数组与集合转换
        demonstrateArrayCollectionConversion();
    }
    
    /**
     * 演示一维数组的基础操作
     */
    private static void demonstrateOneDimensionalArrays() {
        System.out.println("1. 一维数组基础操作:");
        
        // 数组声明和初始化方式
        // 方式1：声明后分别初始化
        int[] numbers1 = new int[5];
        numbers1[0] = 10;
        numbers1[1] = 20;
        numbers1[2] = 30;
        numbers1[3] = 40;
        numbers1[4] = 50;
        
        // 方式2：声明时直接初始化
        int[] numbers2 = {1, 2, 3, 4, 5};
        
        // 方式3：使用new关键字初始化
        int[] numbers3 = new int[]{100, 200, 300, 400, 500};
        
        // 数组遍历 - 传统for循环
        System.out.println("传统for循环遍历:");
        for (int i = 0; i < numbers2.length; i++) {
            System.out.print(numbers2[i] + " ");
        }
        System.out.println();
        
        // 数组遍历 - 增强for循环
        System.out.println("增强for循环遍历:");
        for (int num : numbers2) {
            System.out.print(num + " ");
        }
        System.out.println();
        
        // 数组复制
        int[] copiedArray = Arrays.copyOf(numbers2, numbers2.length);
        System.out.println("复制后的数组: " + Arrays.toString(copiedArray));
        
        // 数组扩容
        int[] expandedArray = Arrays.copyOf(numbers2, 8);
        System.out.println("扩容后的数组: " + Arrays.toString(expandedArray));
        
        // 数组填充
        int[] filledArray = new int[5];
        Arrays.fill(filledArray, 99);
        System.out.println("填充后的数组: " + Arrays.toString(filledArray));
        
        System.out.println();
    }
    
    /**
     * 演示多维数组操作
     */
    private static void demonstrateMultiDimensionalArrays() {
        System.out.println("2. 多维数组操作:");
        
        // 二维数组声明和初始化
        // 不规则二维数组
        int[][] matrix1 = new int[3][];
        matrix1[0] = new int[]{1, 2, 3};
        matrix1[1] = new int[]{4, 5};
        matrix1[2] = new int[]{6, 7, 8, 9};
        
        System.out.println("不规则二维数组:");
        for (int i = 0; i < matrix1.length; i++) {
            for (int j = 0; j < matrix1[i].length; j++) {
                System.out.print(matrix1[i][j] + " ");
            }
            System.out.println();
        }
        
        // 规则二维数组
        int[][] matrix2 = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };
        
        System.out.println("\n规则二维数组:");
        for (int[] row : matrix2) {
            for (int element : row) {
                System.out.print(element + " ");
            }
            System.out.println();
        }
        
        // 三维数组示例
        int[][][] cube = new int[2][3][4];
        // 初始化三维数组
        for (int i = 0; i < cube.length; i++) {
            for (int j = 0; j < cube[i].length; j++) {
                for (int k = 0; k < cube[i][j].length; k++) {
                    cube[i][j][k] = i * 100 + j * 10 + k;
                }
            }
        }
        
        System.out.println("\n三维数组示例:");
        for (int i = 0; i < cube.length; i++) {
            System.out.println("层 " + i + ":");
            for (int j = 0; j < cube[i].length; j++) {
                for (int k = 0; k < cube[i][j].length; k++) {
                    System.out.print(cube[i][j][k] + " ");
                }
                System.out.println();
            }
            System.out.println();
        }
        
        System.out.println();
    }
    
    /**
     * 演示数组工具类的使用
     */
    private static void demonstrateArrayUtils() {
        System.out.println("3. 数组工具类使用:");
        
        int[] numbers = {5, 2, 8, 1, 9, 3};
        
        // 数组排序
        System.out.println("原数组: " + Arrays.toString(numbers));
        Arrays.sort(numbers);
        System.out.println("排序后: " + Arrays.toString(numbers));
        
        // 数组搜索
        int index = Arrays.binarySearch(numbers, 8);
        System.out.println("数字8的索引: " + index);
        
        // 数组比较
        int[] array1 = {1, 2, 3};
        int[] array2 = {1, 2, 3};
        int[] array3 = {1, 2, 4};
        
        System.out.println("array1.equals(array2): " + array1.equals(array2)); // false
        System.out.println("Arrays.equals(array1, array2): " + Arrays.equals(array1, array2)); // true
        System.out.println("Arrays.equals(array1, array3): " + Arrays.equals(array1, array3)); // false
        
        // 数组转列表
        String[] fruits = {"苹果", "香蕉", "橙子"};
        System.out.println("数组转字符串: " + Arrays.toString(fruits));
        System.out.println("数组转列表: " + Arrays.asList(fruits));
        
        System.out.println();
    }
    
    /**
     * 演示数组与集合的转换
     */
    private static void demonstrateArrayCollectionConversion() {
        System.out.println("4. 数组与集合转换:");
        
        // 数组转List
        String[] colors = {"红色", "绿色", "蓝色"};
        java.util.List<String> colorList = Arrays.asList(colors);
        System.out.println("数组转List: " + colorList);
        
        // 注意：Arrays.asList()返回的List是固定大小的
        try {
            colorList.add("黄色"); // 这会抛出UnsupportedOperationException
        } catch (UnsupportedOperationException e) {
            System.out.println("Arrays.asList()返回的List不支持添加操作");
        }
        
        // 正确的转换方式
        java.util.List<String> mutableList = new java.util.ArrayList<>(Arrays.asList(colors));
        mutableList.add("黄色");
        System.out.println("可变List: " + mutableList);
        
        // List转数组
        String[] newArray = mutableList.toArray(new String[0]);
        System.out.println("List转数组: " + Arrays.toString(newArray));
        
        System.out.println();
    }
}
```

### 步骤3：创建集合演示类
创建 `src/main/java/com/example/CollectionsDemo.java` 文件：

```java
package com.example;

import java.util.*;

/**
 * Java集合框架演示类
 * 展示List、Set、Map等集合的使用方法
 */
public class CollectionsDemo {
    
    public static void main(String[] args) {
        System.out.println("=== Java集合框架演示 ===\n");
        
        // 1. List集合演示
        demonstrateListCollections();
        
        // 2. Set集合演示
        demonstrateSetCollections();
        
        // 3. Map集合演示
        demonstrateMapCollections();
        
        // 4. 集合工具类使用
        demonstrateCollectionUtils();
        
        // 5. 泛型集合演示
        demonstrateGenericCollections();
    }
    
    /**
     * 演示List集合的操作
     */
    private static void demonstrateListCollections() {
        System.out.println("1. List集合演示:");
        
        // ArrayList - 动态数组实现
        List<String> arrayList = new ArrayList<>();
        arrayList.add("苹果");
        arrayList.add("香蕉");
        arrayList.add("橙子");
        arrayList.add("苹果"); // 允许重复元素
        
        System.out.println("ArrayList内容: " + arrayList);
        System.out.println("ArrayList大小: " + arrayList.size());
        System.out.println("第二个元素: " + arrayList.get(1));
        
        // LinkedList - 链表实现
        List<Integer> linkedList = new LinkedList<>();
        linkedList.add(10);
        linkedList.add(20);
        linkedList.add(30);
        
        System.out.println("LinkedList内容: " + linkedList);
        
        // Vector - 线程安全的动态数组
        List<String> vector = new Vector<>();
        vector.add("线程安全");
        vector.add("Vector");
        System.out.println("Vector内容: " + vector);
        
        // List遍历方式
        System.out.println("\nList遍历方式:");
        
        // 方式1：增强for循环
        System.out.print("增强for循环: ");
        for (String item : arrayList) {
            System.out.print(item + " ");
        }
        System.out.println();
        
        // 方式2：迭代器
        System.out.print("迭代器遍历: ");
        Iterator<String> iterator = arrayList.iterator();
        while (iterator.hasNext()) {
            System.out.print(iterator.next() + " ");
        }
        System.out.println();
        
        // 方式3：forEach方法 (Java 8+)
        System.out.print("forEach方法: ");
        arrayList.forEach(item -> System.out.print(item + " "));
        System.out.println();
        
        // List操作
        arrayList.remove("香蕉");
        System.out.println("删除'香蕉'后: " + arrayList);
        
        arrayList.set(0, "红苹果");
        System.out.println("修改第一个元素后: " + arrayList);
        
        System.out.println();
    }
    
    /**
     * 演示Set集合的操作
     */
    private static void demonstrateSetCollections() {
        System.out.println("2. Set集合演示:");
        
        // HashSet - 基于哈希表实现，无序
        Set<String> hashSet = new HashSet<>();
        hashSet.add("Java");
        hashSet.add("Python");
        hashSet.add("Go");
        hashSet.add("Java"); // 重复元素不会被添加
        hashSet.add("JavaScript");
        
        System.out.println("HashSet内容: " + hashSet);
        System.out.println("HashSet大小: " + hashSet.size());
        System.out.println("是否包含'Python': " + hashSet.contains("Python"));
        
        // LinkedHashSet - 保持插入顺序
        Set<String> linkedHashSet = new LinkedHashSet<>();
        linkedHashSet.add("第一");
        linkedHashSet.add("第二");
        linkedHashSet.add("第三");
        
        System.out.println("LinkedHashSet内容: " + linkedHashSet);
        
        // TreeSet - 基于红黑树实现，自然排序
        Set<Integer> treeSet = new TreeSet<>();
        treeSet.add(5);
        treeSet.add(2);
        treeSet.add(8);
        treeSet.add(1);
        
        System.out.println("TreeSet内容: " + treeSet); // 自动排序
        
        // TreeSet自定义排序
        Set<String> sortedSet = new TreeSet<>((s1, s2) -> s2.compareTo(s1)); // 逆序
        sortedSet.addAll(Arrays.asList("apple", "banana", "cherry"));
        System.out.println("逆序TreeSet: " + sortedSet);
        
        System.out.println();
    }
    
    /**
     * 演示Map集合的操作
     */
    private static void demonstrateMapCollections() {
        System.out.println("3. Map集合演示:");
        
        // HashMap - 基于哈希表实现，无序
        Map<String, Integer> hashMap = new HashMap<>();
        hashMap.put("苹果", 5);
        hashMap.put("香蕉", 3);
        hashMap.put("橙子", 8);
        hashMap.put("苹果", 10); // 覆盖原有值
        
        System.out.println("HashMap内容: " + hashMap);
        System.out.println("苹果的数量: " + hashMap.get("苹果"));
        System.out.println("HashMap大小: " + hashMap.size());
        
        // LinkedHashMap - 保持插入顺序
        Map<String, String> linkedHashMap = new LinkedHashMap<>();
        linkedHashMap.put("first", "第一个");
        linkedHashMap.put("second", "第二个");
        linkedHashMap.put("third", "第三个");
        
        System.out.println("LinkedHashMap内容: " + linkedHashMap);
        
        // TreeMap - 基于红黑树实现，按键排序
        Map<Integer, String> treeMap = new TreeMap<>();
        treeMap.put(3, "第三");
        treeMap.put(1, "第一");
        treeMap.put(2, "第二");
        
        System.out.println("TreeMap内容: " + treeMap); // 按键自动排序
        
        // Map遍历方式
        System.out.println("\nMap遍历方式:");
        
        // 方式1：遍历键
        System.out.print("遍历键: ");
        for (String key : hashMap.keySet()) {
            System.out.print(key + " ");
        }
        System.out.println();
        
        // 方式2：遍历值
        System.out.print("遍历值: ");
        for (Integer value : hashMap.values()) {
            System.out.print(value + " ");
        }
        System.out.println();
        
        // 方式3：遍历键值对
        System.out.print("遍历键值对: ");
        for (Map.Entry<String, Integer> entry : hashMap.entrySet()) {
            System.out.print(entry.getKey() + "=" + entry.getValue() + " ");
        }
        System.out.println();
        
        // 方式4：forEach方法
        System.out.print("forEach方法: ");
        hashMap.forEach((key, value) -> System.out.print(key + ":" + value + " "));
        System.out.println();
        
        System.out.println();
    }
    
    /**
     * 演示集合工具类的使用
     */
    private static void demonstrateCollectionUtils() {
        System.out.println("4. 集合工具类使用:");
        
        List<Integer> numbers = Arrays.asList(5, 2, 8, 1, 9, 3);
        System.out.println("原列表: " + numbers);
        
        // Collections工具类方法
        Collections.sort(numbers);
        System.out.println("排序后: " + numbers);
        
        Collections.reverse(numbers);
        System.out.println("反转后: " + numbers);
        
        Collections.shuffle(numbers);
        System.out.println("随机打乱: " + numbers);
        
        System.out.println("最大值: " + Collections.max(numbers));
        System.out.println("最小值: " + Collections.min(numbers));
        
        // 创建不可变集合
        List<String> immutableList = Collections.unmodifiableList(
            Arrays.asList("不可变", "元素"));
        System.out.println("不可变列表: " + immutableList);
        
        // 创建同步集合（线程安全）
        List<String> syncList = Collections.synchronizedList(new ArrayList<>());
        syncList.add("线程安全");
        syncList.add("集合");
        System.out.println("同步列表: " + syncList);
        
        System.out.println();
    }
    
    /**
     * 演示泛型集合的使用
     */
    private static void demonstrateGenericCollections() {
        System.out.println("5. 泛型集合演示:");
        
        // 泛型List
        List<String> stringList = new ArrayList<>();
        stringList.add("Hello");
        stringList.add("World");
        // stringList.add(123); // 编译错误
        
        // 泛型Map
        Map<String, List<Integer>> scoreMap = new HashMap<>();
        scoreMap.put("张三", Arrays.asList(85, 92, 78));
        scoreMap.put("李四", Arrays.asList(90, 88, 95));
        
        System.out.println("成绩Map: " + scoreMap);
        
        // 通配符泛型
        List<?> unknownList = stringList; // 无界通配符
        // unknownList.add("test"); // 编译错误，无法添加元素
        
        List<? extends Number> upperBoundList = Arrays.asList(1, 2, 3); // 上界通配符
        // upperBoundList.add(4); // 编译错误
        
        List<? super Integer> lowerBoundList = new ArrayList<Number>(); // 下界通配符
        lowerBoundList.add(100); // 可以添加Integer及其子类型
        
        System.out.println("下界通配符列表: " + lowerBoundList);
        
        System.out.println();
    }
}
```

### 步骤4：创建综合演示类
创建 `src/main/java/com/example/ArraysCollectionsDemo.java` 文件：

```java
package com.example;

import java.util.*;
import java.util.stream.Collectors;

/**
 * 数组与集合综合应用演示
 * 展示实际开发中的典型使用场景
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
```

### 步骤5：编译和运行
```bash
# 编译所有Java文件
javac src/main/java/com/example/*.java

# 分别运行各个演示程序
java com.example.ArraysDemo
java com.example.CollectionsDemo
java com.example.ArraysCollectionsDemo
```

## 🔍 代码详解

### 1. 数组特点
- **固定大小**：创建后长度不可改变
- **类型安全**：同一数组只能存储相同类型元素
- **内存连续**：元素在内存中连续存储
- **索引访问**：通过索引快速访问元素

### 2. 集合框架体系
- **Collection接口**：List、Set、Queue的父接口
- **Map接口**：键值对存储结构
- **List**：有序、可重复集合
- **Set**：无序、不可重复集合
- **Map**：键值对映射关系

### 3. 常用实现类选择
- **ArrayList**：频繁查询、偶尔插入删除
- **LinkedList**：频繁插入删除、偶尔查询
- **HashSet**：快速查找、去重需求
- **TreeSet**：排序需求
- **HashMap**：快速键值对查找
- **TreeMap**：按键排序的键值对

## 🧪 验证测试

### 功能验证清单
- [ ] 数组的基本操作（声明、初始化、遍历）
- [ ] 多维数组的使用
- [ ] 数组工具类方法
- [ ] List集合的各种操作
- [ ] Set集合的特性和去重功能
- [ ] Map集合的键值对操作
- [ ] 集合工具类的使用
- [ ] 泛型集合的安全性
- [ ] 实际应用场景的实现

### 性能测试要点
- 不同集合类型的插入性能对比
- 查找操作的时间复杂度差异
- 内存使用情况分析

## ❓ 常见问题

### Q1: 什么时候使用数组而不是集合？
**答**：当数据量固定且需要高性能索引访问时使用数组；当需要动态大小和丰富操作时使用集合。

### Q2: ArrayList和LinkedList有什么区别？
**答**：ArrayList基于动态数组，适合随机访问；LinkedList基于双向链表，适合频繁插入删除。

### Q3: HashSet是如何保证元素不重复的？
**答**：通过元素的hashCode()和equals()方法来判断元素是否相同。

### Q4: 为什么Map不是Collection的子接口？
**答**：因为Map存储的是键值对，而Collection存储的是单个元素，数据结构本质不同。

## 📚 扩展学习

### 相关技术
- [Java泛型编程](../java-generics-demo/)
- [Java异常处理](../java-exception-handling-demo/)
- [Java流式API](../java-streams-demo/)

### 进阶主题
- 并发集合（ConcurrentHashMap等）
- 不可变集合
- 集合的序列化
- 自定义集合实现

### 企业级应用
- 数据库查询结果处理
- 缓存数据管理
- 配置信息存储
- 业务数据统计分析

---
> **💡 提示**: 熟练掌握数组和集合是Java编程的基础，建议多练习不同场景下的选择和使用。
## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

```bash
# 请根据实际案例替换
./scripts/demo.sh
```
