# Validation Demo

Spring Boot参数校验演示项目，演示如何使用JSR-380进行数据验证。

## 技术栈

- Spring Boot 2.7
- Spring Validation
- Hibernate Validator

## 项目结构

```
validation-demo/
├── src/main/java/com/example/demo/
│   ├── ValidationDemoApplication.java     # 应用入口
│   ├── GlobalExceptionHandler.java        # 全局异常处理
│   ├── controller/
│   │   └── UserController.java            # 用户控制器
│   ├── entity/
│   │   └── User.java                      # 用户实体
│   └── validation/
│       ├── Phone.java                     # 自定义校验注解
│       └── PhoneValidator.java            # 自定义校验器
├── pom.xml
└── README.md
```

## 常用校验注解

### 空值检查

| 注解 | 说明 |
|------|------|
| `@Null` | 必须为null |
| `@NotNull` | 必须不为null |
| `@NotBlank` | 字符串必须不为空（去除空格后） |
| `@NotEmpty` | 字符串/集合必须不为空 |

### 数值检查

| 注解 | 说明 |
|------|------|
| `@Min` | 数值最小值 |
| `@Max` | 数值最大值 |
| `@DecimalMin` | 小数最小值 |
| `@DecimalMax` | 小数最大值 |
| `@Positive` | 正数 |
| `@Negative` | 负数 |

### 字符串检查

| 注解 | 说明 |
|------|------|
| `@Size` | 长度范围 |
| `@Length` | 长度（Hibernate） |
| `@Pattern` | 正则表达式匹配 |
| `@Email` | 邮箱格式 |

### 其他

| 注解 | 说明 |
|------|------|
| `@AssertTrue` | 必须为true |
| `@AssertFalse` | 必须为false |
| `@Past` | 过去日期 |
| `@Future` | 将来日期 |

## 快速开始

### 1. 启动应用

```bash
mvn spring-boot:run
```

### 2. 测试验证

```bash
# 验证失败 - 用户名太短
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "username": "j", "password": "123", "email": "invalid", "age": 16}'

# 验证失败 - 密码不符合要求
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "username": "john", "password": "12345678", "email": "john@example.com", "age": 25, "agreeTerms": true}'

# 验证成功
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "username": "john",
    "password": "Password123",
    "email": "john@example.com",
    "age": 25,
    "agreeTerms": true,
    "phone": "13800138000",
    "points": 100
  }'
```

## 自定义校验

### 1. 创建注解

```java
@Constraint(validatedBy = PhoneValidator.class)
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
public @interface Phone {
    String message() default "手机号格式不正确";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
```

### 2. 创建校验器

```java
public class PhoneValidator implements ConstraintValidator<Phone, String> {
    private static final Pattern PHONE_PATTERN = 
            Pattern.compile("^1[3-9]\\d{9}$");
    
    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        if (value == null || value.isEmpty()) {
            return true;
        }
        return PHONE_PATTERN.matcher(value).matches();
    }
}
```

### 3. 使用注解

```java
public class User {
    @Phone(message = "手机号格式不正确")
    private String phone;
}
```

## 分组校验

```java
public interface CreateGroup {}
public interface UpdateGroup {}

public class User {
    @Null(groups = CreateGroup.class)
    @NotNull(groups = UpdateGroup.class)
    private Long id;
}

@PostMapping
public ResponseEntity<?> create(
    @Validated(CreateGroup.class) @RequestBody User user) { }

@PutMapping
public ResponseEntity<?> update(
    @Validated(UpdateGroup.class) @RequestBody User user) { }
```

## 学习要点

1. JSR-380标准注解的使用
2. 自定义校验注解的实现
3. 分组校验的应用场景
4. 全局异常处理
5. 方法级参数校验
