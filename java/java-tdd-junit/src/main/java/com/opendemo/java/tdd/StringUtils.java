package com.opendemo.java.tdd;

public class StringUtils {
    public static boolean isEmpty(String str) {
        return str == null || str.isEmpty();
    }

    public static boolean isBlank(String str) {
        return str == null || str.trim().isEmpty();
    }

    public static String reverse(String str) {
        if (str == null) {
            return null;
        }
        return new StringBuilder(str).reverse().toString();
    }

    public static String capitalize(String str) {
        if (str == null || str.isEmpty()) {
            return str;
        }
        return str.substring(0, 1).toUpperCase() + str.substring(1);
    }

    public static int countOccurrences(String str, String sub) {
        if (str == null || sub == null || sub.isEmpty()) {
            return 0;
        }
        int count = 0;
        int idx = 0;
        while ((idx = str.indexOf(sub, idx)) != -1) {
            count++;
            idx += sub.length();
        }
        return count;
    }

    public static boolean isPalindrome(String str) {
        if (str == null) {
            return false;
        }
        String normalized = str.toLowerCase().replaceAll("[^a-z0-9]", "");
        return normalized.equals(new StringBuilder(normalized).reverse().toString());
    }

    public static String truncate(String str, int maxLength) {
        if (str == null) {
            return null;
        }
        if (maxLength < 0) {
            throw new IllegalArgumentException("Max length must be non-negative");
        }
        if (str.length() <= maxLength) {
            return str;
        }
        return str.substring(0, maxLength) + "...";
    }
}
