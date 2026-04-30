package com.opendemo.java.patterns.decorator;

public interface Notifier {
    void send(String message);
    String getChannel();
}
