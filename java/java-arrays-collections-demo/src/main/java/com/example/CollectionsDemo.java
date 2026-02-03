package com.example;

import java.util.*;

/**
 * Java集合框架演示类
 * 展示List、Set、Map等集合的使用方法
 * 
 * @author OpenDemo Team
 * @version 1.0.0
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