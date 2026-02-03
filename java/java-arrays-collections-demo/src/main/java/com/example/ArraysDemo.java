package com.example;

import java.util.Arrays;

/**
 * Java数组操作演示类
 * 展示数组的声明、初始化、遍历和常用操作
 * 
 * @author OpenDemo Team
 * @version 1.0.0
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