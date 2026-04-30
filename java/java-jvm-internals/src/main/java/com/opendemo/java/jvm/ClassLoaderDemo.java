package com.opendemo.java.jvm;

public class ClassLoaderDemo {
    public static void main(String[] args) {
        System.out.println("=== ClassLoader Demo ===\n");
        demonstrateClassLoaderHierarchy();
        demonstrateClassLoading();
        demonstrateClassLoaderNames();
    }

    static void demonstrateClassLoaderHierarchy() {
        System.out.println("1. ClassLoader Hierarchy:");
        ClassLoader contextLoader = Thread.currentThread().getContextClassLoader();
        ClassLoader current = contextLoader;
        int level = 0;
        while (current != null) {
            System.out.printf("  Level %d: %s%n", level++, current.getClass().getName());
            current = current.getParent();
        }
        System.out.printf("  Level %d: null (Bootstrap ClassLoader)%n", level);
        System.out.println();
    }

    static void demonstrateClassLoading() {
        System.out.println("2. Class Loading Info:");
        Class<String> stringClass = String.class;
        ClassLoader loader = stringClass.getClassLoader();
        System.out.println("  String class loader: " + (loader == null ? "Bootstrap ClassLoader" : loader));

        Class<ClassLoaderDemo> thisClass = ClassLoaderDemo.class;
        System.out.println("  ClassLoaderDemo loaded by: " + thisClass.getClassLoader());
        System.out.println();

        System.out.println("  Loaded class details:");
        System.out.println("  Name: " + stringClass.getName());
        System.out.println("  Simple Name: " + stringClass.getSimpleName());
        System.out.println("  Package: " + stringClass.getPackage());
        System.out.println("  Is Interface: " + stringClass.isInterface());
        System.out.println("  Is Array: " + stringClass.isArray());
        System.out.println();
    }

    static void demonstrateClassLoaderNames() {
        System.out.println("3. Core ClassLoader Names:");
        System.out.println("  Bootstrap: loads rt.jar (core Java classes)");
        System.out.println("  Extension/Platform: loads JDK extensions");
        System.out.println("  Application/System: loads application classpath");
        System.out.println();

        String bootPath = System.getProperty("sun.boot.class.path");
        if (bootPath != null) {
            System.out.println("  Bootstrap classpath: " + bootPath);
        }
        String extPath = System.getProperty("java.ext.dirs");
        if (extPath != null) {
            System.out.println("  Extension dirs: " + extPath);
        }
        String classPath = System.getProperty("java.class.path");
        System.out.println("  Application classpath: " + classPath);
        System.out.println();
    }
}
