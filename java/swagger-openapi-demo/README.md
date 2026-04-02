# Swagger OpenAPI Demo

Swagger OpenAPI文档生成演示项目，演示如何使用SpringDoc生成API文档。

## 技术栈

- Spring Boot 2.7
- SpringDoc OpenAPI
- Swagger UI

## 项目结构

```
swagger-openapi-demo/
├── src/main/java/com/example/demo/
│   ├── OpenApiDemoApplication.java        # 应用入口
│   ├── config/
│   │   └── OpenApiConfig.java             # OpenAPI配置
│   ├── controller/
│   │   └── UserController.java            # 用户控制器
│   └── entity/
│       └── User.java                      # 用户实体
├── pom.xml
└── README.md
```

## 什么是OpenAPI

OpenAPI Specification（OAS）是一种定义RESTful API的标准格式。Swagger是OpenAPI的实现工具，提供：
- 自动生成API文档
- 交互式API测试界面
- 代码生成

## 核心注解说明

### @Tag

```java
@RestController
@Tag(name = "用户管理", description = "用户相关的CRUD操作")
public class UserController { }
```

对API分组和添加描述。

### @Operation

```java
@Operation(summary = "获取所有用户", description = "返回系统中所有用户的列表")
@GetMapping
public ResponseEntity<List<User>> getAllUsers() { }
```

描述单个API操作。

### @ApiResponse

```java
@ApiResponses({
    @ApiResponse(responseCode = "200", description = "找到用户"),
    @ApiResponse(responseCode = "404", description = "用户不存在")
})
```

描述API响应。

### @Schema

```java
@Schema(description = "用户信息")
public class User {
    @Schema(description = "用户ID", example = "1")
    private Long id;
}
```

描述数据模型。

### @Parameter

```java
@GetMapping("/{id}")
public ResponseEntity<User> getUserById(
    @Parameter(description = "用户ID", example = "1") @PathVariable Long id) { }
```

描述参数信息。

## 快速开始

### 1. 启动应用

```bash
mvn spring-boot:run
```

### 2. 访问文档

| 地址 | 说明 |
|------|------|
| http://localhost:8080/swagger-ui.html | Swagger UI界面 |
| http://localhost:8080/v3/api-docs | OpenAPI JSON |

### 3. 使用Swagger UI

1. 打开 http://localhost:8080/swagger-ui.html
2. 展开用户管理标签
3. 点击"Try it out"按钮
4. 填写参数并点击"Execute"
5. 查看响应结果

## API端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/users | 获取所有用户 |
| GET | /api/users/{id} | 根据ID获取用户 |
| POST | /api/users | 创建用户 |
| PUT | /api/users/{id} | 更新用户 |
| DELETE | /api/users/{id} | 删除用户 |

## 配置说明

### OpenAPI配置

```java
@Bean
public OpenAPI customOpenAPI() {
    return new OpenAPI()
        .info(new Info()
            .title("用户管理API")
            .description("Swagger OpenAPI演示项目")
            .version("1.0.0")
            .contact(new Contact()
                .name("OpenDemo Team")
                .email("contact@opendemo.com"))
            .license(new License()
                .name("Apache 2.0")))
        .servers(List.of(
            new Server().url("http://localhost:8080"),
            new Server().url("https://api.opendemo.com")
        ));
}
```

### application.yml配置

```yaml
springdoc:
  api-docs:
    path: /v3/api-docs
  swagger-ui:
    path: /swagger-ui.html
    enabled: true
  packages-to-scan: com.example.demo.controller
```

## 生产环境建议

### 禁用Swagger

```yaml
springdoc:
  swagger-ui:
    enabled: false
```

### 添加认证

```java
@Bean
public OpenAPI customOpenAPI() {
    return new OpenAPI()
        .addSecurityItem(new SecurityRequirement().addList("bearerAuth"))
        .components(new Components()
            .addSecuritySchemes("bearerAuth",
                new SecurityScheme()
                    .type(SecurityScheme.Type.HTTP)
                    .scheme("bearer")
                    .bearerFormat("JWT")));
}
```

## 学习要点

1. OpenAPI规范的基本概念
2. SpringDoc注解的使用
3. Swagger UI的交互测试
4. API版本管理
5. 生产环境的安全配置
