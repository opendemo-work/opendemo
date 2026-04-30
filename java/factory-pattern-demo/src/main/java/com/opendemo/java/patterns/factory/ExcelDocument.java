package com.opendemo.java.patterns.factory;

public class ExcelDocument implements Document {

    @Override
    public void open() {
        System.out.println("Opening Excel spreadsheet with Microsoft Excel...");
    }

    @Override
    public void save() {
        System.out.println("Saving Excel spreadsheet (.xlsx)...");
    }

    @Override
    public void close() {
        System.out.println("Closing Excel spreadsheet...");
    }

    @Override
    public String getType() {
        return "EXCEL";
    }
}
