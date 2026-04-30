package com.opendemo.java.patterns.templatemethod;

public class CsvDataProcessor extends DataProcessor {

    @Override
    protected String validate(String data) {
        System.out.println("CsvDataProcessor: Validating CSV format...");
        if (data == null || data.trim().isEmpty()) {
            throw new IllegalArgumentException("CSV data is empty");
        }
        return data;
    }

    @Override
    protected String transform(String data) {
        System.out.println("CsvDataProcessor: Transforming CSV data...");
        return data.replace(",", " | ");
    }

    @Override
    protected void save(String data) {
        System.out.println("CsvDataProcessor: Saving to CSV file: " + data);
    }
}
