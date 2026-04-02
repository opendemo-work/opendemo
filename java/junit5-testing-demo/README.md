# JUnit5 Testing Demo

JUnit5单元测试框架演示项目，演示JUnit5的各种特性和最佳实践。

## 技术栈

- Spring Boot 2.7
- JUnit 5 (Jupiter)
- AssertJ (流式断言库)

## 项目结构

```
junit5-testing-demo/
├── src/main/java/com/example/demo/
│   ├── JUnit5DemoApplication.java         # 应用入口
│   ├── service/
│   │   └── Calculator.java                # 计算器类（被测类）
│   └── util/
│       └── StringUtils.java               # 字符串工具类（被测类）
├── src/test/java/com/example/demo/
│   ├── service/
│   │   └── CalculatorTest.java            # 计算器测试
│   └── util/
│       └── StringUtilsTest.java           # 字符串工具测试
├── pom.xml
└── README.md
```

## JUnit5核心概念

### JUnit5架构

```
JUnit 5 = JUnit Platform + JUnit Jupiter + JUnit Vintage

JUnit Platform: 运行测试的基础平台
JUnit Jupiter: JUnit5的新编程模型和扩展模型
JUnit Vintage: 向后兼容JUnit3/4
```

### 与JUnit4对比

| 特性 | JUnit 4 | JUnit 5 |
|------|---------|---------|
| 注解 | @Before, @After | @BeforeEach, @AfterEach |
| 扩展机制 | Runner (有限) | Extension API (灵活) |
| 参数化测试 | @RunWith(Parameterized.class) | @ParameterizedTest |
| 动态测试 | 不支持 | @TestFactory |
| 嵌套测试 | 不支持 | @Nested |

## 核心注解说明

### 生命周期注解

```java
@BeforeAll  // 类级别，所有测试前执行一次 (需static)
@BeforeEach // 方法级别，每个测试前执行
@Test       // 标记测试方法
@AfterEach  // 方法级别，每个测试后执行
@AfterAll   // 类级别，所有测试后执行一次 (需static)
```

### 禁用和条件注解

```java
@Disabled          // 禁用测试
@EnabledOnOs       // 特定操作系统才执行
@EnabledIfSystemProperty // 系统属性条件
@Timeout           // 超时设置
```

### 参数化测试

```java
@ParameterizedTest
@ValueSource(strings = {"racecar", "radar", "level"})
void testPalindromes(String candidate) {
    assertThat(StringUtils.isPalindrome(candidate)).isTrue();
}

@ParameterizedTest
@CsvSource({
    "1, 1, 2",
    "2, 3, 5",
    "10, 20, 30"
})
void testAdd(int a, int b, int expected) {
    assertThat(calculator.add(a, b)).isEqualTo(expected);
}
```

## 快速开始

### 运行测试

```bash
# 运行所有测试
mvn test

# 运行单个测试类
mvn test -Dtest=CalculatorTest

# 运行单个测试方法
mvn test -Dtest=CalculatorTest#testAdd
```

### 查看测试报告

```bash
# 测试报告路径
target/surefire-reports/
```

## 测试示例

### 基础测试

```java
@Test
@DisplayName("加法测试")
void testAdd() {
    // given
    int a = 2;
    int b = 3;
    
    // when
    int result = calculator.add(a, b);
    
    // then
    assertThat(result).isEqualTo(5);
}
```

### 异常测试

```java
@Test
@DisplayName("除数为0应抛出异常")
void testDivideByZero() {
    assertThatThrownBy(() -> calculator.divide(10, 0))
            .isInstanceOf(ArithmeticException.class)
            .hasMessageContaining("除数不能为0");
}
```

### 嵌套测试

```java
@Nested
@DisplayName("字符串截断测试组")
class TruncateTests {
    
    @Test
    @DisplayName("不需要截断")
    void testTruncateNotNeeded() {
        assertThat(StringUtils.truncate("hello", 10)).isEqualTo("hello");
    }
    
    @Test
    @DisplayName("需要截断")
    void testTruncateNeeded() {
        assertThat(StringUtils.truncate("hello world", 8)).isEqualTo("hello...");
    }
}
```

### 动态测试

```java
@TestFactory
@DisplayName("动态测试")
Stream<DynamicTest> dynamicTests() {
    return Stream.of("racecar", "radar", "level")
            .map(text -> DynamicTest.dynamicTest("测试 " + text,
                    () -> assertThat(StringUtils.isPalindrome(text)).isTrue()));
}
```

## AssertJ断言

### 基本断言

```java
assertThat(result).isEqualTo(5);
assertThat(result).isPositive();
assertThat(result).isGreaterThan(4);
assertThat(result).isLessThan(10);
assertThat(result).isBetween(1, 10);
```

### 字符串断言

```java
assertThat(name).isEqualTo("John")
                .startsWith("Jo")
                .endsWith("hn")
                .hasSize(4);
```

### 集合断言

```java
assertThat(list).hasSize(3)
                .contains("a", "b")
                .doesNotContain("z");
```

### 异常断言

```java
assertThatThrownBy(() -> {
    // 可能抛出异常的代码
}).isInstanceOf(IllegalArgumentException.class)
  .hasMessage("错误消息");
```

## 测试最佳实践

### 1. 测试命名规范

```java
// 好
@Test
@DisplayName("用户注册时邮箱已存在应抛出异常")
void shouldThrowExceptionWhenEmailExists() { }

// 不好
@Test
void test1() { }
```

### 2. 测试结构 (Given-When-Then)

```java
@Test
void testSomething() {
    // Given - 准备测试数据
    User user = new User("john", "john@example.com");
    
    // When - 执行被测方法
    boolean result = userService.register(user);
    
    // Then - 验证结果
    assertThat(result).isTrue();
}
```

### 3. 独立测试

每个测试应该独立，不依赖其他测试的执行顺序。

### 4. 单一职责

一个测试只验证一个概念。

## 高级特性

### 扩展机制

```java
public class TimingExtension implements BeforeTestExecutionCallback, AfterTestExecutionCallback {
    
    @Override
    public void beforeTestExecution(ExtensionContext context) {
        context.getStore(ExtensionContext.Namespace.GLOBAL)
               .put("startTime", System.currentTimeMillis());
    }
    
    @Override
    public void afterTestExecution(ExtensionContext context) {
        long startTime = context.getStore(ExtensionContext.Namespace.GLOBAL)
                                .remove("startTime", long.class);
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("Test took " + duration + " ms");
    }
}

// 使用扩展
@ExtendWith(TimingExtension.class)
class MyTest { }
```

### 条件执行

```java
@Test
@EnabledIfSystemProperty(named = "env", matches = "dev")
void onlyOnDev() { }

@Test
@EnabledIf("customCondition")
void conditionalTest() { }

boolean customCondition() {
    return true;
}
```

## 学习要点

1. JUnit5架构和与JUnit4的区别
2. 生命周期注解的使用
3. 参数化测试的多种方式
4. 嵌套测试组织测试结构
5. AssertJ流式断言的优势
6. 异常测试的编写方式
7. 扩展机制实现自定义功能
