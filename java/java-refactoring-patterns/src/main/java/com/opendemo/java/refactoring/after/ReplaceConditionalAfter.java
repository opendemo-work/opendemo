package com.opendemo.java.refactoring.after;

import java.util.HashMap;
import java.util.Map;

public class ReplaceConditionalAfter {
    private final Map<String, PricingStrategy> strategies = new HashMap<>();

    public ReplaceConditionalAfter() {
        strategies.put("NORMAL", new NormalPricing());
        strategies.put("VIP", new VipPricing());
        strategies.put("STAFF", new StaffPricing());
        strategies.put("PREMIUM", new PremiumPricing());
    }

    public double calculatePrice(String type, double amount) {
        PricingStrategy strategy = strategies.getOrDefault(type, new NormalPricing());
        return strategy.calculatePrice(amount);
    }

    public String getLabel(String type) {
        PricingStrategy strategy = strategies.getOrDefault(type, new NormalPricing());
        return strategy.getLabel();
    }
}
