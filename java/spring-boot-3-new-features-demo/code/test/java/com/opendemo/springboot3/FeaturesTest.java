package com.opendemo.springboot3;

import org.junit.jupiter.api.Test;

import java.time.LocalDate;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Spring Boot 3.x 新特性测试
 */
class FeaturesTest {

    @Test
    void testVirtualThreadsCreation() {
        // 验证虚拟线程可以正常创建
        Thread virtualThread = Thread.ofVirtual().start(() -> {
            System.out.println("虚拟线程运行中...");
        });

        assertDoesNotThrow(() -> virtualThread.join());
    }

    @Test
    void testRecordDtoCreation() {
        // 测试 Record DTO 创建
        UserDto user = new UserDto("张三", "zhangsan@example.com", 28);

        assertEquals("张三", user.name());
        assertEquals("zhangsan@example.com", user.email());
        assertEquals(28, user.age());
    }

    @Test
    void testRecordDtoEquality() {
        // 测试 Record 自动生成的 equals
        UserDto user1 = new UserDto("张三", "zhangsan@example.com", 28);
        UserDto user2 = new UserDto("张三", "zhangsan@example.com", 28);

        assertEquals(user1, user2);
        assertEquals(user1.hashCode(), user2.hashCode());
    }

    @Test
    void testRecordWithValidation() {
        // 测试带校验的 Record
        UserRegistrationRequest request = new UserRegistrationRequest(
            "张三",
            "test@example.com",
            LocalDate.of(1990, 5, 15)
        );

        assertEquals("张三", request.username());
        assertEquals(34, request.calculateAge());
    }

    @Test
    void testRecordValidationRejectsEmptyUsername() {
        // 测试空用户名校验
        assertThrows(IllegalArgumentException.class, () ->
            new UserRegistrationRequest("", "test@example.com", LocalDate.now())
        );
    }

    @Test
    void testApiResponse() {
        // 测试 API 响应封装
        ApiResponse<String> success = ApiResponse.success("OK");
        assertTrue(success.success());
        assertEquals("操作成功", success.message());

        ApiResponse<String> error = ApiResponse.error("失败原因");
        assertFalse(error.success());
        assertEquals("失败原因", error.message());
    }
}

// 测试用的 Record 定义 (与主类一致)
record UserDto(String name, String email, int age) {}

record UserRegistrationRequest(String username, String email, LocalDate birthDate) {
    public UserRegistrationRequest {
        if (username == null || username.isBlank()) {
            throw new IllegalArgumentException("用户名不能为空");
        }
    }

    public int calculateAge() {
        return birthDate != null
            ? java.time.Period.between(birthDate, LocalDate.now()).getYears()
            : 0;
    }
}

record ApiResponse<T>(boolean success, String message, T data) {
    public static <T> ApiResponse<T> success(T data) {
        return new ApiResponse<>(true, "操作成功", data);
    }
    public static <T> ApiResponse<T> error(String message) {
        return new ApiResponse<>(false, message, null);
    }
}