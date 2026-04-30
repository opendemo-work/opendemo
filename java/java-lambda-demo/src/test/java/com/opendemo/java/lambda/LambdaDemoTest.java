package com.opendemo.java.lambda;

import org.junit.jupiter.api.Test;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

class LambdaDemoTest {

    @Test
    void testBasicLambda() {
        LambdaDemo demo = new LambdaDemo();
        assertEquals("HELLO", demo.demonstrateBasicLambda());
    }

    @Test
    void testMethodReference() {
        LambdaDemo demo = new LambdaDemo();
        assertEquals("WORLD", demo.demonstrateMethodReference());
    }

    @Test
    void testCustomFunctionalInterface() {
        FunctionalInterfaceDemo demo = new FunctionalInterfaceDemo();
        assertEquals("HELLO WORLD", demo.demonstrateCustomFunctionalInterface());
    }

    @Test
    void testPredicate() {
        FunctionalInterfaceDemo demo = new FunctionalInterfaceDemo();
        assertTrue(demo.demonstratePredicate());
    }

    @Test
    void testFunction() {
        FunctionalInterfaceDemo demo = new FunctionalInterfaceDemo();
        assertEquals(11, demo.demonstrateFunction());
    }

    @Test
    void testSupplier() {
        FunctionalInterfaceDemo demo = new FunctionalInterfaceDemo();
        assertEquals("Hello from Supplier", demo.demonstrateSupplier());
    }

    @Test
    void testBiFunction() {
        FunctionalInterfaceDemo demo = new FunctionalInterfaceDemo();
        assertEquals(10, demo.demonstrateBiFunction());
    }

    @Test
    void testStringProcessor() {
        StringProcessor reverse = s -> new StringBuilder(s).reverse().toString();
        assertEquals("olleH", reverse.process("Hello"));
        assertEquals("null", reverse.processWithDefault(null));
        assertEquals("olleH", reverse.processWithDefault("Hello"));
    }

    @Test
    void testStreamFilter() {
        StreamApiDemo demo = new StreamApiDemo();
        List<String> result = demo.demonstrateFilter();
        assertTrue(result.contains("Alice"));
        assertTrue(result.contains("Charlie"));
        assertTrue(result.contains("David"));
        assertFalse(result.contains("Bob"));
    }

    @Test
    void testStreamMap() {
        StreamApiDemo demo = new StreamApiDemo();
        List<String> result = demo.demonstrateMap();
        assertEquals(List.of("ALICE", "BOB", "CHARLIE"), result);
    }

    @Test
    void testStreamReduce() {
        StreamApiDemo demo = new StreamApiDemo();
        assertEquals("Hello World!", demo.demonstrateReduce());
    }

    @Test
    void testStreamSorted() {
        StreamApiDemo demo = new StreamApiDemo();
        List<String> result = demo.demonstrateSorted();
        assertEquals("Alice", result.get(0));
        assertEquals("David", result.get(result.size() - 1));
    }

    @Test
    void testStreamCount() {
        StreamApiDemo demo = new StreamApiDemo();
        assertEquals(5, demo.demonstrateCount());
    }

    @Test
    void testStreamMatch() {
        StreamApiDemo demo = new StreamApiDemo();
        assertTrue(demo.demonstrateMatch());
    }

    @Test
    void testStreamFlatMap() {
        StreamApiDemo demo = new StreamApiDemo();
        List<Integer> result = demo.demonstrateFlatMap();
        assertEquals(9, result.size());
        assertEquals(1, result.get(0));
        assertEquals(9, result.get(8));
    }

    @Test
    void testStreamFindFirst() {
        StreamApiDemo demo = new StreamApiDemo();
        assertEquals(4, demo.demonstrateFindFirst());
    }

    @Test
    void testStreamDistinct() {
        StreamApiDemo demo = new StreamApiDemo();
        List<Integer> result = demo.demonstrateDistinct();
        assertEquals(List.of(1, 2, 3, 4), result);
    }

    @Test
    void testStreamSum() {
        StreamApiDemo demo = new StreamApiDemo();
        assertEquals(15, demo.demonstrateSum());
    }

    @Test
    void testRunAll() {
        LambdaDemo demo = new LambdaDemo();
        assertDoesNotThrow(() -> demo.runAll());
    }
}
