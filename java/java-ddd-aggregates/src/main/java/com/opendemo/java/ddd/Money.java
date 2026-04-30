package com.opendemo.java.ddd;

import java.math.BigDecimal;
import java.util.Objects;

public class Money extends ValueObject {
    public static final Money ZERO = new Money(BigDecimal.ZERO);

    private final BigDecimal amount;

    public Money(BigDecimal amount) {
        this.amount = amount;
    }

    public Money(double amount) {
        this.amount = BigDecimal.valueOf(amount);
    }

    public Money add(Money other) {
        return new Money(this.amount.add(other.amount));
    }

    public Money subtract(Money other) {
        return new Money(this.amount.subtract(other.amount));
    }

    public Money multiply(int factor) {
        return new Money(this.amount.multiply(BigDecimal.valueOf(factor)));
    }

    public boolean isGreaterThan(Money other) {
        return this.amount.compareTo(other.amount) > 0;
    }

    public boolean isLessThanOrEqual(Money other) {
        return this.amount.compareTo(other.amount) <= 0;
    }

    public BigDecimal getAmount() {
        return amount;
    }

    @Override
    protected Object[] getEqualityComponents() {
        return new Object[]{amount};
    }

    @Override
    public String toString() {
        return "$" + amount;
    }
}
