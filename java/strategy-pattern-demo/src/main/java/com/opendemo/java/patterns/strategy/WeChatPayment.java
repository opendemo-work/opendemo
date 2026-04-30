package com.opendemo.java.patterns.strategy;

public class WeChatPayment implements PaymentStrategy {

    private final String openId;

    public WeChatPayment(String openId) {
        this.openId = openId;
    }

    @Override
    public boolean pay(double amount) {
        System.out.println("Paying ¥" + amount + " with WeChat Pay (OpenID: " + openId + ")");
        return true;
    }

    @Override
    public String getName() {
        return "WeChat Pay";
    }
}
