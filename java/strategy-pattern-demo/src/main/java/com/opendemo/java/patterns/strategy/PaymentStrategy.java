package com.opendemo.java.patterns.strategy;

public interface PaymentStrategy {
    boolean pay(double amount);
    String getName();
}
