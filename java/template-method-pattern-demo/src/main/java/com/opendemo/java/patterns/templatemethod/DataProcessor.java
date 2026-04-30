package com.opendemo.java.patterns.templatemethod;

public abstract class DataProcessor {

    public final void process(String data) {
        System.out.println("=== Starting data processing ===");
        String validated = validate(data);
        System.out.println("Validation completed.");
        String transformed = transform(validated);
        System.out.println("Transformation completed.");
        save(transformed);
        System.out.println("Save completed.");
        System.out.println("=== Data processing finished ===");
    }

    protected abstract String validate(String data);

    protected abstract String transform(String data);

    protected abstract void save(String data);

    protected boolean shouldLog() {
        return true;
    }
}
