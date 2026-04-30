package com.opendemo.java.patterns.singleton;

public class LazySingleton {

    private static LazySingleton instance;

    private LazySingleton() {
    }

    public static LazySingleton getInstance() {
        if (instance == null) {
            instance = new LazySingleton();
        }
        return instance;
    }

    public String getInfo() {
        return "LazySingleton instance: " + this.hashCode();
    }
}
