package com.opendemo.java.exceptions;

public class BankAccount {
    private final String accountNumber;
    private double balance;
    private boolean frozen;

    public BankAccount(String accountNumber, double initialBalance) {
        this.accountNumber = accountNumber;
        this.balance = initialBalance;
        this.frozen = false;
    }

    public void deposit(double amount) throws InvalidAmountException, AccountFrozenException {
        if (amount <= 0) {
            throw new InvalidAmountException(amount);
        }
        if (frozen) {
            throw new AccountFrozenException();
        }
        balance += amount;
    }

    public void withdraw(double amount) throws InsufficientFundsException, InvalidAmountException, AccountFrozenException {
        if (amount <= 0) {
            throw new InvalidAmountException(amount);
        }
        if (frozen) {
            throw new AccountFrozenException();
        }
        if (amount > balance) {
            throw new InsufficientFundsException(balance, amount);
        }
        balance -= amount;
    }

    public void freezeAccount() {
        this.frozen = true;
    }

    public void unfreezeAccount() {
        this.frozen = false;
    }

    public double getBalance() {
        return balance;
    }

    public String getAccountNumber() {
        return accountNumber;
    }

    public boolean isFrozen() {
        return frozen;
    }
}
