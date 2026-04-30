package com.opendemo.java.patterns.templatemethod;

public class XmlDataProcessor extends DataProcessor {

    @Override
    protected String validate(String data) {
        System.out.println("XmlDataProcessor: Validating XML format...");
        if (data == null || !data.trim().startsWith("<") || !data.trim().endsWith(">")) {
            throw new IllegalArgumentException("Invalid XML data");
        }
        return data;
    }

    @Override
    protected String transform(String data) {
        System.out.println("XmlDataProcessor: Transforming XML data...");
        return data.replace("<", "&lt;").replace(">", "&gt;");
    }

    @Override
    protected void save(String data) {
        System.out.println("XmlDataProcessor: Saving to XML file: " + data);
    }
}
