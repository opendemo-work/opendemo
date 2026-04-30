package com.opendemo.java.jvm.gc;

import java.lang.ref.PhantomReference;
import java.lang.ref.Reference;
import java.lang.ref.ReferenceQueue;
import java.lang.ref.SoftReference;
import java.lang.ref.WeakReference;
import java.util.HashMap;
import java.util.Map;
import java.util.WeakHashMap;

public class WeakReferenceDemo {

    public static void main(String[] args) throws InterruptedException {
        demonstrateWeakReference();
        demonstrateSoftReference();
        demonstratePhantomReference();
        demonstrateWeakHashMap();
        demonstrateReferenceUsage();
    }

    public static void demonstrateWeakReference() {
        System.out.println("=== WeakReference 弱引用 ===");

        Object strongRef = new Object();
        WeakReference<Object> weakRef = new WeakReference<>(strongRef);

        System.out.printf("GC前 - 强引用: %s%n", strongRef != null ? "存在" : "null");
        System.out.printf("GC前 - 弱引用获取: %s%n", weakRef.get() != null ? "存在" : "null");

        strongRef = null;
        System.gc();
        try { Thread.sleep(100); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

        System.out.printf("GC后 - 弱引用获取: %s%n", weakRef.get() != null ? "存在" : "null");
        System.out.println("弱引用在GC时会被回收（无论内存是否充足）");
        System.out.println("适用场景: 缓存、Listener列表、WeakHashMap");
        System.out.println();
    }

    public static void demonstrateSoftReference() {
        System.out.println("=== SoftReference 软引用 ===");

        byte[] data = new byte[10 * 1024 * 1024];
        SoftReference<byte[]> softRef = new SoftReference<>(data);

        System.out.printf("GC前 - 软引用获取: %s%n", softRef.get() != null ? "存在" : "null");

        data = null;
        System.gc();
        try { Thread.sleep(100); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

        System.out.printf("内存充足时GC后 - 软引用获取: %s%n", softRef.get() != null ? "存在" : "null");
        System.out.println("软引用只在内存不足时才会被回收");
        System.out.println("适用场景: 内存敏感的缓存");
        System.out.println();
    }

    public static void demonstratePhantomReference() throws InterruptedException {
        System.out.println("=== PhantomReference 虚引用 ===");

        ReferenceQueue<Object> refQueue = new ReferenceQueue<>();
        Object obj = new Object();
        PhantomReference<Object> phantomRef = new PhantomReference<>(obj, refQueue);

        System.out.printf("虚引用get()始终返回: %s%n", phantomRef.get());
        System.out.println("虚引用无法通过get()获取对象引用");

        obj = null;
        System.gc();
        Thread.sleep(200);

        Reference<?> ref = refQueue.poll();
        System.out.printf("对象被回收后，引用队列中: %s%n", ref != null ? "存在" : "不存在");

        if (ref != null) {
            System.out.println("虚引用被加入引用队列，可以执行清理操作");
        }
        System.out.println();
        System.out.println("适用场景:");
        System.out.println("  1. 替代finalize()进行资源清理");
        System.out.println("  2. 监控对象何时被回收");
        System.out.println("  3. java.lang.ref.Cleaner的底层实现");
        System.out.println();
    }

    public static void demonstrateWeakHashMap() {
        System.out.println("=== WeakHashMap ===");

        WeakHashMap<Object, String> weakMap = new WeakHashMap<>();
        Object key1 = new Object();
        Object key2 = new Object();

        weakMap.put(key1, "value1");
        weakMap.put(key2, "value2");

        System.out.printf("GC前 WeakHashMap大小: %d%n", weakMap.size());

        key1 = null;
        System.gc();
        try { Thread.sleep(100); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

        System.out.printf("释放key1并GC后 WeakHashMap大小: %d%n", weakMap.size());
        System.out.println("WeakHashMap的key被GC时，条目自动移除");
        System.out.println();
    }

    public static void demonstrateReferenceUsage() {
        System.out.println("=== 引用类型对比 ===");

        System.out.println("┌──────────┬──────────────┬──────────────┬──────────────┐");
        System.out.println("│ 类型     │ GC行为       │ get()结果    │ 典型用途     │");
        System.out.println("├──────────┼──────────────┼──────────────┼──────────────┤");
        System.out.println("│ Strong   │ 不回收       │ 始终可用     │ 普通引用     │");
        System.out.println("│ Soft     │ 内存不足回收 │ GC后可能null │ 缓存         │");
        System.out.println("│ Weak     │ 下次GC回收   │ GC后可能null │ Map/缓存     │");
        System.out.println("│ Phantom  │ 回收后通知   │ 始终null     │ 资源清理     │");
        System.out.println("└──────────┴──────────────┴──────────────┴──────────────┘");
        System.out.println();

        System.out.println("引用队列 (ReferenceQueue) 使用场景:");
        System.out.println("  1. 监控引用何时被回收");
        System.out.println("  2. 执行相关清理操作");
        System.out.println("  3. 构建自定义缓存失效机制");
    }
}
