package com.opendemo.java.exceptions;

public class AccountFrozenException extends BankOperationException {
    public AccountFrozenException() {
        super("账户已被冻结，无法进行操作");
    }
}
