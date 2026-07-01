<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Bean Validation Demo

> Spring Boot Bean Validation 演示项目 - 涵盖标准注解校验、自定义校验注解、全局异常处理

## 📚 学习目标

完成本案例后，您将能够：
- ✅ 掌握 JSR 380 (Bean Validation 2.0) 标准注解的使用
- ✅ 理解 `@NotNull`、`@NotBlank`、`@Size`、`@Email`、`@Min`、`@Max`、`@Pattern` 等注解
- ✅ 学会创建自定义校验注解（如 `@Phone`）
- ✅ 掌握 `@Valid` 和 `@RequestBody` 配合使用
- ✅ 理解全局异常处理 `@RestControllerAdvice` 的实现
- ✅ 能够设计统一的 API 响应格式

## 🛠️ 环境准备

### 系统要求
- **JDK版本**: OpenJDK 11+
- **构建工具**: Maven 3.6+
- **IDE推荐**: IntelliJ IDEA / Eclipse / VS Code
- **操作系统**: Windows/Linux/macOS

### 依赖安装
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
mvn clean install
```

## 📁 项目结构

```
bean-validation-demo/
├── src/
│   ├── main/
│   │   ├── java/com/example/demo/
│   │   │   ├── BeanValidationApplication.java    # 启动类
│   │   │   ├── entity/
│   │   │   │   └── User.java                      # 用户实体（含校验注解）
│   │   │   ├── controller/
│   │   │   │   └── UserController.java            # REST控制器
│   │   │   ├── exception/
│   │   │   │   └── GlobalExceptionHandler.java    # 全局异常处理
│   │   │   ├── dto/
│   │   │   │   └── ApiResponse.java               # 统一响应封装
│   │   │   └── validation/
│   │   │       ├── Phone.java                     # 自定义手机号注解
│   │   │       └── PhoneValidator.java             # 手机号校验逻辑
│   │   └── resources/
│   │       └── application.yml                    # 应用配置
│   └── test/
│       └── java/com/example/demo/
│           └── BeanValidationApplicationTest.java  # 测试类
├── pom.xml
├── README.md
└── metadata.json
```

## 🚀 快速开始

### 步骤1：启动项目
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd bean-validation-demo
mvn spring-boot:run
```

### 步骤2：测试校验功能
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 发送合法用户数据
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"zhangsan","email":"zhangsan@example.com","age":25,"password":"abc123","phone":"13800138000"}'

# 发送不合法数据（用户名为空）
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"","email":"bad","age":-1,"password":"short","phone":"123"}'

# 获取用户模板
curl http://localhost:8080/api/users/template
```

### 步骤3：运行测试
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
mvn test
```

## 🔍 核心代码解析

### 1. 实体类校验注解
`User.java` 中使用了多种标准校验注解：

| 注解 | 作用 | 示例 |
|------|------|------|
| `@NotBlank` | 字符串不能为null且长度>0 | `@NotBlank(message = "用户名不能为空")` |
| `@Size` | 限制字符串/集合长度 | `@Size(min = 2, max = 20)` |
| `@Email` | 校验邮箱格式 | `@Email(message = "邮箱格式不正确")` |
| `@NotNull` | 不能为null | `@NotNull(message = "年龄不能为空")` |
| `@Min/@Max` | 数值范围限制 | `@Min(value = 1)` |
| `@Pattern` | 正则表达式校验 | `@Pattern(regexp = "...")` |

### 2. 自定义校验注解

**`@Phone` 注解定义**：通过 `@Constraint` 关联校验器实现类，支持 `FIELD` 和 `PARAMETER` 级别的校验。

**`PhoneValidator` 校验逻辑**：实现 `ConstraintValidator` 接口，使用正则 `^1[3-9]\d{9}$` 匹配中国大陆手机号。当值为 null 或空字符串时返回 true（允许可选字段）。

### 3. 全局异常处理
`GlobalExceptionHandler` 使用 `@RestControllerAdvice` 捕获：
- `MethodArgumentNotValidException` - `@Valid` 校验失败
- `ConstraintViolationException` - 直接约束校验失败
- `Exception` - 通用异常兜底

### 4. 统一响应格式
```json
{
  "code": 400,
  "message": "参数校验失败",
  "data": null,
  "errors": {
    "username": "用户名不能为空",
    "email": "邮箱格式不正确"
  }
}
```

### 关键技术点
1. **`@Valid` vs `@Validated`**: `@Valid` 是 JSR 380 标准注解，`@Validated` 是 Spring 扩展注解，支持分组校验
2. **校验注解的 `message` 属性**: 支持国际化消息，默认使用硬编码字符串
3. **自定义注解三要素**: 注解定义 + `ConstraintValidator` 实现 + `@Constraint` 关联
4. **空值处理策略**: `@NotBlank` 不允许空字符串，`@NotNull` 只检查 null，`@Pattern` 允许 null

## ⚠️ 常见问题与解决方案

### Q1: @Valid 校验不生效怎么办？
**问题描述**: Controller 中使用了 `@Valid` 但校验没有触发
**解决方案**: 确保参数上有 `@RequestBody` 注解，且 pom.xml 中包含 `spring-boot-starter-validation` 依赖

### Q2: 如何对嵌套对象进行校验？
**问题描述**: 对象内部包含其他对象属性，内部对象的校验不生效
**解决方案**: 在嵌套属性上同时添加 `@Valid` 注解，如 `@Valid @NotNull private Address address;`

### Q3: 如何实现分组校验？
**问题描述**: 同一个实体类在不同场景下需要不同的校验规则
**解决方案**: 使用 `@Validated` 替代 `@Valid`，定义校验分组接口，在注解上指定 `groups` 属性

### Q4: 自定义注解的 isValid 返回 false 但没有错误消息？
**问题描述**: 自定义校验器校验失败但没有返回错误信息
**解决方案**: 确保注解的 `message` 属性有默认值，且 `ConstraintValidator` 的泛型类型与注解一致

## 📚 扩展学习

### 相关技术文档
- [JSR 380 Bean Validation 规范](https://beanvalidation.org/2.0/)
- [Spring Validation 官方文档](https://docs.spring.io/spring-framework/reference/core/validation.html)
- [Hibernate Validator 文档](https://hibernate.org/validator/documentation/)

### 进阶学习路径
1. 自定义校验器的高级用法（跨字段校验）
2. 校验分组与校验序列
3. 国际化错误消息（MessageSource）
4. Spring Validation 与 Spring Security 结合

### 企业级应用场景
- **表单提交校验**: 用户注册、信息修改等表单验证
- **API 参数校验**: RESTful API 的请求参数校验
- **数据导入校验**: 批量数据导入前的格式校验
- **业务规则校验**: 自定义注解实现复杂业务规则验证

---
> **💡 提示**: Bean Validation 是 Java EE 标准规范，Spring Boot 通过 `spring-boot-starter-validation` 自动集成 Hibernate Validator 实现，无需额外配置即可使用。

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际案例替换
./scripts/demo.sh
```
