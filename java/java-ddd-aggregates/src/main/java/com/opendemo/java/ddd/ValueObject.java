package com.opendemo.java.ddd;

import java.util.Objects;

public abstract class ValueObject {
    protected abstract Object[] getEqualityComponents();

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        ValueObject that = (ValueObject) o;
        return Objects.deepEquals(this.getEqualityComponents(), that.getEqualityComponents());
    }

    @Override
    public int hashCode() {
        return Objects.hash(getEqualityComponents());
    }
}
