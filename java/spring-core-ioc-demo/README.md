# Spring Core IoC 容器基础演示

> 深入理解Spring框架的核心：控制反转(IoC)和依赖注入(DI)

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解IoC（控制反转）的设计思想和优势
- ✅ 掌握Spring IoC容器的核心概念和API
- ✅ 使用注解方式配置和管理Bean
- ✅ 理解Bean的生命周期和作用域
- ✅ 掌握依赖注入的三种方式
- ✅ 理解组件扫描的工作原理

---

## 📚 核心概念

### 什么是IoC（控制反转）？

**IoC (Inversion of Control)** 是一种设计原则，它将对象的创建和管理从应用程序代码中剥离出来，交给容器（如Spring容器）来统一管理。

**传统方式 vs IoC方式**：

```
传统方式：
应用程序 → 主动创建对象 → 使用对象

IoC方式：
Spring容器 → 创建并管理对象 → 应用程序（被动接收）
```

### 什么是DI（依赖注入）？

**DI (Dependency Injection)** 是实现IoC的一种方式，通过容器将依赖关系注入到对象中，而不是由对象自己查找或创建依赖。

---

## 🛠️ 环境准备

### 系统要求

- **JDK**: 11 或更高版本
- **Maven**: 3.6+ 或 Gradle 7+
- **IDE**: IntelliJ IDEA / Eclipse / VS Code

### 验证环境

```bash
# 检查JDK版本
java -version

# 检查Maven版本
mvn -version
```

### 项目依赖

```xml
<dependencies>
    <!-- Spring Context (IoC容器) -->
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-context</artifactId>
        <version>5.3.21</version>
    </dependency>
</dependencies>
```

---

## 📁 项目结构

```
spring-core-ioc-demo/
├── src/
│   ├── main/
│   │   └── java/
│   │       └── com/example/demo/
│   │           ├── Application.java          # 应用入口
│   │           ├── config/
│   │           │   └── AppConfig.java        # Spring配置类
│   │           ├── model/
│   │           │   └── User.java             # 用户实体
│   │           ├── service/
│   │           │   ├── UserService.java      # 服务接口
│   │           │   └── impl/
│   │           │       └── UserServiceImpl.java  # 服务实现
│   └── test/
│       └── java/
│           └── com/example/demo/
│               └── UserServiceTest.java      # 单元测试
├── pom.xml                                   # Maven配置
├── metadata.json                             # 案例元数据
└── README.md                                 # 本文件
```

---

## 🚀 快速开始

### 步骤1：编译项目

```bash
cd spring-core-ioc-demo
mvn clean compile
```

### 步骤2：运行应用

```bash
mvn exec:java -Dexec.mainClass="com.example.demo.Application"
```

或

```bash
mvn package
java -jar target/spring-core-ioc-demo-1.0.0.jar
```

### 步骤3：运行测试

```bash
mvn test
```

---

## 💻 代码详解

### 1. 创建IoC容器

```java
// 使用注解配置创建容器
AnnotationConfigApplicationContext context = 
    new AnnotationConfigApplicationContext(AppConfig.class);
```

### 2. 定义Bean

**方式1：使用@Component注解（推荐）**

```java
@Service  // 等价于 @Component
public class UserServiceImpl implements UserService {
    // ...
}
```

**方式2：使用@Bean方法（显式配置）**

```java
@Configuration
public class AppConfig {
    @Bean
    public UserService userService() {
        return new UserServiceImpl();
    }
}
```

### 3. 获取Bean

```java
// 按类型获取
UserService userService = context.getBean(UserService.class);

// 按名称获取
UserService userService = (UserService) context.getBean("userServiceImpl");
```

### 4. Bean生命周期

```java
@Service
public class UserServiceImpl implements UserService {
    
    // 构造器
    public UserServiceImpl() {
        System.out.println("1. 构造器调用");
    }
    
    // 初始化方法
    @PostConstruct
    public void init() {
        System.out.println("2. 初始化方法 (@PostConstruct)");
    }
    
    // 销毁方法
    @PreDestroy
    public void destroy() {
        System.out.println("3. 销毁方法 (@PreDestroy)");
    }
}
```

### 5. 依赖注入方式

**方式1：构造器注入（推荐）**

```java
@Service
public class OrderService {
    private final UserService userService;
    
    @Autowired  // Spring 4.3+ 可以省略
    public OrderService(UserService userService) {
        this.userService = userService;
    }
}
```

**方式2：Setter注入**

```java
@Service
public class OrderService {
    private UserService userService;
    
    @Autowired
    public void setUserService(UserService userService) {
        this.userService = userService;
    }
}
```

**方式3：字段注入（不推荐）**

```java
@Service
public class OrderService {
    @Autowired
    private UserService userService;
}
```

---

## 🧪 验证测试

### 运行所有测试

```bash
mvn test
```

### 测试覆盖点

- ✅ 容器启动和Bean获取
- ✅ 根据ID查询用户
- ✅ 查询所有用户
- ✅ 创建用户
- ✅ 更新用户
- ✅ 删除用户

---

## ❓ 常见问题

### Q1: 如何切换XML配置和注解配置？

**A**: 
```java
// 注解配置
AnnotationConfigApplicationContext context = 
    new AnnotationConfigApplicationContext(AppConfig.class);

// XML配置
ClassPathXmlApplicationContext context = 
    new ClassPathXmlApplicationContext("application-context.xml");
```

### Q2: Bean的默认作用域是什么？

**A**: 默认是singleton（单例），即每个Spring容器中只有一个实例。其他作用域：
- `prototype`: 每次请求创建新实例
- `request`: HTTP请求范围
- `session`: HTTP会话范围

### Q3: 如何处理循环依赖？

**A**: 
1. 使用@Lazy延迟加载
2. 使用Setter注入代替构造器注入
3. 重构代码消除循环依赖（推荐）

### Q4: 如何查看容器中所有的Bean？

**A**:
```java
String[] beanNames = context.getBeanDefinitionNames();
for (String name : beanNames) {
    System.out.println(name);
}
```

---

## 📚 扩展学习

### 相关案例

- [Spring Bean生命周期演示](../spring-bean-lifecycle-demo/) - 深入了解Bean的完整生命周期
- [Spring AOP面向切面编程](../spring-aop-demo/) - 学习面向切面编程
- [Spring Data JPA集成](../spring-data-jpa-demo/) - 数据持久化技术

### 官方文档

- [Spring Framework 官方文档](https://docs.spring.io/spring-framework/docs/current/reference/html/)
- [Spring IoC 容器](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans)

### 推荐书籍

- 《Spring实战》(Spring in Action)
- 《Spring揭秘》
- 《Spring源码深度解析》

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request改进本案例！

---

## 📄 许可证

MIT License

---

*最后更新：2026年4月11日*
