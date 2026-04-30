package com.opendemo.java.lambda;

@FunctionalInterface
public interface StringProcessor {
    String process(String input);

    default String processWithDefault(String input) {
        if (input == null) {
            return "null";
        }
        return process(input);
    }
}
