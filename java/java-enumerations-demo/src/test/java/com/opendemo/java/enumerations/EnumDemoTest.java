package com.opendemo.java.enumerations;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class EnumDemoTest {

    @Test
    void testColorValues() {
        assertEquals(6, Color.values().length);
        assertEquals("红色", Color.RED.getName());
        assertEquals("#FF0000", Color.RED.getHexCode());
    }

    @Test
    void testColorIsPrimary() {
        assertTrue(Color.RED.isPrimary());
        assertTrue(Color.GREEN.isPrimary());
        assertTrue(Color.BLUE.isPrimary());
        assertFalse(Color.YELLOW.isPrimary());
        assertFalse(Color.BLACK.isPrimary());
    }

    @Test
    void testColorFromName() {
        assertEquals(Color.RED, Color.fromName("红色"));
        assertEquals(Color.BLUE, Color.fromName("蓝色"));
    }

    @Test
    void testColorFromNameInvalid() {
        assertThrows(IllegalArgumentException.class, () -> Color.fromName("紫色"));
    }

    @Test
    void testColorFromHexCode() {
        assertEquals(Color.GREEN, Color.fromHexCode("#00FF00"));
        assertEquals(Color.GREEN, Color.fromHexCode("#00ff00"));
    }

    @Test
    void testColorFromHexCodeInvalid() {
        assertThrows(IllegalArgumentException.class, () -> Color.fromHexCode("#123456"));
    }

    @Test
    void testColorToString() {
        assertTrue(Color.RED.toString().contains("红色"));
        assertTrue(Color.RED.toString().contains("#FF0000"));
    }

    @Test
    void testMathOperationAdd() {
        assertEquals(5.0, MathOperation.ADD.apply(2, 3), 0.001);
    }

    @Test
    void testMathOperationSubtract() {
        assertEquals(7.0, MathOperation.SUBTRACT.apply(10, 3), 0.001);
    }

    @Test
    void testMathOperationMultiply() {
        assertEquals(30.0, MathOperation.MULTIPLY.apply(10, 3), 0.001);
    }

    @Test
    void testMathOperationDivide() {
        assertEquals(3.333, MathOperation.DIVIDE.apply(10, 3), 0.01);
    }

    @Test
    void testMathOperationDivideByZero() {
        assertThrows(ArithmeticException.class, () -> MathOperation.DIVIDE.apply(10, 0));
    }

    @Test
    void testMathOperationSymbol() {
        assertEquals("+", MathOperation.ADD.getSymbol());
        assertEquals("-", MathOperation.SUBTRACT.getSymbol());
        assertEquals("*", MathOperation.MULTIPLY.getSymbol());
        assertEquals("/", MathOperation.DIVIDE.getSymbol());
    }

    @Test
    void testMathOperationFromSymbol() {
        assertEquals(MathOperation.ADD, MathOperation.fromSymbol("+"));
        assertThrows(IllegalArgumentException.class, () -> MathOperation.fromSymbol("%"));
    }

    @Test
    void testHttpStatusSuccess() {
        assertTrue(HttpStatus.OK.isSuccess());
        assertTrue(HttpStatus.CREATED.isSuccess());
        assertFalse(HttpStatus.BAD_REQUEST.isSuccess());
    }

    @Test
    void testHttpStatusClientError() {
        assertTrue(HttpStatus.BAD_REQUEST.isClientError());
        assertTrue(HttpStatus.UNAUTHORIZED.isClientError());
        assertTrue(HttpStatus.FORBIDDEN.isClientError());
        assertTrue(HttpStatus.NOT_FOUND.isClientError());
        assertFalse(HttpStatus.OK.isClientError());
    }

    @Test
    void testHttpStatusServerError() {
        assertTrue(HttpStatus.INTERNAL_SERVER_ERROR.isServerError());
        assertTrue(HttpStatus.BAD_GATEWAY.isServerError());
        assertTrue(HttpStatus.SERVICE_UNAVAILABLE.isServerError());
        assertFalse(HttpStatus.NOT_FOUND.isServerError());
    }

    @Test
    void testHttpStatusFromCode() {
        assertEquals(HttpStatus.OK, HttpStatus.fromCode(200));
        assertEquals(HttpStatus.NOT_FOUND, HttpStatus.fromCode(404));
        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, HttpStatus.fromCode(500));
    }

    @Test
    void testHttpStatusFromCodeInvalid() {
        assertThrows(IllegalArgumentException.class, () -> HttpStatus.fromCode(999));
    }

    @Test
    void testHttpStatusToString() {
        assertTrue(HttpStatus.OK.toString().contains("200"));
        assertTrue(HttpStatus.OK.toString().contains("OK"));
    }

    @Test
    void testSwitchStatement() {
        EnumDemo demo = new EnumDemo();
        assertEquals("选择了绿色", demo.demonstrateSwitchStatement());
    }

    @Test
    void testRunAll() {
        EnumDemo demo = new EnumDemo();
        assertDoesNotThrow(() -> demo.runAll());
    }

    @Test
    void testMathOperationImplementsInterface() {
        Operation add = MathOperation.ADD;
        assertEquals(8.0, add.apply(5, 3), 0.001);
    }
}
