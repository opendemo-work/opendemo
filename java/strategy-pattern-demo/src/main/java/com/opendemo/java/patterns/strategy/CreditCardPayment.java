package com.opendemo.java.patterns.strategy;

public class CreditCardPayment implements PaymentStrategy {

    private final String cardNumber;
    private final String cardHolder;
    private final String expiryDate;

    public CreditCardPayment(String cardNumber, String cardHolder, String expiryDate) {
        this.cardNumber = cardNumber;
        this.cardHolder = cardHolder;
        this.expiryDate = expiryDate;
    }

    @Override
    public boolean pay(double amount) {
        System.out.println("Paying ¥" + amount + " with Credit Card (****"
                + cardNumber.substring(cardNumber.length() - 4) + ")");
        return true;
    }

    @Override
    public String getName() {
        return "Credit Card";
    }
}
