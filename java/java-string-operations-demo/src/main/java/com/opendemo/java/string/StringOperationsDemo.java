package com.opendemo.java.string;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Java字符串操作完整示例
 * 
 * 演示String类的各种常用方法和最佳实践
 * 包括：创建、比较、查找、替换、分割、格式化等操作
 * 
 * @author OpenDemo Team
 * @since 1.0.0
 */
public class StringOperationsDemo {
    
    private static final Logger logger = LoggerFactory.getLogger(StringOperationsDemo.class);
    
    // 常量定义
    private static final String SAMPLE_TEXT = "Hello World! This is a sample text for Java String operations demonstration.";
    private static final String EMAIL_PATTERN = "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$";
    
    public static void main(String[] args) {
        logger.info("=== Java字符串操作完整示例 ===");
        
        StringOperationsDemo demo = new StringOperationsDemo();
        
        // 1. 字符串创建方式
        demo.demonstrateStringCreation();
        
        // 2. 字符串比较操作
        demo.demonstrateStringComparison();
        
        // 3. 字符串查找操作
        demo.demonstrateStringSearching();
        
        // 4. 字符串修改操作
        demo.demonstrateStringModification();
        
        // 5. 字符串分割和连接
        demo.demonstrateStringSplitJoin();
        
        // 6. 字符串格式化
        demo.demonstrateStringFormatting();
        
        // 7. 字符串验证
        demo.demonstrateStringValidation();
        
        // 8. 性能考虑
        demo.demonstratePerformanceConsiderations();
        
        logger.info("=== 示例演示完成 ===");
    }
    
    /**
     * 演示字符串的多种创建方式
     */
    public void demonstrateStringCreation() {
        logger.info("\n--- 1. 字符串创建方式 ---");
        
        // 字面量方式（推荐）
        String str1 = "Hello World";
        logger.info("字面量创建: {}", str1);
        
        // new关键字方式
        String str2 = new String("Hello World");
        logger.info("new关键字创建: {}", str2);
        
        // 字符数组方式
        char[] chars = {'H', 'e', 'l', 'l', 'o'};
        String str3 = new String(chars);
        logger.info("字符数组创建: {}", str3);
        
        // 字节数组方式
        byte[] bytes = {72, 101, 108, 108, 111}; // ASCII码
        String str4 = new String(bytes);
        logger.info("字节数组创建: {}", str4);
        
        // StringBuilder方式
        StringBuilder sb = new StringBuilder();
        sb.append("Hello").append(" ").append("World");
        String str5 = sb.toString();
        logger.info("StringBuilder创建: {}", str5);
        
        // StringBuffer方式（线程安全）
        StringBuffer stringBuffer = new StringBuffer();
        stringBuffer.append("Thread").append(" ").append("Safe");
        String str6 = stringBuffer.toString();
        logger.info("StringBuffer创建: {}", str6);
    }
    
    /**
     * 演示字符串比较操作
     */
    public void demonstrateStringComparison() {
        logger.info("\n--- 2. 字符串比较操作 ---");
        
        String str1 = "Hello";
        String str2 = "Hello";
        String str3 = new String("Hello");
        String str4 = "hello";
        
        // == 比较引用
        logger.info("str1 == str2: {}", str1 == str2); // true (字符串池)
        logger.info("str1 == str3: {}", str1 == str3); // false (不同对象)
        
        // equals() 比较内容
        logger.info("str1.equals(str2): {}", str1.equals(str2)); // true
        logger.info("str1.equals(str3): {}", str1.equals(str3)); // true
        logger.info("str1.equals(str4): {}", str1.equals(str4)); // false
        
        // equalsIgnoreCase() 忽略大小写比较
        logger.info("str1.equalsIgnoreCase(str4): {}", str1.equalsIgnoreCase(str4)); // true
        
        // compareTo() 字典序比较
        logger.info("\"Apple\".compareTo(\"Banana\"): {}", "Apple".compareTo("Banana")); // 负数
        logger.info("\"Banana\".compareTo(\"Apple\"): {}", "Banana".compareTo("Apple")); // 正数
        logger.info("\"Apple\".compareTo(\"Apple\"): {}", "Apple".compareTo("Apple")); // 0
    }
    
    /**
     * 演示字符串查找操作
     */
    public void demonstrateStringSearching() {
        logger.info("\n--- 3. 字符串查找操作 ---");
        
        String text = SAMPLE_TEXT;
        logger.info("搜索文本: {}", text);
        
        // indexOf() 查找首次出现位置
        int index1 = text.indexOf("sample");
        logger.info("indexOf(\"sample\"): {}", index1);
        
        // lastIndexOf() 查找最后出现位置
        int index2 = text.lastIndexOf(" ");
        logger.info("lastIndexOf(\" \"): {}", index2);
        
        // contains() 是否包含子字符串
        boolean contains = text.contains("Java");
        logger.info("contains(\"Java\"): {}", contains);
        
        // startsWith() 是否以某字符串开头
        boolean starts = text.startsWith("Hello");
        logger.info("startsWith(\"Hello\"): {}", starts);
        
        // endsWith() 是否以某字符串结尾
        boolean ends = text.endsWith("demonstration.");
        logger.info("endsWith(\"demonstration.\"): {}", ends);
        
        // charAt() 获取指定位置字符
        char ch = text.charAt(0);
        logger.info("charAt(0): {}", ch);
    }
    
