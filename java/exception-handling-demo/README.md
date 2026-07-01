<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Exception Handling Demo - Spring Boot 全局异常处理

> Spring Boot 统一异常处理最佳实践：使用 @RestControllerAdvice、@ExceptionHandler 和自定义异常构建健壮的错误响应机制

## 目录

- [核心概念](#核心概念)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [异常体系设计](#异常体系设计)
- [@RestControllerAdvice 详解](#restcontrolleradvice-详解)
- [@ExceptionHandler 详解](#exceptionhandler-详解)
- [自定义异常](#自定义异常)
- [统一错误响应格式](#统一错误响应格式)
- [测试接口](#测试接口)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)

## 核心概念

### 为什么需要全局异常处理？

在没有全局异常处理的情况下，Spring Boot 默认会将未捕获的异常转换为 Whitelabel Error Page 或标准的 HTTP 错误响应。这种方式存在以下问题：

- 错误响应格式不统一，前后端难以约定
- 敏感信息可能泄露（堆栈信息暴露）
- 无法携带业务错误码
- 每个 Controller 重复编写 try-catch 代码

全局异常处理通过 `@RestControllerAdvice` + `@ExceptionHandler` 在统一层面拦截所有异常，生成一致的错误响应。

### Spring MVC 异常处理层次

```
请求 → Controller → 抛出异常
                         ↓
              @ExceptionHandler (方法级别)
                         ↓ (未处理)
              @ControllerAdvice (全局级别)
                         ↓ (未处理)
              Spring 默认错误处理 (BasicErrorController)
```

## 技术栈

- Java 11+
- Spring Boot 2.7.14
- Spring Web (spring-boot-starter-web)
- JUnit 5 + Spring Boot Test

## 项目结构

```
exception-handling-demo/
├── pom.xml
├── README.md
├── metadata.json
└── src/main/java/com/example/demo/
    ├── ExceptionHandlingApplication.java          # 启动类
    ├── controller/
    │   └── UserController.java                    # 用户 Controller
    ├── exception/
    │   ├── BusinessException.java                 # 业务异常
    │   └── ResourceNotFoundException.java         # 资源不存在异常
    ├── handler/
    │   └── GlobalExceptionHandler.java            # 全局异常处理器
    └── model/
        └── ErrorResponse.java                     # 统一错误响应
```

## 快速开始

```bash
# 编译项目
mvn clean package

# 运行项目
mvn spring-boot:run

# 运行测试
mvn test
```

应用启动后访问 `http://localhost:8080`

## 异常体系设计

### 异常类层次

```
RuntimeException
├── ResourceNotFoundException     # 资源不存在 (404)
├── BusinessException             # 业务逻辑异常 (400)
└── 其他 RuntimeException         # 系统异常 (500)
```

### 自定义异常的优势

1. **语义明确**：通过异常类名即可理解错误类型
2. **携带上下文**：可以封装业务错误码、错误详情等
3. **分类处理**：不同异常类型映射到不同 HTTP 状态码
4. **可扩展性**：可随时增加新的异常类型

## @RestControllerAdvice 详解

`@RestControllerAdvice` 是 `@ControllerAdvice` 和 `@ResponseBody` 的组合注解。

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    // 异常处理方法
}
```

### @ControllerAdvice 的属性

| 属性 | 说明 | 示例 |
|------|------|------|
| `basePackages` | 指定扫描的包 | `"com.example.demo.controller"` |
| `annotations` | 指定带有特定注解的 Controller | `RestController.class` |
| `assignableTypes` | 指定特定的 Controller 类 | `UserController.class` |

### 限定范围示例

```java
// 仅处理特定包下的 Controller
@RestControllerAdvice(basePackages = "com.example.demo.controller")
public class ApiExceptionHandler {}

// 仅处理带 @RestController 注解的类
@RestControllerAdvice(annotations = RestController.class)
public class ApiExceptionHandler {}
```

## @ExceptionHandler 详解

`@ExceptionHandler` 用于标记处理特定异常类型的方法。

### 工作机制

1. Spring MVC 捕获 Controller 抛出的异常
2. 首先查找当前 Controller 内的 `@ExceptionHandler` 方法
3. 如果未找到，查找 `@ControllerAdvice` 中的 `@ExceptionHandler` 方法
4. 匹配最精确的异常类型（子类优先）

### 返回值类型

| 返回类型 | 说明 |
|----------|------|
| `ResponseEntity<T>` | 完全控制 HTTP 响应（状态码、头、体） |
| `Map<String, Object>` | 直接作为 JSON 响应体，默认 200 |
| `ProblemDetail` | Spring 6 提供的 RFC 7807 标准错误响应 |
| `void` | 不返回响应体 |

### 异常匹配规则

```java
// 精确匹配 - 只处理 ResourceNotFoundException
@ExceptionHandler(ResourceNotFoundException.class)

// 多种异常 - 处理多种指定异常
@ExceptionHandler({BusinessException.class, IllegalArgumentException.class})

// 通配匹配 - 处理所有 RuntimeException
@ExceptionHandler(RuntimeException.class)
```

### 处理优先级

当多个 `@ExceptionHandler` 都能匹配时，Spring 选择**最接近异常继承体系**的那个。例如抛出 `ResourceNotFoundException`，同时存在：

- `@ExceptionHandler(ResourceNotFoundException.class)`
- `@ExceptionHandler(RuntimeException.class)`

Spring 会选择前者，因为它更精确。

## 自定义异常

### ResourceNotFoundException

用于表示请求的资源不存在，映射到 HTTP 404：

```java
public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}
```

### BusinessException

用于表示业务逻辑校验失败，携带业务错误码，映射到 HTTP 400：

```java
public class BusinessException extends RuntimeException {
    private final int code;

    public BusinessException(int code, String message) {
        super(message);
        this.code = code;
    }

    public int getCode() {
        return code;
    }
}
```

## 统一错误响应格式

### 错误响应结构

```json
{
    "timestamp": "2026-04-30T10:30:00",
    "status": 404,
    "error": "Not Found",
    "message": "用户不存在: 999",
    "path": "/api/users/999"
}
```

### 带业务错误码的响应

```json
{
    "timestamp": "2026-04-30T10:30:00",
    "status": 400,
    "code": 400001,
    "message": "用户名不能为空",
    "path": "/api/users"
}
```

### 设计原则

1. **统一格式**：所有错误响应遵循相同结构
2. **包含时间戳**：便于问题追踪和日志关联
3. **包含请求路径**：帮助定位问题
4. **不暴露堆栈**：生产环境不返回技术细节
5. **业务错误码**：前端可根据 code 做精确处理

## 测试接口

### 资源不存在异常 (404)

```bash
curl http://localhost:8080/api/users/999
```

响应：
```json
{
    "timestamp": "2026-04-30T10:30:00",
    "status": 404,
    "error": "Not Found",
    "message": "用户不存在: 999",
    "path": "/api/users/999"
}
```

### 业务异常 (400)

```bash
curl -X POST "http://localhost:8080/api/users?name="
```

响应：
```json
{
    "timestamp": "2026-04-30T10:30:00",
    "status": 400,
    "code": 400001,
    "message": "用户名不能为空",
    "path": "/api/users"
}
```

### 正常请求 (200)

```bash
curl http://localhost:8080/api/users/1
```

响应：`User1`

### 系统异常 (500)

```bash
curl http://localhost:8080/api/users/error
```

响应：
```json
{
    "timestamp": "2026-04-30T10:30:00",
    "status": 500,
    "error": "Internal Server Error",
    "message": "系统内部错误",
    "path": "/api/users/error"
}
```

## 最佳实践

### 1. 异常粒度设计

- 按业务领域设计异常类，而非按 HTTP 状态码
- 异常类应携带足够的上下文信息
- 避免创建过多的异常类，适当复用

### 2. 错误码规范

```
格式: XXYYYZ
XX   - 模块编号 (40=用户模块, 41=订单模块)
YYY  - 具体错误 (001=参数为空, 002=不存在)
Z    - 严重级别 (0=提示, 1=警告, 2=严重)
```

### 3. 日志记录

在 `@ExceptionHandler` 中记录异常日志，便于问题排查：

```java
@ExceptionHandler(Exception.class)
public ResponseEntity<ErrorResponse> handleException(Exception e, HttpServletRequest request) {
    log.error("系统异常: {} {}", request.getMethod(), request.getRequestURI(), e);
    // 返回错误响应
}
```

### 4. 生产环境安全

- 不要在错误响应中返回堆栈信息
- 不要返回 SQL 语句或数据库结构信息
- 对未知异常返回统一的 "系统繁忙" 提示

### 5. 与验证框架配合

Spring Boot Validation 抛出的 `MethodArgumentNotValidException` 和 `BindException` 也应该在全局异常处理器中统一处理。

## 常见问题

### Q: @ControllerAdvice 和 @RestControllerAdvice 的区别？

`@RestControllerAdvice` = `@ControllerAdvice` + `@ResponseBody`。在 REST API 项目中使用 `@RestControllerAdvice`，方法返回值会自动序列化为 JSON。

### Q: 多个 @ControllerAdvice 如何共存？

通过 `@Order` 注解控制优先级。`@Order(Ordered.HIGHEST_PRECEDENCE)` 优先级最高。

### Q: 如何获取当前请求的路径？

在 `@ExceptionHandler` 方法中注入 `HttpServletRequest` 参数即可：
```java
@ExceptionHandler(Exception.class)
public ResponseEntity<ErrorResponse> handle(Exception e, HttpServletRequest request) {
    String path = request.getRequestURI();
}
```

### Q: 异步方法中的异常能被捕获吗？

`@ExceptionHandler` 只能处理同步 Controller 中抛出的异常。异步方法（`@Async`、`CompletableFuture`）中的异常需要另外处理。

## 扩展阅读

- [Spring Boot Error Handling 官方文档](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.developing-web-applications.spring-mvc.error-handling)
- [RFC 7807 - Problem Details for HTTP APIs](https://tools.ietf.org/html/rfc7807)
- [Spring Framework @ExceptionHandler](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/ExceptionHandler.html)

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

```bash
./scripts/demo.sh
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

```bash
# 请根据实际案例替换
./scripts/demo.sh
```
