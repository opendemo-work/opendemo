package com.opendemo.java.refactoring.after;

public interface PricingStrategy {
    double calculatePrice(double amount);
    String getLabel();
}

class NormalPricing implements PricingStrategy {
    @Override
    public double calculatePrice(double amount) {
        return amount;
    }

    @Override
    public String getLabel() {
        return "Regular Customer";
    }
}

class VipPricing implements PricingStrategy {
    @Override
    public double calculatePrice(double amount) {
        return amount * 0.8;
    }

    @Override
    public String getLabel() {
        return "VIP Customer";
    }
}

class StaffPricing implements PricingStrategy {
    @Override
    public double calculatePrice(double amount) {
        return amount * 0.5;
    }

    @Override
    public String getLabel() {
        return "Staff Member";
    }
}

class PremiumPricing implements PricingStrategy {
    @Override
    public double calculatePrice(double amount) {
        return amount * 0.7;
    }

    @Override
    public String getLabel() {
        return "Premium Member";
    }
}
