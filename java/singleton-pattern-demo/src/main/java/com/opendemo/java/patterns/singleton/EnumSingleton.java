package com.opendemo.java.patterns.singleton;

public enum EnumSingleton {

    INSTANCE;

    private int counter = 0;

    public int increment() {
        return ++counter;
    }

    public int getCounter() {
        return counter;
    }

    public String getInfo() {
        return "EnumSingleton instance: " + this.hashCode();
    }
}
