package com.example.demo.util;

import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.NullAndEmptySource;

import static org.assertj.core.api.Assertions.*;

/**
 * StringUtils类测试
 * 
 * 演示更多JUnit5特性和AssertJ断言
 */
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)  // 指定测试方法执行顺序
@DisplayName("字符串工具类测试")
public class StringUtilsTest {
    
    // ========== 反转字符串测试 ==========
    
    @Test
    @Order(1)
    @DisplayName("反转正常字符串")
    void testReverseNormalString() {
        assertThat(StringUtils.reverse("hello")).isEqualTo("olleh");
        assertThat(StringUtils.reverse("Java")).isEqualTo("avaJ");
    }
    
    @Test
    @Order(2)
    @DisplayName("反转空字符串")
    void testReverseEmptyString() {
        assertThat(StringUtils.reverse("")).isEmpty();
    }
    
    @Test
    @Order(3)
    @DisplayName("反转null")
    void testReverseNull() {
        assertThat(StringUtils.reverse(null)).isNull();
    }
    
    @Test
    @Order(4)
    @DisplayName("反转单字符")
    void testReverseSingleChar() {
        assertThat(StringUtils.reverse("a")).isEqualTo("a");
    }
    
    // ========== 回文判断测试 ==========
    
    @ParameterizedTest
    @DisplayName("回文字符串测试")
    @CsvSource({
            "level, true",
            "radar, true",
            "madam, true",
            "hello, false",
            "world, false"
    })
    void testIsPalindrome(String input, boolean expected) {
        assertThat(StringUtils.isPalindrome(input)).isEqualTo(expected);
    }
    
    @Test
    @DisplayName("空字符串不是回文")
    void testIsPalindromeEmpty() {
        assertThat(StringUtils.isPalindrome("")).isFalse();
    }
    
    @Test
    @DisplayName("null不是回文")
    void testIsPalindromeNull() {
        assertThat(StringUtils.isPalindrome(null)).isFalse();
    }
    
    // ========== 字符统计测试 ==========
    
    @ParameterizedTest
    @DisplayName("字符出现次数测试")
    @CsvSource({
            "hello, l, 2",
            "banana, a, 3",
            "java, v, 1",
            "test, x, 0"
    })
    void testCountOccurrences(String str, char target, int expected) {
        assertThat(StringUtils.countOccurrences(str, target)).isEqualTo(expected);
    }
    
    @Test
    @DisplayName("统计空字符串")
    void testCountOccurrencesEmpty() {
        assertThat(StringUtils.countOccurrences("", 'a')).isZero();
    }
    
    // ========== 字符串截断测试 ==========
    
    @Nested
    @DisplayName("字符串截断测试组")
    class TruncateTests {
        
        @Test
        @DisplayName("不需要截断")
        void testTruncateNotNeeded() {
            String input = "hello";
            assertThat(StringUtils.truncate(input, 10)).isEqualTo("hello");
        }
        
        @Test
        @DisplayName("需要截断")
        void testTruncateNeeded() {
            String input = "hello world";
            assertThat(StringUtils.truncate(input, 8)).isEqualTo("hello...");
        }
        
        @Test
        @DisplayName("截断长度很小")
        void testTruncateSmallLength() {
            String input = "hello";
            assertThat(StringUtils.truncate(input, 2)).isEqualTo("he");
        }
        
        @ParameterizedTest
        @NullAndEmptySource  // 提供null和空字符串参数
        @DisplayName("截断null和空字符串")
        void testTruncateNullAndEmpty(String input) {
            assertThat(StringUtils.truncate(input, 10)).isEqualTo(input);
        }
    }
    
    // ========== 条件执行测试 ==========
    
    @Test
    @EnabledOnOs(org.junit.jupiter.api.condition.OS.WINDOWS)
    @DisplayName("仅在Windows上执行")
    void windowsOnlyTest() {
        assertThat(true).isTrue();
    }
    
    @Test
    @EnabledOnOs(org.junit.jupiter.api.condition.OS.MAC)
    @DisplayName("仅在Mac上执行")
    void macOnlyTest() {
        assertThat(true).isTrue();
    }
    
    // ========== 重复测试 ==========
    
    @RepeatedTest(value = 3, name = "重复测试 {currentRepetition}/{totalRepetitions}")
    @DisplayName("重复执行测试")
    void repeatedTest() {
        assertThat(StringUtils.reverse("abc")).isEqualTo("cba");
    }
    
    // ========== 动态测试 ==========
    
    @TestFactory
    @DisplayName("动态测试")
    java.util.stream.Stream<DynamicTest> dynamicTests() {
        return java.util.stream.Stream.of("racecar", "radar", "level")
                .map(text -> DynamicTest.dynamicTest("测试 " + text,
                        () -> assertThat(StringUtils.isPalindrome(text)).isTrue()));
    }
}
