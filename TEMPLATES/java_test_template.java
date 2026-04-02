/**
 * Java 测试模板
 *
 * 使用方法:
 * 1. 将此文件复制到 demo 目录下
 * 2. 重命名为 *Test.java
 * 3. 运行测试: mvn test 或 gradle test
 *
 * 测试命名规范:
 * - 测试类: <ClassName>Test
 * - 测试方法: test<MethodName><Scenario> 或 <methodName>Should<expected>When<condition>
 *
 * 依赖:
 * - JUnit 5 (Jupiter)
 * - 可选: AssertJ, Mockito
 */

import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.*;

/**
 * 功能测试类
 * 
 * 描述: [描述你要测试的功能]
 */
public class FeatureTest {

    // ============================================================================
    // 生命周期方法
    // ============================================================================

    @BeforeAll
    static void setUpClass() {
        // 所有测试前的设置
        System.out.println("测试类初始化");
    }

    @AfterAll
    static void tearDownClass() {
        // 所有测试后的清理
        System.out.println("测试类清理");
    }

    @BeforeEach
    void setUp() {
        // 每个测试前的设置
        System.out.println("测试方法初始化");
    }

    @AfterEach
    void tearDown() {
        // 每个测试后的清理
        System.out.println("测试方法清理");
    }

    // ============================================================================
    // 基本测试方法
    // ============================================================================

    @Test
    @DisplayName("测试正常情况")
    void testNormalCase() {
        // Arrange (准备)
        String input = "test_input";
        String expected = "expected_output";

        // Act (执行)
        // String result = yourFunction(input);
        String result = input; // 占位符

        // Assert (断言)
        assertEquals(expected, result);
    }

    @Test
    @DisplayName("测试边界情况 - 空输入")
    void testEdgeCaseEmptyInput() {
        // Arrange
        String input = "";

        // Act
        // String result = yourFunction(input);
        String result = input; // 占位符

        // Assert
        assertTrue(result.isEmpty());
    }

    @Test
    @DisplayName("测试异常情况")
    void testErrorCase() {
        // Arrange
        String invalidInput = null;

        // Act & Assert
        assertThrows(NullPointerException.class, () -> {
            // yourFunction(invalidInput);
            throw new NullPointerException("Invalid input"); // 占位符
        });
    }

    // ============================================================================
    // 参数化测试
    // ============================================================================

    @ParameterizedTest
    @DisplayName("参数化测试 - 多个输入")
    @ValueSource(strings = {"input1", "input2", "input3"})
    void testWithMultipleInputs(String input) {
        // 使用多个参数运行相同测试
        assertNotNull(input);
        assertFalse(input.isEmpty());
    }

    @ParameterizedTest
    @DisplayName("参数化测试 - CSV 数据源")
    @CsvSource({
        "1, 1, 2",     // a, b, expected
        "2, 3, 5",
        "10, 20, 30",
    })
    void testAddition(int a, int b, int expected) {
        // Act
        int result = a + b;

        // Assert
        assertEquals(expected, result, "加法结果应该正确");
    }

    // ============================================================================
    // 断言示例
    // ============================================================================

    @Test
    @DisplayName("各种断言示例")
    void testVariousAssertions() {
        // 基本断言
        assertEquals(2, 1 + 1);
        assertTrue(true);
        assertFalse(false);
        assertNull(null);
        assertNotNull("not null");

        // 对象断言
        Object obj1 = new Object();
        Object obj2 = obj1;
        assertSame(obj1, obj2);

        // 数组断言
        int[] expected = {1, 2, 3};
        int[] actual = {1, 2, 3};
        assertArrayEquals(expected, actual);

        // 带消息的断言
        assertEquals(4, 2 + 2, "数学错误: 2+2 应该等于 4");

        // 组合断言 (所有断言都会执行，失败的一起报告)
        assertAll("组合断言",
            () -> assertEquals(4, 2 + 2),
            () -> assertEquals("java", "java"),
            () -> assertTrue(true)
        );
    }

    // ============================================================================
    // 超时测试
    // ============================================================================

    @Test
    @DisplayName("测试超时 - 必须在2秒内完成")
    @Timeout(2) // 2秒超时
    void testTimeout() throws InterruptedException {
        // 模拟耗时操作
        Thread.sleep(100);
        assertTrue(true);
    }

    // ============================================================================
    // 重复测试
    // ============================================================================

    @RepeatedTest(5)
    @DisplayName("重复测试5次")
    void testRepeated(RepetitionInfo repetitionInfo) {
        System.out.println("当前重复: " + repetitionInfo.getCurrentRepetition());
        assertTrue(true);
    }

    // ============================================================================
    // 禁用测试
    // ============================================================================

    @Disabled("功能尚未实现")
    @Test
    @DisplayName("跳过的测试")
    void testSkipped() {
        // 这个测试会被跳过
    }

    @DisabledOnOs(OS.WINDOWS)
    @Test
    @DisplayName("在非Windows系统上运行")
    void testNotOnWindows() {
        // 只在非Windows系统上运行
    }

    // ============================================================================
    // 条件测试
    // ============================================================================

    @Test
    @EnabledIfSystemProperty(named = "env", matches = "ci")
    @DisplayName("只在CI环境运行")
    void testOnlyOnCI() {
        // 只在CI环境运行
    }

    @Test
    @EnabledIfEnvironmentVariable(named = "FEATURE_FLAG", matches = "true")
    @DisplayName("根据环境变量决定")
    void testBasedOnEnvVar() {
        // 根据环境变量决定是否运行
    }

    // ============================================================================
    // 嵌套测试
    // ============================================================================

    @Nested
    @DisplayName("嵌套测试组 - 用户管理")
    class UserManagementTests {

        @Test
        @DisplayName("创建用户")
        void testCreateUser() {
            assertTrue(true);
        }

        @Test
        @DisplayName("删除用户")
        void testDeleteUser() {
            assertTrue(true);
        }

        @Nested
        @DisplayName("嵌套测试组 - 用户权限")
        class UserPermissionTests {

            @Test
            @DisplayName("检查管理员权限")
            void testAdminPermission() {
                assertTrue(true);
            }
        }
    }

    // ============================================================================
    // 动态测试
    // ============================================================================

    @TestFactory
    @DisplayName("动态生成测试")
    Stream<DynamicTest> testDynamicTests() {
        return Stream.of("A", "B", "C")
            .map(text -> DynamicTest.dynamicTest("测试 " + text,
                () -> assertTrue(text.length() > 0)));
    }

    // ============================================================================
    // 性能测试
    // ============================================================================

    @Test
    @DisplayName("性能测试")
    void testPerformance() {
        // Arrange
        long startTime = System.currentTimeMillis();

        // Act
        for (int i = 0; i < 1000000; i++) {
            Math.sqrt(i);
        }

        long endTime = System.currentTimeMillis();
        long elapsedTime = endTime - startTime;

        // Assert
        assertTrue(elapsedTime < 1000, "操作应该在1秒内完成");
    }
}
