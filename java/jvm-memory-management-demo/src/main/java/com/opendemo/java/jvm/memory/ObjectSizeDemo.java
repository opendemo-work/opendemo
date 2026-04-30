package com.opendemo.java.jvm.memory;

import java.lang.instrument.Instrumentation;
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

public class ObjectSizeDemo {

    private static final int OBJECT_HEADER_SIZE = is64Bit() ? 16 : 8;
    private static final int REFERENCE_SIZE = is64Bit() ? 8 : 4;
    private static final int ALIGNMENT = 8;

    public static void main(String[] args) {
        estimatePrimitiveSizes();
        estimateObjectSizes();
        estimateCollectionSizes();
        demonstrateCompressedOops();
        compareMemoryFootprint();
    }

    public static void estimatePrimitiveSizes() {
        System.out.println("=== 基本类型大小 ===");
        System.out.println("boolean: 1 byte");
        System.out.println("byte:    1 byte");
        System.out.println("short:   2 bytes");
        System.out.println("char:    2 bytes");
        System.out.println("int:     4 bytes");
        System.out.println("float:   4 bytes");
        System.out.println("long:    8 bytes");
        System.out.println("double:  8 bytes");
        System.out.println("引用类型: " + REFERENCE_SIZE + " bytes (64位JVM" +
                (is64Bit() ? "" : " (32位)") + ")");
        System.out.println();
    }

    public static void estimateObjectSizes() {
        System.out.println("=== 对象大小估算 ===");

        System.out.printf("空对象 (Object): %d bytes%n", estimateSize(0));
        System.out.printf("含1个int字段: %d bytes%n", estimateSize(4));
        System.out.printf("含1个long字段: %d bytes%n", estimateSize(8));
        System.out.printf("含1个引用字段: %d bytes%n", estimateSize(REFERENCE_SIZE));
        System.out.printf("含2个int + 1个引用: %d bytes%n", estimateSize(8 + REFERENCE_SIZE));
        System.out.println();

        SimpleObject obj = new SimpleObject();
        System.out.printf("SimpleObject (2个int, 1个String引用) 估算: ~%d bytes%n",
                estimateSimpleObjectSize());
        System.out.printf("SimpleObject 含字符串 'Hello' 估算: ~%d bytes%n",
                estimateSimpleObjectSize() + estimateStringSize("Hello"));
        System.out.println();

        ArrayObject arr = new ArrayObject();
        System.out.printf("ArrayObject 估算: ~%d bytes (不含数组内容)%n",
                estimateArrayObjectSize());
    }

    public static void estimateCollectionSizes() {
        System.out.println("=== 集合大小估算 ===");

        List<String> arrayList = new ArrayList<>();
        List<String> linkedList = new LinkedList<>();
        Map<String, Integer> hashMap = new HashMap<>();

        System.out.printf("空 ArrayList: ~%d bytes%n", estimateCollectionOverhead(arrayList));
        System.out.printf("空 LinkedList: ~%d bytes%n", estimateCollectionOverhead(linkedList));
        System.out.printf("空 HashMap: ~%d bytes%n", estimateCollectionOverhead(hashMap));
        System.out.println();

        for (int i = 0; i < 100; i++) {
            String val = "item-" + i;
            arrayList.add(val);
            linkedList.add(val);
            hashMap.put(val, i);
        }

        System.out.printf("100元素的 ArrayList: ~%d bytes (不含元素)%n",
                16 + 100 * REFERENCE_SIZE + 16);
        System.out.printf("100元素的 LinkedList: ~%d bytes (不含元素)%n",
                16 + 100 * (16 + REFERENCE_SIZE * 2));
        System.out.printf("100元素的 HashMap: ~%d bytes (不含键值)%n",
                16 + 128 * (16 + REFERENCE_SIZE * 3) + 16);
        System.out.println();
    }

    public static void demonstrateCompressedOops() {
        System.out.println("=== 压缩指针 (Compressed Oops) ===");
        System.out.println("32位JVM: 引用4字节, 最大堆~4GB");
        System.out.println("64位JVM: 引用8字节, 无压缩时对象更大");
        System.out.println("64位JVM + CompressedOops (-XX:+UseCompressedOops):");
        System.out.println("  引用4字节, 堆<32GB时默认开启");
        System.out.println();

        int withCompressed = 16 + 4 * 3;
        int withoutCompressed = 16 + 8 * 3;
        System.out.printf("含3个引用字段的对象:%n");
        System.out.printf("  压缩指针开启: %d bytes%n", alignUp(withCompressed));
        System.out.printf("  压缩指针关闭: %d bytes%n", alignUp(withoutCompressed));
        System.out.printf("  节省: %d bytes (%.0f%%)%n",
                withoutCompressed - withCompressed,
                (1 - (double) withCompressed / withoutCompressed) * 100);
    }

    public static void compareMemoryFootprint() {
        System.out.println();
        System.out.println("=== 内存占用对比 ===");

        int count = 1_000_000;

        long primitiveArray = (long) count * 4;
        long integerList = (long) count * (16 + 4 + 16 + 8);
        long boxedArray = (long) count * (16 + 4);

        System.out.printf("100万个int原始数组: ~%d MB%n", primitiveArray / (1024 * 1024));
        System.out.printf("100万个Integer的ArrayList: ~%d MB%n", integerList / (1024 * 1024));
        System.out.printf("100万个Integer数组: ~%d MB%n", boxedArray / (1024 * 1024));
        System.out.printf("装箱开销: ~%.1fx%n", (double) integerList / primitiveArray);
    }

    private static int estimateSize(int fieldBytes) {
        return alignUp(OBJECT_HEADER_SIZE + fieldBytes);
    }

    private static int estimateSimpleObjectSize() {
        return alignUp(OBJECT_HEADER_SIZE + 4 + 4 + REFERENCE_SIZE);
    }

    private static int estimateStringSize(String s) {
        return alignUp(OBJECT_HEADER_SIZE + 4 + 4 + REFERENCE_SIZE) +
                alignUp(OBJECT_HEADER_SIZE + 8 + 2 * s.length());
    }

    private static int estimateArrayObjectSize() {
        return alignUp(OBJECT_HEADER_SIZE + REFERENCE_SIZE + 4);
    }

    private static int estimateCollectionOverhead(Object collection) {
        return alignUp(OBJECT_HEADER_SIZE + REFERENCE_SIZE * 4 + 4 * 3);
    }

    private static int alignUp(int size) {
        return (size + ALIGNMENT - 1) / ALIGNMENT * ALIGNMENT;
    }

    private static boolean is64Bit() {
        return "64".equals(System.getProperty("sun.arch.data.model", "32"));
    }

    static class SimpleObject {
        int field1 = 42;
        int field2 = 100;
        String name = "test";
    }

    static class ArrayObject {
        int[] data = new int[100];
        int size = 0;
    }
}
