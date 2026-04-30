package com.opendemo.java.patterns.factory;

public class WordDocument implements Document {

    @Override
    public void open() {
        System.out.println("Opening Word document with Microsoft Word...");
    }

    @Override
    public void save() {
        System.out.println("Saving Word document (.docx)...");
    }

    @Override
    public void close() {
        System.out.println("Closing Word document...");
    }

    @Override
    public String getType() {
        return "WORD";
    }
}
