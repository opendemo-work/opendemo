package com.opendemo.java.variables;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class VariablesTypesDemoTest {

    @Test
    void testIntegerTypes() {
        byte smallNumber = 100;
        short mediumNumber = 30000;
        int regularNumber = 2000000000;
        long bigNumber = 9000000000L;

        assertEquals(100, smallNumber);
        assertEquals(30000, mediumNumber);
        assertEquals(2000000000, regularNumber);
        assertEquals(9000000000L, bigNumber);
    }

    @Test
    void testFloatingPointTypes() {
        float price = 19.99F;
        double preciseValue = 3.14159265359;

        assertTrue(price > 19.98F && price < 20.00F);
        assertTrue(preciseValue > 3.14159 && preciseValue < 3.14160);
    }

    @Test
    void testCharAndBooleanTypes() {
        char letter = 'A';
        char unicodeChar = '\u0041';
        boolean isJavaFun = true;
        boolean isFinished = false;

        assertEquals('A', letter);
        assertEquals('A', unicodeChar);
        assertEquals(letter, unicodeChar);
        assertTrue(isJavaFun);
        assertFalse(isFinished);
    }

    @Test
    void testStringType() {
        String greeting = "Hello";
        String name = "World";
        String message = greeting + " " + name + "!";

        assertEquals("Hello World!", message);
        assertEquals(12, message.length());
        assertEquals("HELLO WORLD!", message.toUpperCase());
        assertTrue(message.contains("World"));
        assertFalse(message.contains("Java"));
    }

    @Test
    void testArrayTypes() {
        int[] numbers = {1, 2, 3, 4, 5};
        String[] fruits = {"苹果", "香蕉", "橙子"};

        assertEquals(5, numbers.length);
        assertEquals(1, numbers[0]);
        assertEquals(5, numbers[4]);
        assertEquals(3, fruits.length);
        assertEquals("苹果", fruits[0]);
    }

    @Test
    void testAutoTypeConversion() {
        int intValue = 100;
        long longValue = intValue;
        float floatValue = longValue;
        double doubleValue = floatValue;

        assertEquals(100L, longValue);
        assertEquals(100.0F, floatValue, 0.001);
        assertEquals(100.0, doubleValue, 0.001);
    }

    @Test
    void testExplicitTypeConversion() {
        double doubleValue = 99.99;
        int convertedInt = (int) doubleValue;

        assertEquals(99, convertedInt);
    }

    @Test
    void testStringNumberConversion() {
        String numberStr = "123";
        int parsedInt = Integer.parseInt(numberStr);
        assertEquals(123, parsedInt);

        int age = 25;
        String ageStr = String.valueOf(age);
        assertEquals("25", ageStr);
    }

    @Test
    void testConstants() {
        final double PI = 3.14159;
        final String COMPANY_NAME = "OpenDemo";

        assertEquals(3.14159, PI, 0.00001);
        assertEquals("OpenDemo", COMPANY_NAME);
    }

    @Test
    void testByteRange() {
        byte minByte = Byte.MIN_VALUE;
        byte maxByte = Byte.MAX_VALUE;

        assertEquals(-128, minByte);
        assertEquals(127, maxByte);
    }

    @Test
    void testShortRange() {
        assertEquals(-32768, Short.MIN_VALUE);
        assertEquals(32767, Short.MAX_VALUE);
    }

    @Test
    void testIntegerRange() {
        assertEquals(-2147483648, Integer.MIN_VALUE);
        assertEquals(2147483647, Integer.MAX_VALUE);
    }

    @Test
    void testDoubleNaNAndInfinity() {
        double nan = Double.NaN;
        double positiveInfinity = Double.POSITIVE_INFINITY;
        double negativeInfinity = Double.NEGATIVE_INFINITY;

        assertTrue(Double.isNaN(nan));
        assertTrue(Double.isInfinite(positiveInfinity));
        assertTrue(Double.isInfinite(negativeInfinity));
    }

    @Test
    void testStringMethods() {
        String str = "Hello, Java!";

        assertTrue(str.startsWith("Hello"));
        assertTrue(str.endsWith("Java!"));
        assertEquals("Hello", str.substring(0, 5));
        assertEquals("hello, java!", str.toLowerCase());
        assertEquals(1, str.indexOf(','));
        assertEquals(7, str.indexOf("Java"));
    }

    @Test
    void testStringBuilder() {
        StringBuilder sb = new StringBuilder();
        sb.append("Hello");
        sb.append(" ");
        sb.append("World");

        assertEquals("Hello World", sb.toString());

        sb.insert(5, " Beautiful");
        assertEquals("Hello Beautiful World", sb.toString());

        sb.delete(5, 15);
        assertEquals("Hello World", sb.toString());
    }
}
