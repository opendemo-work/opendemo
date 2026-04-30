package com.opendemo.java.tdd;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import static org.junit.jupiter.api.Assertions.*;

class FizzBuzzTest {
    private FizzBuzz fizzBuzz;

    @BeforeEach
    void setUp() {
        fizzBuzz = new FizzBuzz();
    }

    @Test
    @DisplayName("Regular numbers return themselves")
    void regularNumbers() {
        assertEquals("1", fizzBuzz.convert(1));
        assertEquals("2", fizzBuzz.convert(2));
        assertEquals("7", fizzBuzz.convert(7));
    }

    @Test
    @DisplayName("Multiples of 3 return Fizz")
    void multiplesOfThree() {
        assertEquals("Fizz", fizzBuzz.convert(3));
        assertEquals("Fizz", fizzBuzz.convert(6));
        assertEquals("Fizz", fizzBuzz.convert(9));
    }

    @Test
    @DisplayName("Multiples of 5 return Buzz")
    void multiplesOfFive() {
        assertEquals("Buzz", fizzBuzz.convert(5));
        assertEquals("Buzz", fizzBuzz.convert(10));
        assertEquals("Buzz", fizzBuzz.convert(20));
    }

    @Test
    @DisplayName("Multiples of 15 return FizzBuzz")
    void multiplesOfFifteen() {
        assertEquals("FizzBuzz", fizzBuzz.convert(15));
        assertEquals("FizzBuzz", fizzBuzz.convert(30));
        assertEquals("FizzBuzz", fizzBuzz.convert(45));
    }

    @ParameterizedTest
    @ValueSource(ints = {0, -1, -100})
    @DisplayName("Non-positive numbers throw exception")
    void nonPositiveThrows(int number) {
        assertThrows(IllegalArgumentException.class, () -> fizzBuzz.convert(number));
    }

    @Nested
    @DisplayName("First 15 numbers sequence")
    class First15Numbers {
        @Test
        void verifySequence() {
            String[] expected = {"1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz",
                    "11", "Fizz", "13", "14", "FizzBuzz"};
            for (int i = 0; i < 15; i++) {
                assertEquals(expected[i], fizzBuzz.convert(i + 1),
                        "Failed at position " + (i + 1));
            }
        }
    }
}
