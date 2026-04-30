package com.opendemo.java.jvm.memory;

public class StackDemo {

    private static int counter = 0;

    public static void main(String[] args) {
        demonstrateStackFrames();
        demonstrateStackOverflow();
        demonstrateTailRecursion();
    }

    public static void demonstrateStackFrames() {
        System.out.println("=== 栈帧结构演示 ===");
        System.out.println("每个方法调用创建一个栈帧，包含:");
        System.out.println("  1. 局部变量表 (Local Variable Table)");
        System.out.println("  2. 操作数栈 (Operand Stack)");
        System.out.println("  3. 动态链接 (Dynamic Linking)");
        System.out.println("  4. 方法返回地址 (Return Address)");
        System.out.println();

        methodA();
    }

    private static void methodA() {
        int a = 10;
        String message = "Hello from A";
        System.out.printf("  methodA: a=%d, message=%s%n", a, message);
        methodB(a);
    }

    private static void methodB(int value) {
        double b = value * 3.14;
        System.out.printf("    methodB: value=%d, b=%.2f%n", value, b);
        methodC(b);
    }

    private static void methodC(double value) {
        long c = (long) value * 100;
        System.out.printf("      methodC: value=%.2f, c=%d%n", value, c);
        System.out.println("      methodC 返回 -> methodB -> methodA -> main");
        System.out.println();
    }

    public static void demonstrateStackOverflow() {
        System.out.println("=== 栈溢出演示 ===");

        try {
            recursiveMethod(1);
        } catch (StackOverflowError e) {
            System.out.printf("栈溢出! 递归深度: %d%n", counter);
            System.out.println("StackOverflowError: " + e.getMessage());
            System.out.println("可通过 -Xss 参数增大栈大小（默认约512KB-1MB）");
        }
        System.out.println();
    }

    private static void recursiveMethod(int depth) {
        counter = depth;
        long localData1 = depth;
        double localData2 = depth * Math.PI;
        String localData3 = "frame-" + depth;

        if (depth % 1000 == 0) {
            System.out.printf("  递归深度: %d%n", depth);
        }

        recursiveMethod(depth + 1);
    }

    public static void demonstrateTailRecursion() {
        System.out.println("=== 避免栈溢出的方法 ===");
        System.out.println("1. 使用迭代替代递归:");
        long iterativeResult = factorialIterative(20);
        System.out.printf("   迭代方式计算 20! = %d%n", iterativeResult);

        System.out.println("2. 增大栈大小: -Xss4m");
        System.out.println("3. 使用尾递归优化（Java不直接支持，需手动转为迭代）");
        System.out.println("4. 使用堆内存替代栈内存（如用List保存中间结果）");

        System.out.println();
        System.out.println("栈大小参数:");
        System.out.println("  -Xss256k  (256KB)");
        System.out.println("  -Xss512k  (512KB, 64位JVM默认)");
        System.out.println("  -Xss1m    (1MB)");
    }

    private static long factorialIterative(int n) {
        long result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }
}
