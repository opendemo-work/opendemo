package com.opendemo.java.generics;

public class GenericContainer<T> {
    private T data;
    
    public void setData(T data) {
        this.data = data;
    }
    
    public T getData() {
        return data;
    }
    
    public <U> void display(U item) {
        System.out.println("泛型方法: " + item);
    }
}