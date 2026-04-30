package com.opendemo.java.refactoring.before;

import java.util.List;

public class ExtractMethodBefore {
    private String name;
    private List<Order> orders;

    public ExtractMethodBefore(String name, List<Order> orders) {
        this.name = name;
        this.orders = orders;
    }

    public void printOwing() {
        double outstanding = 0.0;

        System.out.println("**************************");
        System.out.println("***** Customer Owes ******");
        System.out.println("**************************");

        for (Order order : orders) {
            outstanding += order.getAmount();
        }

        System.out.println("name: " + name);
        System.out.println("amount: " + outstanding);
    }

    public static class Order {
        private double amount;
        public Order(double amount) { this.amount = amount; }
        public double getAmount() { return amount; }
    }
}
