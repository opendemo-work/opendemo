package com.opendemo.java.exceptions;

public class InvalidAmountException extends BankOperationException {
    private final double amount;

    public InvalidAmountException(double amount) {
        super("无效的金额: $" + amount);
        this.amount = amount;
    }

    public double getAmount() {
        return amount;
    }
}
