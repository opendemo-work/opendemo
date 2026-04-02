# Java TDD with JUnit

Java测试驱动开发实践。

## TDD循环

```
Red -> Green -> Refactor
写测试 -> 写代码 -> 重构
```

## JUnit 5示例

```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

public class CalculatorTest {
    private Calculator calculator;
    
    @BeforeEach
    void setUp() {
        calculator = new Calculator();
    }
    
    @Test
    @DisplayName("Adding two positive numbers")
    void testAdd() {
        // Arrange
        int a = 2;
        int b = 3;
        
        // Act
        int result = calculator.add(a, b);
        
        // Assert
        assertEquals(5, result);
    }
    
    @Test
    @DisplayName("Division by zero throws exception")
    void testDivideByZero() {
        assertThrows(ArithmeticException.class, () -> {
            calculator.divide(10, 0);
        });
    }
    
    @ParameterizedTest
    @CsvSource({
        "1, 1, 2",
        "2, 3, 5",
        "10, 20, 30"
    })
    void testAddParameterized(int a, int b, int expected) {
        assertEquals(expected, calculator.add(a, b));
    }
}

// 生产代码
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
    
    public int divide(int a, int b) {
        if (b == 0) {
            throw new ArithmeticException("Division by zero");
        }
        return a / b;
    }
}
```

## 测试金字塔

```
    /\
   /  \    E2E Tests (少数)
  /____\
 /      \  Integration Tests (中等)
/________\
            Unit Tests (大量)
```

## 学习要点

1. TDD三定律
2. JUnit 5特性
3. 测试命名规范
4. FIRST原则
5. 测试覆盖率
