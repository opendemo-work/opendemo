package com.opendemo.java.string;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

/**
 * StringOperationsDemo测试类
 * 
 * 测试字符串操作的各种功能
 * 
 * @author OpenDemo Team
 */
class StringOperationsDemoTest {
    
    private StringOperationsDemo demo;
    
    @BeforeEach
    void setUp() {
        demo = new StringOperationsDemo();
    }
    
    @Test
    void testStringCreation() {
        // 测试字符串创建的基本功能
        String literal = "Hello";
        String object = new String("Hello");
        char[] chars = {'H', 'e', 'l', 'l', 'o'};
        String fromChars = new String(chars);
        
        assertNotNull(literal);
        assertNotNull(object);
        assertNotNull(fromChars);
        assertEquals("Hello", fromChars);
    }
    
    @Test
    void testStringComparison() {
        String str1 = "Hello";
        String str2 = "Hello";
        String str3 = new String("Hello");
        String str4 = "hello";
        
        // 测试equals方法
        assertTrue(str1.equals(str2));
        assertTrue(str1.equals(str3));
        assertFalse(str1.equals(str4));
        
        // 测试equalsIgnoreCase方法
        assertTrue(str1.equalsIgnoreCase(str4));
        
        // 测试compareTo方法
        assertTrue("Apple".compareTo("Banana") < 0);
        assertTrue("Banana".compareTo("Apple") > 0);
        assertEquals(0, "Apple".compareTo("Apple"));
    }
    
    @Test
    void testStringSearching() {
        String text = "Hello World! This is a sample text.";
        
        // 测试indexOf
        assertEquals(13, text.indexOf("sample"));
        assertEquals(5, text.indexOf(" "));
        
        // 测试contains
        assertTrue(text.contains("World"));
        assertFalse(text.contains("Java"));
        
        // 测试startsWith和endsWith
        assertTrue(text.startsWith("Hello"));
        assertTrue(text.endsWith("text."));
        
        // 测试charAt
        assertEquals('H', text.charAt(0));
        assertEquals('.', text.charAt(text.length() - 1));
    }
    
    @Test
    void testStringModification() {
        String original = "  Hello World  ";
        
        // 测试trim
        assertEquals("Hello World", original.trim());
        
        // 测试大小写转换
        assertEquals("HELLO WORLD", original.trim().toUpperCase());
        assertEquals("hello world", original.trim().toLowerCase());
        
        // 测试replace
        assertEquals("HeLLo WorLd", original.trim().replace('l', 'L'));
        
        // 测试substring
        assertEquals("World", original.trim().substring(6));
        assertEquals("Hello", original.trim().substring(0, 5));
    }
    
    @Test
    void testStringSplit() {
        String csv = "apple,banana,cherry";
        String[] parts = csv.split(",");
        
        assertEquals(3, parts.length);
        assertEquals("apple", parts[0]);
        assertEquals("banana", parts[1]);
        assertEquals("cherry", parts[2]);
    }
    
    @Test
    void testStringJoin() {
        String[] fruits = {"apple", "banana", "cherry"};
        String joined = String.join(" | ", fruits);
        
        assertEquals("apple | banana | cherry", joined);
    }
    
    @Test
    void testStringValidation() {
        // 测试邮箱验证
        String validEmail = "user@example.com";
        String invalidEmail = "invalid.email";
        
        assertTrue(validEmail.matches("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$"));
        assertFalse(invalidEmail.matches("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$"));
        
        // 测试手机号验证
        String validPhone = "13812345678";
        String invalidPhone = "12345";
        
        assertTrue(validPhone.matches("^1[3-9]\\d{9}$"));
        assertFalse(invalidPhone.matches("^1[3-9]\\d{9}$"));
    }
    
    @Test
    void testStringBuilderPerformance() {
        // 测试StringBuilder的基本功能
        StringBuilder sb = new StringBuilder();
        sb.append("Hello").append(" ").append("World");
        
        assertEquals("Hello World", sb.toString());
        assertEquals(11, sb.length());
        
        // 测试插入和删除
        sb.insert(5, " Beautiful");
        assertEquals("Hello Beautiful World", sb.toString());
        
        sb.delete(5, 15);
        assertEquals("Hello World", sb.toString());
    }
    
    @Test
    void testStringFormat() {
        String name = "张三";
        int age = 25;
        double salary = 8500.50;
        
        String formatted = String.format("姓名: %s, 年龄: %d, 薪资: %.2f", name, age, salary);
        assertTrue(formatted.contains("张三"));
        assertTrue(formatted.contains("25"));
        assertTrue(formatted.contains("8500.50"));
    }
    
    @Test
    void testEmptyAndNullStrings() {
        String empty = "";
        String nullString = null;
        String whitespace = "   ";
        
        // 测试空字符串
        assertTrue(empty.isEmpty());
        assertEquals(0, empty.length());
        
        // 测试空白字符串
        assertFalse(whitespace.isEmpty());
        assertTrue(whitespace.trim().isEmpty());
        
        // 测试null安全操作
        assertThrows(NullPointerException.class, () -> nullString.length());
    }
}