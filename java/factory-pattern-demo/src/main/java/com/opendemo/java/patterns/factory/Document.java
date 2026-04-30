package com.opendemo.java.patterns.factory;

public interface Document {
    void open();
    void save();
    void close();
    String getType();
}
