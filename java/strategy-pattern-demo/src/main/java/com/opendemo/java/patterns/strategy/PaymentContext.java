package com.opendemo.java.patterns.strategy;

public class PaymentContext {

    private PaymentStrategy paymentStrategy;

    public void setPaymentStrategy(PaymentStrategy paymentStrategy) {
        this.paymentStrategy = paymentStrategy;
    }

    public PaymentStrategy getPaymentStrategy() {
        return paymentStrategy;
    }

    public boolean executePayment(double amount) {
        if (paymentStrategy == null) {
            System.out.println("No payment strategy selected!");
            return false;
        }
        System.out.println("Using strategy: " + paymentStrategy.getName());
        return paymentStrategy.pay(amount);
    }
}
