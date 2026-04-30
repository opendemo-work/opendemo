package com.opendemo.java.tdd;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.EmptyStackException;

class BoundedStackTest {
    private BoundedStack<String> stack;

    @BeforeEach
    void setUp() {
        stack = new BoundedStack<>(3);
    }

    @Nested
    @DisplayName("When stack is empty")
    class WhenEmpty {
        @Test
        void isEmptyReturnsTrue() {
            assertTrue(stack.isEmpty());
        }

        @Test
        void sizeIsZero() {
            assertEquals(0, stack.size());
        }

        @Test
        void popThrowsEmptyStack() {
            assertThrows(EmptyStackException.class, () -> stack.pop());
        }

        @Test
        void peekThrowsEmptyStack() {
            assertThrows(EmptyStackException.class, () -> stack.peek());
        }
    }

    @Nested
    @DisplayName("When stack has elements")
    class WhenHasElements {
        @BeforeEach
        void pushElements() {
            stack.push("first");
            stack.push("second");
        }

        @Test
        void isEmptyReturnsFalse() {
            assertFalse(stack.isEmpty());
        }

        @Test
        void sizeReturnsCount() {
            assertEquals(2, stack.size());
        }

        @Test
        void peekReturnsTopWithoutRemoving() {
            assertEquals("second", stack.peek());
            assertEquals(2, stack.size());
        }

        @Test
        void popReturnsAndRemovesTop() {
            assertEquals("second", stack.pop());
            assertEquals(1, stack.size());
            assertEquals("first", stack.pop());
            assertTrue(stack.isEmpty());
        }

        @Test
        void lifoOrder() {
            stack.push("third");
            assertEquals("third", stack.pop());
            assertEquals("second", stack.pop());
            assertEquals("first", stack.pop());
        }
    }

    @Nested
    @DisplayName("When stack is full")
    class WhenFull {
        @BeforeEach
        void fillStack() {
            stack.push("a");
            stack.push("b");
            stack.push("c");
        }

        @Test
        void pushThrowsWhenFull() {
            assertThrows(IllegalStateException.class, () -> stack.push("d"));
        }

        @Test
        void getCapacity() {
            assertEquals(3, stack.getCapacity());
        }
    }

    @Test
    @DisplayName("Clear empties the stack")
    void clearEmptiesStack() {
        stack.push("x");
        stack.push("y");
        stack.clear();
        assertTrue(stack.isEmpty());
        assertEquals(0, stack.size());
    }

    @Test
    @DisplayName("Zero or negative capacity throws")
    void invalidCapacityThrows() {
        assertThrows(IllegalArgumentException.class, () -> new BoundedStack<>(0));
        assertThrows(IllegalArgumentException.class, () -> new BoundedStack<>(-1));
    }

    @Test
    @DisplayName("Stack works with different types")
    void stackWithIntegers() {
        BoundedStack<Integer> intStack = new BoundedStack<>(5);
        intStack.push(42);
        intStack.push(99);
        assertEquals(99, intStack.pop());
        assertEquals(42, intStack.pop());
    }
}
