package com.example.demo.util;

/**
 * 字符串工具类
 * 
 * 用于演示JUnit5参数化测试
 */
public class StringUtils {
    
    /**
     * 反转字符串
     */
    public static String reverse(String str) {
        if (str == null) {
            return null;
        }
        return new StringBuilder(str).reverse().toString();
    }
    
    /**
     * 判断是否为回文
     */
    public static boolean isPalindrome(String str) {
        if (str == null || str.isEmpty()) {
            return false;
        }
        String reversed = reverse(str);
        return str.equals(reversed);
    }
    
    /**
     * 统计字符出现次数
     */
    public static int countOccurrences(String str, char target) {
        if (str == null || str.isEmpty()) {
            return 0;
        }
        int count = 0;
        for (char c : str.toCharArray()) {
            if (c == target) {
                count++;
            }
        }
        return count;
    }
    
    /**
     * 截断字符串（超出长度添加省略号）
     */
    public static String truncate(String str, int maxLength) {
        if (str == null) {
            return null;
        }
        if (str.length() <= maxLength) {
            return str;
        }
        if (maxLength <= 3) {
            return str.substring(0, maxLength);
        }
        return str.substring(0, maxLength - 3) + "...";
    }
}
