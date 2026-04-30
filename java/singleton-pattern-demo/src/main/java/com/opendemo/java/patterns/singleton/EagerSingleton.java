package com.opendemo.java.patterns.singleton;

public class EagerSingleton {

    private static final EagerSingleton instance = new EagerSingleton();

    private EagerSingleton() {
    }

    public static EagerSingleton getInstance() {
        return instance;
    }

    public String getInfo() {
        return "EagerSingleton instance: " + this.hashCode();
    }
}
