package com.opendemo.java.ddd;

import java.util.Objects;

public class ProductId extends ValueObject {
    private final String value;

    public ProductId(String value) {
        this.value = Objects.requireNonNull(value, "ProductId cannot be null");
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
