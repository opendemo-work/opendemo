package com.example.demo.service;

import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;

import static org.assertj.core.api.Assertions.*;

/**
 * Calculator类测试
 * 
 * 演示JUnit5基础注解和断言
 */
@DisplayName("计算器测试")
public class CalculatorTest {
    
    private Calculator calculator;
    
    /**
     * @BeforeAll - 在所有测试方法之前执行，只执行一次
     * 必须是static方法
     */
    @BeforeAll
    static void initAll() {
        System.out.println("[BeforeAll] 测试类初始化");
    }
    
    /**
     * @BeforeEach - 在每个测试方法之前执行
     */
    @BeforeEach
    void init() {
        calculator = new Calculator();
        System.out.println("[BeforeEach] 创建Calculator实例");
    }
    
    /**
     * @AfterEach - 在每个测试方法之后执行
     */
    @AfterEach
    void tearDown() {
        System.out.println("[AfterEach] 清理资源");
    }
    
    /**
     * @AfterAll - 在所有测试方法之后执行，只执行一次
     * 必须是static方法
     */
    @AfterAll
    static void tearDownAll() {
        System.out.println("[AfterAll] 测试类清理");
    }
    
    // ========== 基础测试 ==========
    
    @Test
    @DisplayName("加法测试 - 两个正数")
    void testAddPositiveNumbers() {
        // given
        int a = 2;
        int b = 3;
        
        // when
        int result = calculator.add(a, b);
        
        // then
        assertThat(result).isEqualTo(5);
    }
    
    @Test
    @DisplayName("加法测试 - 包含负数")
    void testAddWithNegative() {
        assertThat(calculator.add(-2, 3)).isEqualTo(1);
        assertThat(calculator.add(-2, -3)).isEqualTo(-5);
    }
    
    @Test
    @DisplayName("减法测试")
    void testSubtract() {
        assertThat(calculator.subtract(5, 3)).isEqualTo(2);
        assertThat(calculator.subtract(3, 5)).isEqualTo(-2);
    }
    
    @Test
    @DisplayName("乘法测试")
    void testMultiply() {
        assertThat(calculator.multiply(4, 5)).isEqualTo(20);
        assertThat(calculator.multiply(-4, 5)).isEqualTo(-20);
    }
    
    @Test
    @DisplayName("除法测试 - 正常情况")
    void testDivide() {
        assertThat(calculator.divide(10, 2)).isEqualTo(5);
        assertThat(calculator.divide(7, 2)).isEqualTo(3);
    }
    
    @Test
    @DisplayName("除法测试 - 除数为0应抛出异常")
    void testDivideByZero() {
        // AssertJ异常断言
        assertThatThrownBy(() -> calculator.divide(10, 0))
                .isInstanceOf(ArithmeticException.class)
                .hasMessageContaining("除数不能为0");
    }
    
    @Test
    @DisplayName("平方根测试")
    void testSqrt() {
        assertThat(calculator.sqrt(4)).isEqualTo(2.0);
        assertThat(calculator.sqrt(9)).isEqualTo(3.0);
        assertThat(calculator.sqrt(2)).isCloseTo(1.414, within(0.001));
    }
    
    @Test
    @DisplayName("平方根测试 - 负数应抛出异常")
    void testSqrtNegative() {
        assertThatExceptionOfType(IllegalArgumentException.class)
                .isThrownBy(() -> calculator.sqrt(-1))
                .withMessage("不能对负数求平方根");
    }
    
    // ========== 参数化测试 ==========
    
    @ParameterizedTest
    @DisplayName("偶数判断测试")
    @ValueSource(ints = {0, 2, 4, 6, 100, -2, -4})
    void testIsEven(int number) {
        assertThat(calculator.isEven(number)).isTrue();
    }
    
    @ParameterizedTest
    @DisplayName("奇数判断测试")
    @ValueSource(ints = {1, 3, 5, 7, 99, -1, -3})
    void testIsOdd(int number) {
        assertThat(calculator.isEven(number)).isFalse();
    }
    
    @ParameterizedTest
    @DisplayName("加法参数化测试")
    @CsvSource({
            "1, 1, 2",
            "2, 3, 5",
            "10, 20, 30",
            "-1, 1, 0",
            "-5, -5, -10"
    })
    void testAddParameterized(int a, int b, int expected) {
        assertThat(calculator.add(a, b)).isEqualTo(expected);
    }
    
    // ========== 断言组合 ==========
    
    @Test
    @DisplayName("复杂断言测试")
    void testComplexAssertions() {
        int result = calculator.add(2, 3);
        
        // 多个断言
        assertThat(result)
                .isEqualTo(5)
                .isPositive()
                .isGreaterThan(4)
                .isLessThan(10);
    }
    
    // ========== 禁用测试 ==========
    
    @Test
    @Disabled("此测试暂时禁用，等待需求确认")
    @DisplayName("被禁用的测试")
    void disabledTest() {
        // 此测试不会执行
    }
    
    // ========== 超时测试 ==========
    
    @Test
    @Timeout(value = 1) // 1秒内必须完成
    @DisplayName("超时测试")
    void testTimeout() {
        // 模拟快速操作
        calculator.add(1, 2);
    }
}
