package com.opendemo.java.arrayscollections;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import java.util.stream.Collectors;

class ArraysCollectionsDemoTest {

    @Test
    void testArrayDeclaration() {
        int[] numbers1 = new int[5];
        numbers1[0] = 10;
        assertEquals(10, numbers1[0]);
        assertEquals(0, numbers1[4]);

        int[] numbers2 = {1, 2, 3, 4, 5};
        assertEquals(5, numbers2.length);
        assertEquals(3, numbers2[2]);

        int[] numbers3 = new int[]{100, 200, 300};
        assertEquals(3, numbers3.length);
        assertEquals(200, numbers3[1]);
    }

    @Test
    void testArrayCopy() {
        int[] original = {1, 2, 3, 4, 5};
        int[] copied = Arrays.copyOf(original, original.length);
        assertArrayEquals(original, copied);
        assertNotSame(original, copied);

        int[] expanded = Arrays.copyOf(original, 8);
        assertEquals(8, expanded.length);
        assertEquals(0, expanded[5]);
    }

    @Test
    void testArrayFill() {
        int[] filled = new int[5];
        Arrays.fill(filled, 99);
        for (int val : filled) {
            assertEquals(99, val);
        }
    }

    @Test
    void testArraySort() {
        int[] numbers = {5, 2, 8, 1, 9, 3};
        Arrays.sort(numbers);
        assertArrayEquals(new int[]{1, 2, 3, 5, 8, 9}, numbers);
    }

    @Test
    void testBinarySearch() {
        int[] numbers = {1, 2, 3, 5, 8, 9};
        int index = Arrays.binarySearch(numbers, 5);
        assertEquals(3, index);

        int notFound = Arrays.binarySearch(numbers, 4);
        assertTrue(notFound < 0);
    }

    @Test
    void testArrayEquals() {
        int[] a = {1, 2, 3};
        int[] b = {1, 2, 3};
        int[] c = {1, 2, 4};

        assertFalse(a.equals(b));
        assertTrue(Arrays.equals(a, b));
        assertFalse(Arrays.equals(a, c));
    }

    @Test
    void testTwoDimensionalArray() {
        int[][] matrix = {
                {1, 2, 3},
                {4, 5, 6},
                {7, 8, 9}
        };
        assertEquals(3, matrix.length);
        assertEquals(3, matrix[0].length);
        assertEquals(5, matrix[1][1]);

        int[][] irregular = new int[3][];
        irregular[0] = new int[]{1, 2, 3};
        irregular[1] = new int[]{4, 5};
        irregular[2] = new int[]{6, 7, 8, 9};
        assertEquals(3, irregular[0].length);
        assertEquals(2, irregular[1].length);
        assertEquals(4, irregular[2].length);
    }

    @Test
    void testArrayList() {
        List<String> list = new ArrayList<>();
        list.add("苹果");
        list.add("香蕉");
        list.add("橙子");

        assertEquals(3, list.size());
        assertEquals("香蕉", list.get(1));
        assertTrue(list.contains("苹果"));

        list.remove("香蕉");
        assertEquals(2, list.size());

        list.set(0, "红苹果");
        assertEquals("红苹果", list.get(0));
    }

    @Test
    void testLinkedList() {
        List<Integer> linkedList = new LinkedList<>();
        linkedList.add(10);
        linkedList.add(20);
        linkedList.add(30);
        assertEquals(3, linkedList.size());
        assertEquals(20, linkedList.get(1));
    }

    @Test
    void testHashSet() {
        Set<String> set = new HashSet<>();
        set.add("Java");
        set.add("Python");
        set.add("Java");
        assertEquals(2, set.size());
        assertTrue(set.contains("Java"));
        assertTrue(set.contains("Python"));
    }

    @Test
    void testLinkedHashSetOrder() {
        Set<String> set = new LinkedHashSet<>();
        set.add("第一");
        set.add("第二");
        set.add("第三");
        List<String> ordered = new ArrayList<>(set);
        assertEquals("第一", ordered.get(0));
        assertEquals("第二", ordered.get(1));
        assertEquals("第三", ordered.get(2));
    }

    @Test
    void testTreeSetOrder() {
        Set<Integer> set = new TreeSet<>();
        set.add(5);
        set.add(2);
        set.add(8);
        set.add(1);
        List<Integer> sorted = new ArrayList<>(set);
        assertEquals(List.of(1, 2, 5, 8), sorted);
    }

