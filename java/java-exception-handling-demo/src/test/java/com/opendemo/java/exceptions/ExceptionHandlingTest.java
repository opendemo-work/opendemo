package com.opendemo.java.exceptions;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

class ExceptionHandlingTest {
    private BankAccount account;

    @BeforeEach
    void setUp() {
        account = new BankAccount("123456", 1000.0);
    }

    @Test
    void depositIncreasesBalance() throws BankOperationException {
        account.deposit(500.0);
        assertEquals(1500.0, account.getBalance(), 0.001);
    }

    @Test
    void depositNegativeAmountThrowsInvalidAmount() {
        assertThrows(InvalidAmountException.class, () -> account.deposit(-100.0));
    }

    @Test
    void depositZeroThrowsInvalidAmount() {
        assertThrows(InvalidAmountException.class, () -> account.deposit(0.0));
    }

    @Test
    void withdrawDecreasesBalance() throws BankOperationException {
        account.withdraw(300.0);
        assertEquals(700.0, account.getBalance(), 0.001);
    }

    @Test
    void withdrawMoreThanBalanceThrowsInsufficientFunds() {
        InsufficientFundsException ex = assertThrows(InsufficientFundsException.class,
                () -> account.withdraw(2000.0));
        assertEquals(1000.0, ex.getCurrentBalance(), 0.001);
        assertEquals(2000.0, ex.getWithdrawAmount(), 0.001);
    }

    @Test
    void withdrawNegativeAmountThrowsInvalidAmount() {
        assertThrows(InvalidAmountException.class, () -> account.withdraw(-50.0));
    }

    @Test
    void frozenAccountCannotDeposit() throws BankOperationException {
        account.freezeAccount();
        assertTrue(account.isFrozen());
        assertThrows(AccountFrozenException.class, () -> account.deposit(100.0));
    }

    @Test
    void frozenAccountCannotWithdraw() {
        account.freezeAccount();
        assertThrows(AccountFrozenException.class, () -> account.withdraw(100.0));
    }

    @Test
    void unfreezeRestoresOperations() throws BankOperationException {
        account.freezeAccount();
        account.unfreezeAccount();
        assertFalse(account.isFrozen());
        account.deposit(100.0);
        assertEquals(1100.0, account.getBalance(), 0.001);
    }

    @Test
    void tryCatchFinallyExecutesFinally() {
        StringBuilder sb = new StringBuilder();
        try {
            int x = 10 / 0;
        } catch (ArithmeticException e) {
            sb.append("catch");
        } finally {
            sb.append("finally");
        }
        assertEquals("catchfinally", sb.toString());
    }

    @Test
    void multiCatchHandlesMultipleTypes() {
        Exception caught = null;
        try {
            Object o = "string";
            Integer i = (Integer) o;
        } catch (ClassCastException | NullPointerException e) {
            caught = e;
        }
        assertNotNull(caught);
        assertTrue(caught instanceof ClassCastException);
    }

    @Test
    void chainedExceptionPreservesCause() {
        DataProcessingException ex = assertThrows(DataProcessingException.class, () -> {
            try {
                throw new FileReadException("file not found");
            } catch (FileReadException e) {
                throw new DataProcessingException("processing failed", e);
            }
        });
        assertNotNull(ex.getCause());
        assertTrue(ex.getCause() instanceof FileReadException);
        assertEquals("file not found", ex.getCause().getMessage());
    }

    @Test
    void tryWithResourcesAutoCloses() {
        boolean[] closed = {false};
        AutoCloseable resource = () -> closed[0] = true;
        try (AutoCloseable r = resource) {
            // use resource
        } catch (Exception e) {
            fail("Should not throw");
        }
        assertTrue(closed[0]);
    }

    @Test
    void assertUsage() {
        int value = 42;
        assert value > 0 : "value should be positive";
    }

    @Test
    void throwKeywordCreatesException() {
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> {
            throw new IllegalArgumentException("test message");
        });
        assertEquals("test message", ex.getMessage());
    }

    @Test
    void accountNumberIsCorrect() {
        assertEquals("123456", account.getAccountNumber());
    }
}
