package com.opendemo.java.patterns.strategy;

public class AlipayPayment implements PaymentStrategy {

    private final String accountId;

    public AlipayPayment(String accountId) {
        this.accountId = accountId;
    }

    @Override
    public boolean pay(double amount) {
        System.out.println("Paying ¥" + amount + " with Alipay (Account: " + accountId + ")");
        return true;
    }

    @Override
    public String getName() {
        return "Alipay";
    }
}
