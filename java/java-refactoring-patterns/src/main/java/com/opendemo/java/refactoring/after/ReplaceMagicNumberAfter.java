package com.opendemo.java.refactoring.after;

public class ReplaceMagicNumberAfter {
    private static final double DOMESTIC_LIGHT_RATE = 5.99;
    private static final double DOMESTIC_MEDIUM_RATE = 9.99;
    private static final double DOMESTIC_HEAVY_RATE = 15.99;
    private static final double INTERNATIONAL_LIGHT_RATE = 15.99;
    private static final double INTERNATIONAL_MEDIUM_RATE = 29.99;
    private static final double INTERNATIONAL_HEAVY_RATE = 49.99;
    private static final double LIGHT_WEIGHT_LIMIT = 1.0;
    private static final double MEDIUM_WEIGHT_LIMIT = 5.0;
    private static final double OVERSIZE_WEIGHT_LIMIT = 10.0;
    private static final double OVERSIZE_SURCHARGE = 1.5;
    private static final double FREE_SHIPPING_THRESHOLD = 35.00;

    public double calculateShipping(double weight, String destination) {
        double cost;
        if (destination.equals("DOMESTIC")) {
            cost = getDomesticRate(weight);
        } else {
            cost = getInternationalRate(weight);
        }
        if (weight > OVERSIZE_WEIGHT_LIMIT) {
            cost *= OVERSIZE_SURCHARGE;
        }
        return cost;
    }

    private double getDomesticRate(double weight) {
        if (weight <= LIGHT_WEIGHT_LIMIT) return DOMESTIC_LIGHT_RATE;
        if (weight <= MEDIUM_WEIGHT_LIMIT) return DOMESTIC_MEDIUM_RATE;
        return DOMESTIC_HEAVY_RATE;
    }

    private double getInternationalRate(double weight) {
        if (weight <= LIGHT_WEIGHT_LIMIT) return INTERNATIONAL_LIGHT_RATE;
        if (weight <= MEDIUM_WEIGHT_LIMIT) return INTERNATIONAL_MEDIUM_RATE;
        return INTERNATIONAL_HEAVY_RATE;
    }

    public boolean isFreeShippingEligible(double orderTotal) {
        return orderTotal >= FREE_SHIPPING_THRESHOLD;
    }
}