    /**
     * 演示字符串修改操作
     */
    public void demonstrateStringModification() {
        logger.info("\n--- 4. 字符串修改操作 ---");
        
        String original = "  Hello World  ";
        logger.info("原始字符串: '{}'", original);
        
        // trim() 去除首尾空白
        String trimmed = original.trim();
        logger.info("trim(): '{}'", trimmed);
        
        // toUpperCase() 转大写
        String upper = trimmed.toUpperCase();
        logger.info("toUpperCase(): '{}'", upper);
        
        // toLowerCase() 转小写
        String lower = trimmed.toLowerCase();
        logger.info("toLowerCase(): '{}'", lower);
        
        // replace() 替换字符或字符串
        String replaced = trimmed.replace('l', 'L');
        logger.info("replace('l', 'L'): '{}'", replaced);
        
        String replacedAll = trimmed.replaceAll("o", "0");
        logger.info("replaceAll(\"o\", \"0\"): '{}'", replacedAll);
        
        // substring() 截取子字符串
        String sub1 = trimmed.substring(6);
        logger.info("substring(6): '{}'", sub1);
        
        String sub2 = trimmed.substring(0, 5);
        logger.info("substring(0, 5): '{}'", sub2);
    }
    
    /**
     * 演示字符串分割和连接
     */
    public void demonstrateStringSplitJoin() {
        logger.info("\n--- 5. 字符串分割和连接 ---");
        
        String csvData = "apple,banana,cherry,date";
        logger.info("CSV数据: {}", csvData);
        
        // split() 分割字符串
        String[] fruits = csvData.split(",");
        logger.info("split(\",\") 结果:");
        for (int i = 0; i < fruits.length; i++) {
            logger.info("  [{}]: {}", i, fruits[i]);
        }
        
        // join() 连接字符串（Java 8+）
        List<String> fruitList = Arrays.asList(fruits);
        String joined = String.join(" | ", fruitList);
        logger.info("String.join(\" | \", list): {}", joined);
        
        // 使用Stream API连接
        String streamJoined = fruitList.stream()
                .map(String::toUpperCase)
                .collect(Collectors.joining(", "));
        logger.info("Stream joining: {}", streamJoined);
    }
    
    /**
     * 演示字符串格式化
     */
    public void demonstrateStringFormatting() {
        logger.info("\n--- 6. 字符串格式化 ---");
        
        String name = "张三";
        int age = 25;
        double salary = 8500.50;
        
        // printf() 格式化输出
        System.out.printf("姓名: %s, 年龄: %d, 薪资: %.2f%n", name, age, salary);
        
        // format() 返回格式化字符串
        String formatted = String.format("员工信息 - 姓名: %s, 年龄: %d, 薪资: ¥%,.2f", 
                                       name, age, salary);
        logger.info("format() 结果: {}", formatted);
        
        // 常用格式化符号
        logger.info("整数格式化: %d -> %05d", 42, 42);
        logger.info("浮点数格式化: %f -> %.2f", 3.14159, 3.14159);
        logger.info("百分比格式化: %f -> %.1f%%", 0.875, 0.875 * 100);
        logger.info("左对齐格式化: %-10s|", "左对齐");
        logger.info("右对齐格式化: %10s|", "右对齐");
    }
    
    /**
     * 演示字符串验证
     */
    public void demonstrateStringValidation() {
        logger.info("\n--- 7. 字符串验证 ---");
        
        String[] testEmails = {
            "user@example.com",
            "invalid.email",
            "user@",
            "@domain.com",
            "valid_email123@test-domain.co.uk"
        };
        
        logger.info("邮箱验证测试:");
        for (String email : testEmails) {
            boolean isValid = email.matches(EMAIL_PATTERN);
            logger.info("  {} -> {}", email, isValid ? "✅ 有效" : "❌ 无效");
        }
        
        // 其他常用验证
        String phoneNumber = "13812345678";
        boolean isPhoneValid = phoneNumber.matches("^1[3-9]\\d{9}$");
        logger.info("手机号验证: {} -> {}", phoneNumber, isPhoneValid ? "有效" : "无效");
        
        String chineseName = "李小龙";
        boolean isChineseValid = chineseName.matches("^[\\u4e00-\\u9fa5]{2,4}$");
        logger.info("中文姓名验证: {} -> {}", chineseName, isChineseValid ? "有效" : "无效");
    }
    
    /**
     * 演示性能考虑和最佳实践
     */
    public void demonstratePerformanceConsiderations() {
        logger.info("\n--- 8. 性能考虑和最佳实践 ---");
        
        // StringBuilder vs String concatenation
        long startTime = System.currentTimeMillis();
        
        // 低效的字符串拼接
        String result1 = "";
        for (int i = 0; i < 1000; i++) {
            result1 += "item" + i + ";";
        }
        long time1 = System.currentTimeMillis() - startTime;
        
        // 高效的StringBuilder
        startTime = System.currentTimeMillis();
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 1000; i++) {
            sb.append("item").append(i).append(";");
        }
        String result2 = sb.toString();
        long time2 = System.currentTimeMillis() - startTime;
        
        logger.info("String拼接耗时: {} ms", time1);
        logger.info("StringBuilder耗时: {} ms", time2);
        logger.info("性能提升: {:.2f}倍", (double) time1 / time2);
        
        // 不可变性演示
        String immutableStr = "Original";
        String modifiedStr = immutableStr.concat(" Modified");
        logger.info("原字符串: {}", immutableStr);
        logger.info("修改后字符串: {}", modifiedStr);
        logger.info("原字符串是否改变: {}", immutableStr.equals("Original"));
    }
}