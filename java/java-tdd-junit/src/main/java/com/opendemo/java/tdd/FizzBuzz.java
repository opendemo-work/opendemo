package com.opendemo.java.tdd;

public class FizzBuzz {
    public String convert(int number) {
        if (number <= 0) {
            throw new IllegalArgumentException("Number must be positive");
        }
        if (number % 15 == 0) {
            return "FizzBuzz";
        }
        if (number % 3 == 0) {
            return "Fizz";
        }
        if (number % 5 == 0) {
            return "Buzz";
        }
        return String.valueOf(number);
    }
}
