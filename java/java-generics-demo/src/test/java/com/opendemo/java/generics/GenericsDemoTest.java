package com.opendemo.java.generics;

import org.junit.jupiter.api.Test;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

class GenericsDemoTest {

    @Test
    void testGenericBox() {
        GenericBox<String> box = new GenericBox<>("hello");
        assertEquals("hello", box.get());
        assertEquals("String", box.getType());
        assertFalse(box.isEmpty());
    }

    @Test
    void testGenericBoxEmpty() {
        GenericBox<String> box = new GenericBox<>();
        assertNull(box.get());
        assertTrue(box.isEmpty());
        assertEquals("null", box.getType());
    }

    @Test
    void testGenericBoxInteger() {
        GenericBox<Integer> box = new GenericBox<>(42);
        assertEquals(42, box.get());
        box.set(100);
        assertEquals(100, box.get());
    }

    @Test
    void testGenericBoxToString() {
        GenericBox<String> box = new GenericBox<>("test");
        assertTrue(box.toString().contains("test"));
    }

    @Test
    void testGetMiddle() {
        Integer[] ints = {1, 2, 3, 4, 5};
        assertEquals(3, GenericMethodDemo.getMiddle(ints));
        String[] strs = {"a", "b", "c"};
        assertEquals("b", GenericMethodDemo.getMiddle(strs));
    }

    @Test
    void testGetMiddleEmpty() {
        assertNull(GenericMethodDemo.getMiddle(new Integer[0]));
        assertNull(GenericMethodDemo.getMiddle(null));
    }

    @Test
    void testFindMax() {
        Integer[] ints = {3, 7, 1, 9, 5};
        assertEquals(9, GenericMethodDemo.findMax(ints));
        String[] strs = {"apple", "banana", "cherry"};
        assertEquals("cherry", GenericMethodDemo.findMax(strs));
    }

    @Test
    void testFindMin() {
        Integer[] ints = {3, 7, 1, 9, 5};
        assertEquals(1, GenericMethodDemo.findMin(ints));
    }

    @Test
    void testFromArrayToList() {
        Integer[] array = {1, 2, 3};
        List<Integer> list = GenericMethodDemo.fromArrayToList(array);
        assertEquals(3, list.size());
        assertTrue(list.contains(1));
    }

    @Test
    void testFormatPair() {
        String result = GenericMethodDemo.formatPair("key", 42);
        assertEquals("(key, 42)", result);
    }

    @Test
    void testSwap() {
        Integer[] array = {1, 2, 3};
        GenericMethodDemo.swap(array, 0, 2);
        assertArrayEquals(new Integer[]{3, 2, 1}, array);
    }

    @Test
    void testSwapInvalidIndex() {
        assertThrows(IllegalArgumentException.class, () -> {
            GenericMethodDemo.swap(new Integer[]{1}, -1, 0);
        });
    }

    @Test
    void testBoundedNumberBox() {
        BoundedTypeDemo.NumberBox<Integer> intBox = new BoundedTypeDemo.NumberBox<>(10);
        assertEquals(10, intBox.getValue());
        assertEquals(10.0, intBox.doubleValue(), 0.001);
    }

    @Test
    void testBoundedNumberBoxComparison() {
        BoundedTypeDemo.NumberBox<Integer> box1 = new BoundedTypeDemo.NumberBox<>(10);
        BoundedTypeDemo.NumberBox<Integer> box2 = new BoundedTypeDemo.NumberBox<>(20);
        assertFalse(box1.isGreaterThan(box2));
        assertTrue(box2.isGreaterThan(box1));
    }

    @Test
    void testCountGreaterThan() {
        Integer[] array = {1, 5, 3, 8, 2};
        assertEquals(2, BoundedTypeDemo.countGreaterThan(array, 4));
    }

    @Test
    void testSumOfList() {
        List<Integer> list = Arrays.asList(1, 2, 3, 4, 5);
        assertEquals(15.0, BoundedTypeDemo.sumOfList(list), 0.001);
    }

    @Test
    void testAddNumbers() {
        List<Number> list = new ArrayList<>();
        BoundedTypeDemo.addNumbers(list, 10, 20, 30);
        assertEquals(3, list.size());
    }

    @Test
    void testWildcardSumList() {
        assertEquals(6.0, WildcardDemo.sumList(Arrays.asList(1, 2, 3)), 0.001);
        assertEquals(6.6, WildcardDemo.sumList(Arrays.asList(1.1, 2.2, 3.3)), 0.001);
    }

    @Test
    void testWildcardCopyList() {
        List<Integer> source = Arrays.asList(1, 2, 3);
        List<Object> dest = new ArrayList<>();
        WildcardDemo.copyList(source, dest);
        assertEquals(3, dest.size());
        assertEquals(1, dest.get(0));
    }

    @Test
    void testWildcardContainsNull() {
        List<String> list1 = Arrays.asList("a", "b");
        assertFalse(WildcardDemo.containsNull(list1));
    }

    @Test
    void testRunAll() {
        GenericsDemo demo = new GenericsDemo();
        assertDoesNotThrow(() -> demo.runAll());
    }
}
