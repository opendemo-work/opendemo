package com.opendemo.java.ddd;

import java.util.Objects;

public class OrderId extends ValueObject {
    private final String value;

    public OrderId(String value) {
        this.value = Objects.requireNonNull(value, "OrderId cannot be null");
    }

    public String getValue() {
        return value;
    }

    @Override
    protected Object[] getEqualityComponents() {
        return new Object[]{value};
    }

    @Override
    public String toString() {
        return value;
    }
}
