package com.opendemo.java.refactoring.before;

public class ReplaceMagicNumberBefore {
    public double calculateShipping(double weight, String destination) {
        double cost = 0;
        if (destination.equals("DOMESTIC")) {
            if (weight <= 1.0) {
                cost = 5.99;
            } else if (weight <= 5.0) {
                cost = 9.99;
            } else {
                cost = 15.99;
            }
        } else if (destination.equals("INTERNATIONAL")) {
            if (weight <= 1.0) {
                cost = 15.99;
            } else if (weight <= 5.0) {
                cost = 29.99;
            } else {
                cost = 49.99;
            }
        }
        if (weight > 10.0) {
            cost = cost * 1.5;
        }
        return cost;
    }

    public boolean isFreeShippingEligible(double orderTotal) {
        return orderTotal >= 35.00;
    }
}