    @Test
    void testTreeSetReverseOrder() {
        Set<String> set = new TreeSet<>(Comparator.reverseOrder());
        set.add("apple");
        set.add("banana");
        set.add("cherry");
        List<String> sorted = new ArrayList<>(set);
        assertEquals("cherry", sorted.get(0));
    }

    @Test
    void testHashMap() {
        Map<String, Integer> map = new HashMap<>();
        map.put("苹果", 5);
        map.put("香蕉", 3);
        map.put("苹果", 10);

        assertEquals(2, map.size());
        assertEquals(10, map.get("苹果"));
        assertNull(map.get("橙子"));
    }

    @Test
    void testLinkedHashMapOrder() {
        Map<String, String> map = new LinkedHashMap<>();
        map.put("first", "1");
        map.put("second", "2");
        map.put("third", "3");
        List<String> keys = new ArrayList<>(map.keySet());
        assertEquals(List.of("first", "second", "third"), keys);
    }

    @Test
    void testTreeMapOrder() {
        Map<Integer, String> map = new TreeMap<>();
        map.put(3, "三");
        map.put(1, "一");
        map.put(2, "二");
        List<Integer> keys = new ArrayList<>(map.keySet());
        assertEquals(List.of(1, 2, 3), keys);
    }

    @Test
    void testMapEntrySet() {
        Map<String, Integer> map = new HashMap<>();
        map.put("a", 1);
        map.put("b", 2);
        int sum = 0;
        for (Map.Entry<String, Integer> entry : map.entrySet()) {
            sum += entry.getValue();
        }
        assertEquals(3, sum);
    }

    @Test
    void testCollectionsSort() {
        List<Integer> numbers = new ArrayList<>(Arrays.asList(5, 2, 8, 1, 9, 3));
        Collections.sort(numbers);
        assertEquals(List.of(1, 2, 3, 5, 8, 9), numbers);
    }

    @Test
    void testCollectionsReverse() {
        List<Integer> numbers = new ArrayList<>(Arrays.asList(1, 2, 3, 4, 5));
        Collections.reverse(numbers);
        assertEquals(List.of(5, 4, 3, 2, 1), numbers);
    }

    @Test
    void testCollectionsMinMax() {
        List<Integer> numbers = Arrays.asList(5, 2, 8, 1, 9, 3);
        assertEquals(9, Collections.max(numbers));
        assertEquals(1, Collections.min(numbers));
    }

    @Test
    void testArrayToListConversion() {
        String[] colors = {"红色", "绿色", "蓝色"};
        List<String> fixedList = Arrays.asList(colors);
        assertEquals(3, fixedList.size());

        List<String> mutableList = new ArrayList<>(Arrays.asList(colors));
        mutableList.add("黄色");
        assertEquals(4, mutableList.size());
    }

    @Test
    void testListToArrayConversion() {
        List<String> list = new ArrayList<>(Arrays.asList("a", "b", "c"));
        String[] array = list.toArray(new String[0]);
        assertArrayEquals(new String[]{"a", "b", "c"}, array);
    }

    @Test
    void testDeduplication() {
        List<Integer> withDuplicates = Arrays.asList(1, 2, 3, 2, 4, 1, 5, 3);
        Set<Integer> unique = new LinkedHashSet<>(withDuplicates);
        List<Integer> deduplicated = new ArrayList<>(unique);
        assertEquals(List.of(1, 2, 3, 4, 5), deduplicated);
    }

    @Test
    void testFrequencyCount() {
        List<String> words = Arrays.asList("apple", "banana", "apple", "orange", "banana", "apple");
        Map<String, Long> wordCount = words.stream()
                .collect(Collectors.groupingBy(w -> w, Collectors.counting()));
        assertEquals(3L, wordCount.get("apple"));
        assertEquals(2L, wordCount.get("banana"));
        assertEquals(1L, wordCount.get("orange"));
    }

    @Test
    void testBubbleSort() {
        int[] arr = {64, 34, 25, 12, 22, 11, 90};
        int[] expected = {11, 12, 22, 25, 34, 64, 90};
        bubbleSort(arr);
        assertArrayEquals(expected, arr);
    }

    private void bubbleSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }
}
