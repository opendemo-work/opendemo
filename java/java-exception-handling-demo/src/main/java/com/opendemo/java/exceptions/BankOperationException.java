package com.opendemo.java.exceptions;

public class BankOperationException extends Exception {
    public BankOperationException(String message) {
        super(message);
    }

    public BankOperationException(String message, Throwable cause) {
        super(message, cause);
    }
}
