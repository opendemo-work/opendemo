package com.opendemo.java.tdd;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.NullAndEmptySource;
import org.junit.jupiter.params.provider.ValueSource;
import static org.junit.jupiter.api.Assertions.*;

class StringUtilsTest {
    @Nested
    @DisplayName("isEmpty")
    class IsEmptyTests {
        @Test
        void nullReturnsTrue() {
            assertTrue(StringUtils.isEmpty(null));
        }

        @Test
        void emptyStringReturnsTrue() {
            assertTrue(StringUtils.isEmpty(""));
        }

        @Test
        void nonEmptyReturnsFalse() {
            assertFalse(StringUtils.isEmpty("hello"));
        }

        @Test
        void whitespaceReturnsFalse() {
            assertFalse(StringUtils.isEmpty(" "));
        }
    }

    @Nested
    @DisplayName("isBlank")
    class IsBlankTests {
        @Test
        void nullReturnsTrue() {
            assertTrue(StringUtils.isBlank(null));
        }

        @Test
        void emptyReturnsTrue() {
            assertTrue(StringUtils.isBlank(""));
        }

        @ParameterizedTest
        @ValueSource(strings = {" ", "  ", "\t", "\n"})
        void whitespaceReturnsTrue(String input) {
            assertTrue(StringUtils.isBlank(input));
        }

        @Test
        void nonBlankReturnsFalse() {
            assertFalse(StringUtils.isBlank("hello"));
        }
    }

    @Nested
    @DisplayName("reverse")
    class ReverseTests {
        @Test
        void nullReturnsNull() {
            assertNull(StringUtils.reverse(null));
        }

        @Test
        void emptyReturnsEmpty() {
            assertEquals("", StringUtils.reverse(""));
        }

        @ParameterizedTest
        @CsvSource({"abc, cba", "hello, olleh", "a, a", "ab, ba"})
        void reversesCorrectly(String input, String expected) {
            assertEquals(expected, StringUtils.reverse(input));
        }
    }

    @Nested
    @DisplayName("capitalize")
    class CapitalizeTests {
        @Test
        void nullReturnsNull() {
            assertNull(StringUtils.capitalize(null));
        }

        @Test
        void emptyReturnsEmpty() {
            assertEquals("", StringUtils.capitalize(""));
        }

        @Test
        void capitalizesFirstLetter() {
            assertEquals("Hello", StringUtils.capitalize("hello"));
        }

        @Test
        void alreadyCapitalized() {
            assertEquals("Hello", StringUtils.capitalize("Hello"));
        }

        @Test
        void singleChar() {
            assertEquals("H", StringUtils.capitalize("h"));
        }
    }

    @Nested
    @DisplayName("countOccurrences")
    class CountOccurrencesTests {
        @Test
        void nullStringReturnsZero() {
            assertEquals(0, StringUtils.countOccurrences(null, "a"));
        }

        @Test
        void nullSubstringReturnsZero() {
            assertEquals(0, StringUtils.countOccurrences("abc", null));
        }

        @Test
        void emptySubstringReturnsZero() {
            assertEquals(0, StringUtils.countOccurrences("abc", ""));
        }

        @ParameterizedTest
        @CsvSource({"hello, l, 2", "aaa, a, 3", "abc, x, 0", "ababab, ab, 3"})
        void countsCorrectly(String str, String sub, int expected) {
            assertEquals(expected, StringUtils.countOccurrences(str, sub));
        }
    }

    @Nested
    @DisplayName("isPalindrome")
    class IsPalindromeTests {
        @Test
        void nullReturnsFalse() {
            assertFalse(StringUtils.isPalindrome(null));
        }

        @Test
        void emptyReturnsTrue() {
            assertTrue(StringUtils.isPalindrome(""));
        }

        @ParameterizedTest
        @ValueSource(strings = {"racecar", "level", "madam", "A man a plan a canal Panama"})
        void validPalindromes(String input) {
            assertTrue(StringUtils.isPalindrome(input));
        }

        @ParameterizedTest
        @ValueSource(strings = {"hello", "world", "java"})
        void invalidPalindromes(String input) {
            assertFalse(StringUtils.isPalindrome(input));
        }
    }

    @Nested
    @DisplayName("truncate")
    class TruncateTests {
        @Test
        void nullReturnsNull() {
            assertNull(StringUtils.truncate(null, 5));
        }

        @Test
        void shortStringUnchanged() {
            assertEquals("hi", StringUtils.truncate("hi", 10));
        }

        @Test
        void exactLengthUnchanged() {
            assertEquals("hello", StringUtils.truncate("hello", 5));
        }

        @Test
        void truncatesWithEllipsis() {
            assertEquals("hel...", StringUtils.truncate("hello world", 3));
        }

        @Test
        void zeroLength() {
            assertEquals("...", StringUtils.truncate("hello", 0));
        }

        @Test
        void negativeLengthThrows() {
            assertThrows(IllegalArgumentException.class, () -> StringUtils.truncate("hello", -1));
        }
    }
}
