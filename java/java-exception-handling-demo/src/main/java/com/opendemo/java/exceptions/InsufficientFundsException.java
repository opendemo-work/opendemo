package com.opendemo.java.exceptions;

public class InsufficientFundsException extends BankOperationException {
    private final double currentBalance;
    private final double withdrawAmount;

    public InsufficientFundsException(double currentBalance, double withdrawAmount) {
        super(String.format("余额不足。当前余额: $%.2f, 尝试取款: $%.2f", currentBalance, withdrawAmount));
        this.currentBalance = currentBalance;
        this.withdrawAmount = withdrawAmount;
    }

    public double getCurrentBalance() {
        return currentBalance;
    }

    public double getWithdrawAmount() {
        return withdrawAmount;
    }
}
