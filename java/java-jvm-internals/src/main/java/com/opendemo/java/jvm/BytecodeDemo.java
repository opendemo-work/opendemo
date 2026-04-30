package com.opendemo.java.jvm;

public class BytecodeDemo {
    public static void main(String[] args) {
        System.out.println("=== Bytecode Demo ===\n");
        demonstrateSimpleMethod();
        demonstrateLoop();
        demonstrateExceptionTable();
    }

    static void demonstrateSimpleMethod() {
        System.out.println("1. Simple Method Bytecode Concepts:");
        System.out.println("  Source: int add(int a, int b) { return a + b; }");
        System.out.println("  Bytecode concept:");
        System.out.println("    iload_1    // load a");
        System.out.println("    iload_2    // load b");
        System.out.println("    iadd       // add");
        System.out.println("    ireturn    // return result");
        System.out.println();

        int a = 10, b = 20;
        int result = a + b;
        System.out.println("  Result: " + result);
        System.out.println();
    }

    static void demonstrateLoop() {
        System.out.println("2. Loop Bytecode Concepts:");
        System.out.println("  Source: for (int i=0; i<10; i++) { sum += i; }");
        System.out.println("  Bytecode uses goto instructions for looping");
        System.out.println();

        int sum = 0;
        for (int i = 0; i < 10; i++) {
            sum += i;
        }
        System.out.println("  Loop result (1+2+...+9): " + sum);
        System.out.println();
    }

    static void demonstrateExceptionTable() {
        System.out.println("3. Exception Table Concept:");
        System.out.println("  try-catch generates an exception table in bytecode:");
        System.out.println("  | from | to | target | type |");
        System.out.println("  | 0    | 4  | 5      | ArithmeticException |");
        System.out.println();

        try {
            int x = 10 / 0;
        } catch (ArithmeticException e) {
            System.out.println("  Caught: " + e.getMessage());
        } finally {
            System.out.println("  finally block (compiled as subroutine or duplicated code)");
        }
        System.out.println();

        System.out.println("4. Class File Version Info:");
        String version = System.getProperty("java.class.version");
        String vmVersion = System.getProperty("java.vm.version");
        String specVersion = System.getProperty("java.specification.version");
        System.out.println("  Class file version: " + version);
        System.out.println("  VM version: " + vmVersion);
        System.out.println("  Specification version: " + specVersion);
        System.out.println();
    }
}
