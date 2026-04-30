package com.opendemo.java.tdd;

import java.util.ArrayList;
import java.util.EmptyStackException;
import java.util.List;

public class BoundedStack<T> {
    private final List<T> elements;
    private final int capacity;

    public BoundedStack(int capacity) {
        if (capacity <= 0) {
            throw new IllegalArgumentException("Capacity must be positive");
        }
        this.capacity = capacity;
        this.elements = new ArrayList<>(capacity);
    }

    public void push(T item) {
        if (elements.size() >= capacity) {
            throw new IllegalStateException("Stack is full");
        }
        elements.add(item);
    }

    public T pop() {
        if (elements.isEmpty()) {
            throw new EmptyStackException();
        }
        return elements.remove(elements.size() - 1);
    }

    public T peek() {
        if (elements.isEmpty()) {
            throw new EmptyStackException();
        }
        return elements.get(elements.size() - 1);
    }

    public boolean isEmpty() {
        return elements.isEmpty();
    }

    public int size() {
        return elements.size();
    }

    public int getCapacity() {
        return capacity;
    }

    public void clear() {
        elements.clear();
    }
}
