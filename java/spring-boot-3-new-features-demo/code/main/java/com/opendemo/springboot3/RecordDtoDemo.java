package com.opendemo.springboot3;

import java.time.LocalDate;
import java.time.Period;
import java.util.List;
import java.util.Optional;

/**
 * Record DTO 演示
 *
 * Java Record 是一种特殊类，用于创建不可变的数据类。
 * 自动生成:
 * - 构造方法
 * - equals(), hashCode()
 * - toString()
 * - getter 方法 (字段名而非 getXxx)
 *
 * 适用场景:
 * - DTO (Data Transfer Object)
 * - 不可变数据对象
 * - 方法返回值
 */
public class RecordDtoDemo {

    public static void main(String[] args) {
        System.out.println("===========================================");
        System.out.println("Record DTO 演示");
        System.out.println("===========================================\n");

        // 1. 基础 Record 用法
        demonstrateBasicRecord();

        // 2. 带校验的 Record
        demonstrateRecordWithValidation();

        // 3. Record 在 Spring Boot 中的应用
        demonstrateSpringBootUsage();

        System.out.println("\n===========================================");
        System.out.println("Record DTO 演示完成");
        System.out.println("===========================================");
    }

    /**
     * 基础 Record 用法演示
     */
    private static void demonstrateBasicRecord() {
        System.out.println("1. 基础 Record 用法:");

        // 使用 Record 创建 DTO
        UserDto user = new UserDto("张三", "zhangsan@example.com", 28);

        // 访问字段 (使用方法而非 getter)
        System.out.println("  用户名: " + user.name());
        System.out.println("  邮箱: " + user.email());
        System.out.println("  年龄: " + user.age());

        // 自动生成的 toString()
        System.out.println("  toString: " + user);

        // Record 是不可变的
        // user.name = "李四"; // 编译错误!

        System.out.println();
    }

    /**
     * 带校验的 Record 演示
     */
    private static void demonstrateRecordWithValidation() {
        System.out.println("2. 带校验的 Record:");

        try {
            // 正常创建
            UserRegistrationRequest request = new UserRegistrationRequest(
                "张三",
                "zhangsan@example.com",
                LocalDate.of(1990, 5, 15)
            );
            System.out.println("  创建成功: " + request);
        } catch (IllegalArgumentException e) {
            System.out.println("  创建失败: " + e.getMessage());
        }

        try {
            // 测试空用户名校验
            UserRegistrationRequest invalidRequest = new UserRegistrationRequest(
                "",
                "test@example.com",
                LocalDate.of(1990, 5, 15)
            );
            System.out.println("  创建成功: " + invalidRequest);
        } catch (IllegalArgumentException e) {
            System.out.println("  校验失败: " + e.getMessage());
        }

        System.out.println();
    }

    /**
     * Spring Boot 中使用 Record 演示
     */
    private static void demonstrateSpringBootUsage() {
        System.out.println("3. Spring Boot 中的 Record 用法:");

        // 模拟 API 响应
        ApiResponse<UserDto> response = ApiResponse.success(
            new UserDto("李四", "lisi@example.com", 30)
        );

        System.out.println("  响应: " + response);

        // 使用 Optional 的 Record
        Optional<UserDto> userOpt = Optional.of(
            new UserDto("王五", "wangwu@example.com", 25)
        );

        userOpt.ifPresent(user ->
            System.out.printf("  找到用户: %s (%s)%n",
                user.name(), user.email())
        );

        System.out.println();
    }

    // ========== Record 定义 ==========

    /**
     * 基础用户 DTO
     * 自动生成: 构造方法, equals, hashCode, toString, getter
     */
    public record UserDto(
        String name,
        String email,
        int age
    ) {}

    /**
     * 用户注册请求 (带校验)
     */
    public record UserRegistrationRequest(
        String username,
        String email,
        LocalDate birthDate
    ) {
        // 紧凑构造方法用于校验
        public UserRegistrationRequest {
            if (username == null || username.isBlank()) {
                throw new IllegalArgumentException("用户名不能为空");
            }
            if (email == null || !email.contains("@")) {
                throw new IllegalArgumentException("邮箱格式不合法");
            }
            if (birthDate != null && birthDate.isAfter(LocalDate.now())) {
                throw new IllegalArgumentException("出生日期不能在未来");
            }
        }

        // 可以添加额外方法
        public int calculateAge() {
            return birthDate != null
                ? Period.between(birthDate, LocalDate.now()).getYears()
                : 0;
        }
    }

    /**
     * API 响应封装
     */
    public record ApiResponse<T>(
        boolean success,
        String message,
        T data
    ) {
        // 静态工厂方法
        public static <T> ApiResponse<T> success(T data) {
            return new ApiResponse<>(true, "操作成功", data);
        }

        public static <T> ApiResponse<T> error(String message) {
            return new ApiResponse<>(false, message, null);
        }
    }
}