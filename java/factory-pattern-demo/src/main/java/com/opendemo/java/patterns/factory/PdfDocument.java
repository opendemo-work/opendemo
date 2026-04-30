package com.opendemo.java.patterns.factory;

public class PdfDocument implements Document {

    @Override
    public void open() {
        System.out.println("Opening PDF document with Adobe Reader...");
    }

    @Override
    public void save() {
        System.out.println("Saving PDF document...");
    }

    @Override
    public void close() {
        System.out.println("Closing PDF document...");
    }

    @Override
    public String getType() {
        return "PDF";
    }
}
