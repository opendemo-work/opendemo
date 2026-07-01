<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Value Annotation Demo

> Spring @Value 注解演示项目 - 涵盖字面值注入、配置文件读取、SpEL 表达式、默认值设置

## 📚 学习目标

完成本案例后，您将能够：
- ✅ 掌握 `@Value` 注解的各种使用方式
- ✅ 理解字面值注入（直接赋值）
- ✅ 学会从配置文件读取属性值（`${property.key}`）
- ✅ 掌握默认值的设置方法（`${property.key:default}`）
- ✅ 理解 SpEL 表达式注入（`#{expression}`）
- ✅ 能够注入集合类型（List、数组）
- ✅ 区分 `${}` 和 `#{}` 的使用场景

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
value-annotation-demo/
├── src/
│   ├── main/
│   │   ├── java/com/example/demo/
│   │   │   ├── ValueAnnotationDemoApplication.java  # 启动类
│   │   │   ├── config/
│   │   │   │   └── AppProperties.java                # 配置属性类
│   │   │   ├── service/
│   │   │   │   └── ConfigService.java                # 配置服务
│   │   │   └── controller/
│   │   │       └── ConfigController.java             # REST控制器
│   │   └── resources/
│   │       └── application.yml                       # 应用配置（含自定义属性）
│   └── test/
│       └── java/com/example/demo/
│           └── ValueAnnotationDemoApplicationTest.java
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
cd value-annotation-demo
mvn spring-boot:run
```

### 步骤2：测试配置接口
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 获取基本配置（字面值 + 配置文件值）
curl http://localhost:8083/api/config/basic

# 获取数值类型配置
curl http://localhost:8083/api/config/numeric

# 获取 SpEL 表达式计算结果
curl http://localhost:8083/api/config/spel

# 获取集合类型配置
curl http://localhost:8083/api/config/collections

# 获取所有配置汇总
curl http://localhost:8083/api/config/all
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

### 1. @Value 的四种使用方式

#### 字面值注入
```java
@Value("literal-value")
private String literalValue;
```
直接赋予固定字符串值，通常用于常量注入。

#### 配置文件读取
```java
@Value("${app.name}")
private String appName;
```
通过 `${key}` 从配置文件中读取属性值。key 必须存在，否则启动报错。

#### 带默认值的配置读取
```java
@Value("${app.version:0.0.1}")
private String appVersion;
```
冒号 `:` 后面是默认值，当 key 不存在时使用默认值。

#### SpEL 表达式
```java
@Value("#{T(java.lang.Math).random() * 100}")
private double randomValue;
```
通过 `#{}` 使用 Spring Expression Language，支持方法调用、运算、访问系统属性等。

### 2. ${} 与 #{} 的区别

| 特性 | `${}` 占位符 | `#{}` SpEL 表达式 |
|------|-------------|-------------------|
| 来源 | 配置文件属性 | Spring 表达式 |
| 功能 | 简单字符串替换 | 复杂逻辑运算 |
| 默认值 | `${key:default}` | 不支持冒号默认值 |
| 类型转换 | 自动（基本类型） | 自动（任意类型） |
| 示例 | `${server.port}` | `#{T(Math).random()}` |

### 3. 集合类型注入

**数组注入**：
```java
@Value("${app.supported-locales:zh_CN,en_US}")
private String[] supportedLocales;
```
逗号分隔的字符串自动拆分为数组。

**List 注入（结合 SpEL）**：
```java
@Value("#{'${app.servers:localhost:8080}'.split(',')}")
private List<String> servers;
```
使用 SpEL 的 `split()` 方法将字符串拆分为 List。

### 4. 常用 SpEL 表达式示例

| 表达式 | 作用 |
|--------|------|
| `#{T(java.lang.Math).random() * 100}` | 生成 0-100 随机数 |
| `#{systemProperties['java.version']}` | 读取 JVM 系统属性 |
| `#{systemEnvironment['PATH']}` | 读取操作系统环境变量 |
| `#{beanName.methodName()}` | 调用 Spring Bean 方法 |
| `#{configProperty + '_suffix'}` | 字符串拼接 |

### 关键技术点
1. **类型自动转换**: `@Value` 支持将字符串自动转为 `int`、`boolean`、`double` 等基本类型
2. **启动校验**: 不带默认值的 `${key}` 如果 key 不存在会导致应用启动失败
3. **SpEL 中引用属性**: 可以在 `#{}` 中嵌套 `${}`，如 `#{'${app.name}'.toUpperCase()}`
4. **@Value vs @ConfigurationProperties**: `@Value` 适合少量属性，`@ConfigurationProperties` 适合批量属性绑定

## ⚠️ 常见问题与解决方案

### Q1: @Value 注入值为 null？
**问题描述**: 使用 `@Value` 注解但字段值为 null
**解决方案**: 确保类是 Spring 管理的 Bean（有 `@Component` 等注解），且不能在构造函数中使用 `@Value` 字段（此时还未注入），应使用 `@PostConstruct` 或构造器参数注入

### Q2: 应用启动报 "Could not resolve placeholder"？
**问题描述**: `@Value("${some.key}")` 找不到属性导致启动失败
**解决方案**: 检查配置文件中是否存在该 key，或添加默认值 `${some.key:default}`

### Q3: @Value 能注入静态字段吗？
**问题描述**: 尝试在 `static` 字段上使用 `@Value` 但值始终为 null
**解决方案**: `@Value` 不能直接注入静态字段。可通过非 static setter 方法间接赋值：
```java
private static String value;
@Value("${key}")
public void setValue(String value) { ClassName.value = value; }
```

### Q4: ${} 和 #{} 可以混合使用吗？
**问题描述**: 需要同时使用属性引用和 SpEL 表达式
**解决方案**: 可以在 SpEL 中嵌套占位符，如 `#{'${app.name}'.toUpperCase()}`，先解析 `${}` 再执行 SpEL

## 📚 扩展学习

### 相关技术文档
- [Spring @Value 官方文档](https://docs.spring.io/spring-framework/reference/core/beans/annotation-config/value-annotations.html)
- [SpEL 官方文档](https://docs.spring.io/spring-framework/reference/core/expressions.html)
- [Spring Boot Externalized Configuration](https://docs.spring.io/spring-boot/docs/2.7.x/reference/html/features.html#features.external-config)

### 进阶学习路径
1. `@ConfigurationProperties` 类型安全配置绑定
2. `@Value` 结合 `@Conditional` 实现条件化配置
3. SpEL 的高级用法（集合操作、正则匹配、安全导航）
4. Spring Boot 配置属性元数据生成

### 企业级应用场景
- **环境差异化配置**: 不同环境注入不同的数据库连接、超时时间等
- **功能开关**: 通过 `@Value` 注入布尔值控制功能启用/禁用
- **动态参数**: 注入可运行时变更的配置值
- **第三方集成**: 注入 API Key、回调地址等第三方服务配置

---
> **💡 提示**: `@Value` 适合简单场景的属性注入。当配置属性较多时，推荐使用 `@ConfigurationProperties` 配合 `@EnableConfigurationProperties`，可以获得类型安全、校验支持和 IDE 自动补全等优势。

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
