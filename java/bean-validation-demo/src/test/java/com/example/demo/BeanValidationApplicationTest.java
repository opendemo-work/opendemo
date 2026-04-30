package com.example.demo;

import com.example.demo.entity.User;
import com.example.demo.validation.PhoneValidator;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import javax.validation.ConstraintViolation;
import javax.validation.Validation;
import javax.validation.Validator;
import javax.validation.ValidatorFactory;

import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

class BeanValidationApplicationTest {

    private Validator validator;
    private PhoneValidator phoneValidator;

    @BeforeEach
    void setUp() {
        ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
        validator = factory.getValidator();
        phoneValidator = new PhoneValidator();
    }

    @Test
    void testValidUser() {
        User user = new User("zhangsan", "zhangsan@example.com", 25, "abc123", "13800138000");
        Set<ConstraintViolation<User>> violations = validator.validate(user);
        assertTrue(violations.isEmpty(), "合法用户不应该有校验错误");
    }

    @Test
    void testBlankUsername() {
        User user = new User("", "test@example.com", 25, "abc123", "13800138000");
        Set<ConstraintViolation<User>> violations = validator.validate(user);
        assertFalse(violations.isEmpty());
        assertTrue(violations.stream().anyMatch(v -> v.getMessage().contains("用户名")));
    }

    @Test
    void testShortUsername() {
        User user = new User("a", "test@example.com", 25, "abc123", "13800138000");
        Set<ConstraintViolation<User>> violations = validator.validate(user);
        assertFalse(violations.isEmpty());
        assertTrue(violations.stream().anyMatch(v -> v.getMessage().contains("2-20")));
    }

    @Test
    void testInvalidEmail() {
        User user = new User("zhangsan", "invalid-email", 25, "abc123", "13800138000");
        Set<ConstraintViolation<User>> violations = validator.validate(user);
        assertFalse(violations.isEmpty());
        assertTrue(violations.stream().anyMatch(v -> v.getMessage().contains("邮箱")));
    }

    @Test
    void testAgeTooSmall() {
        User user = new User("zhangsan", "test@example.com", 0, "abc123", "13800138000");
        Set<ConstraintViolation<User>> violations = validator.validate(user);
        assertFalse(violations.isEmpty());
        assertTrue(violations.stream().anyMatch(v -> v.getMessage().contains("大于0")));
    }

    @Test
    void testAgeTooLarge() {
        User user = new User("zhangsan", "test@example.com", 200, "abc123", "13800138000");
        Set<ConstraintViolation<User>> violations = validator.validate(user);
        assertFalse(violations.isEmpty());
        assertTrue(violations.stream().anyMatch(v -> v.getMessage().contains("150")));
    }

    @Test
    void testNullAge() {
        User user = new User("zhangsan", "test@example.com", null, "abc123", "13800138000");
        Set<ConstraintViolation<User>> violations = validator.validate(user);
        assertFalse(violations.isEmpty());
        assertTrue(violations.stream().anyMatch(v -> v.getMessage().contains("年龄")));
    }

    @Test
    void testPasswordWithoutDigit() {
        User user = new User("zhangsan", "test@example.com", 25, "abcdef", "13800138000");
        Set<ConstraintViolation<User>> violations = validator.validate(user);
        assertFalse(violations.isEmpty());
        assertTrue(violations.stream().anyMatch(v -> v.getMessage().contains("字母和数字")));
    }

    @Test
    void testPhoneValidator_Valid() {
        assertTrue(phoneValidator.isValid("13800138000", null));
        assertTrue(phoneValidator.isValid("15912345678", null));
    }

    @Test
    void testPhoneValidator_Invalid() {
        assertFalse(phoneValidator.isValid("12345678901", null));
        assertFalse(phoneValidator.isValid("10012345678", null));
    }

    @Test
    void testPhoneValidator_Null() {
        assertTrue(phoneValidator.isValid(null, null));
    }

    @Test
    void testPhoneValidator_Empty() {
        assertTrue(phoneValidator.isValid("", null));
    }

    @Test
    void testMultipleViolations() {
        User user = new User("", "bad", -1, "short", "123");
        Set<ConstraintViolation<User>> violations = validator.validate(user);
        assertTrue(violations.size() >= 4, "应该有多个校验错误");
    }

    @Test
    void testUserToString() {
        User user = new User("zhangsan", "test@example.com", 25, "abc123", "13800138000");
        String str = user.toString();
        assertTrue(str.contains("zhangsan"));
        assertTrue(str.contains("test@example.com"));
    }
}
