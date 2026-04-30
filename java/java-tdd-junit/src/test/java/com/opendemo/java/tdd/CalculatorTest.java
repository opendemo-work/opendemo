package com.opendemo.java.tdd;

import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {
    private Calculator calculator;

    @BeforeEach
    void setUp() {
        calculator = new Calculator();
    }

    @Test
    @DisplayName("Adding two positive numbers")
    void testAdd() {
        assertEquals(5, calculator.add(2, 3));
    }

    @Test
    @DisplayName("Adding negative numbers")
    void testAddNegative() {
        assertEquals(-5, calculator.add(-2, -3));
    }

    @Test
    @DisplayName("Adding zero")
    void testAddZero() {
        assertEquals(5, calculator.add(5, 0));
    }

    @Test
    @DisplayName("Subtraction")
    void testSubtract() {
        assertEquals(2, calculator.subtract(5, 3));
    }

    @Test
    @DisplayName("Multiplication")
    void testMultiply() {
        assertEquals(15, calculator.multiply(3, 5));
    }

    @Test
    @DisplayName("Division")
    void testDivide() {
        assertEquals(2.5, calculator.divide(5, 2), 0.001);
    }

    @Test
    @DisplayName("Division by zero throws exception")
    void testDivideByZero() {
        assertThrows(ArithmeticException.class, () -> calculator.divide(10, 0));
    }

    @ParameterizedTest
    @CsvSource({"1, 1, 2", "2, 3, 5", "10, 20, 30", "-5, 5, 0"})
    void testAddParameterized(int a, int b, int expected) {
        assertEquals(expected, calculator.add(a, b));
    }

    @ParameterizedTest
    @CsvSource({"10, 2, 5.0", "9, 3, 3.0", "7, 2, 3.5"})
    void testDivideParameterized(int a, int b, double expected) {
        assertEquals(expected, calculator.divide(a, b), 0.001);
    }
}
