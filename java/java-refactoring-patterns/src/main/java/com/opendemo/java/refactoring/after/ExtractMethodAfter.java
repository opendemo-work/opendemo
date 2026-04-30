package com.opendemo.java.refactoring.after;

import com.opendemo.java.refactoring.before.ExtractMethodBefore.Order;

import java.util.List;

public class ExtractMethodAfter {
    private String name;
    private List<Order> orders;

    public ExtractMethodAfter(String name, List<Order> orders) {
        this.name = name;
        this.orders = orders;
    }

    public void printOwing() {
        printBanner();
        double outstanding = calculateOutstanding();
        printDetails(outstanding);
    }

    private void printBanner() {
        System.out.println("**************************");
        System.out.println("***** Customer Owes ******");
        System.out.println("**************************");
    }

    private double calculateOutstanding() {
        return orders.stream()
                .mapToDouble(Order::getAmount)
                .sum();
    }

    private void printDetails(double outstanding) {
        System.out.println("name: " + name);
        System.out.println("amount: " + outstanding);
    }
}
