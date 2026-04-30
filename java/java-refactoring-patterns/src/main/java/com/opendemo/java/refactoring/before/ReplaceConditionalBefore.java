package com.opendemo.java.refactoring.before;

public class ReplaceConditionalBefore {
    public double calculatePrice(String type, double amount) {
        if (type.equals("NORMAL")) {
            return amount * 1.0;
        } else if (type.equals("VIP")) {
            return amount * 0.8;
        } else if (type.equals("STAFF")) {
            return amount * 0.5;
        } else if (type.equals("PREMIUM")) {
            return amount * 0.7;
        }
        return amount;
    }

    public String getLabel(String type) {
        if (type.equals("NORMAL")) {
            return "Regular Customer";
        } else if (type.equals("VIP")) {
            return "VIP Customer";
        } else if (type.equals("STAFF")) {
            return "Staff Member";
        } else if (type.equals("PREMIUM")) {
            return "Premium Member";
        }
        return "Unknown";
    }
}
