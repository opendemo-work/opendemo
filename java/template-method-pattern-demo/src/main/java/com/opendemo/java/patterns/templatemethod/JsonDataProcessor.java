package com.opendemo.java.patterns.templatemethod;

public class JsonDataProcessor extends DataProcessor {

    @Override
    protected String validate(String data) {
        System.out.println("JsonDataProcessor: Validating JSON format...");
        if (data == null || !data.trim().startsWith("{") || !data.trim().endsWith("}")) {
            throw new IllegalArgumentException("Invalid JSON data");
        }
        return data;
    }

    @Override
    protected String transform(String data) {
        System.out.println("JsonDataProcessor: Transforming JSON data...");
        return data.replace("{", "[JSON_START]").replace("}", "[JSON_END]");
    }

    @Override
    protected void save(String data) {
        System.out.println("JsonDataProcessor: Saving to JSON file: " + data);
    }
}
