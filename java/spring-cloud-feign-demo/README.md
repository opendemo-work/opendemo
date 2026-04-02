# Spring Cloud Feign Demo

Spring Cloud Feign声明式HTTP客户端示例项目，演示如何使用Feign进行服务间调用。

## 技术栈

- Spring Boot 2.7
- Spring Cloud OpenFeign
- Spring Web

## 项目结构

```
spring-cloud-feign-demo/
├── src/main/java/com/example/demo/
│   ├── FeignApplication.java              # 应用入口
│   ├── client/
│   │   └── UserServiceClient.java         # Feign客户端接口
│   └── controller/
│       └── FeignController.java           # 测试控制器
├── pom.xml
└── README.md
```

## 核心概念

### 什么是Feign

Feign是一个声明式的HTTP客户端，由Netflix开发，后被Spring Cloud集成。它让编写HTTP客户端变得更加简单，只需要创建一个接口并用注解来配置它。

### Feign的优势

1. **声明式调用**：像调用本地方法一样调用远程服务
2. **集成Ribbon**：内置负载均衡支持
3. **集成Hystrix**：支持服务降级和熔断
4. **简洁代码**：无需编写HTTP请求代码

## 核心注解说明

### @EnableFeignClients
在主类上启用Feign客户端扫描。

```java
@SpringBootApplication
@EnableFeignClients
public class FeignApplication {
    public static void main(String[] args) {
        SpringApplication.run(FeignApplication.class, args);
    }
}
```

### @FeignClient
定义Feign客户端接口。

```java
@FeignClient(name = "user-service", url = "http://localhost:8081")
public interface UserServiceClient {
    
    @GetMapping("/users/{id}")
    String getUserById(@PathVariable("id") Long id);
    
    @GetMapping("/users")
    String getAllUsers();
}
```

属性说明：
- `name`: 服务名称（用于服务发现）
- `url`: 服务URL（直接指定时跳过服务发现）
- `fallback`: 降级处理类
- `configuration`: 自定义配置类

## 快速开始

### 1. 添加依赖

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

### 2. 启用Feign

```java
@SpringBootApplication
@EnableFeignClients
public class FeignApplication { ... }
```

### 3. 创建Feign客户端

```java
@FeignClient(name = "user-service", url = "http://localhost:8081")
public interface UserServiceClient {
    @GetMapping("/users/{id}")
    User getUserById(@PathVariable Long id);
}
```

### 4. 注入使用

```java
@Service
public class UserService {
    @Autowired
    private UserServiceClient userServiceClient;
    
    public User getUser(Long id) {
        return userServiceClient.getUserById(id);
    }
}
```

## 运行测试

### 启动应用

```bash
mvn spring-boot:run
```

### 测试接口

需要先启动一个提供用户服务的服务（端口8081），或使用MockServer。

```bash
# 获取单个用户
curl http://localhost:8080/feign/users/1

# 获取所有用户
curl http://localhost:8080/feign/users
```

## 高级特性

### 1. 服务发现集成

配合Eureka使用时，无需指定url：

```java
@FeignClient(name = "user-service")  // 自动从Eureka发现服务
public interface UserServiceClient { ... }
```

### 2. 服务降级

```java
@FeignClient(name = "user-service", fallback = UserServiceClientFallback.class)
public interface UserServiceClient { ... }

@Component
public class UserServiceClientFallback implements UserServiceClient {
    @Override
    public String getUserById(Long id) {
        return "服务降级：无法获取用户信息";
    }
}
```

### 3. 请求/响应拦截器

```java
@Configuration
public class FeignConfig {
    @Bean
    public RequestInterceptor requestInterceptor() {
        return template -> {
            template.header("Authorization", "Bearer token");
            template.header("X-Request-ID", UUID.randomUUID().toString());
        };
    }
}
```

### 4. 自定义配置

```java
@FeignClient(name = "user-service", configuration = FeignConfig.class)
public interface UserServiceClient { ... }
```

## Feign与RestTemplate对比

| 特性 | Feign | RestTemplate |
|------|-------|--------------|
| 编码方式 | 声明式 | 编程式 |
| 代码量 | 少 | 多 |
| 可读性 | 高 | 一般 |
| 负载均衡 | 内置 | 需额外配置 |
| 熔断降级 | 支持 | 需手动实现 |
| 学习成本 | 低 | 中等 |

## 生产环境建议

1. **设置超时时间**
```yaml
feign:
  client:
    config:
      default:
        connectTimeout: 5000
        readTimeout: 5000
```

2. **启用压缩**
```yaml
feign:
  compression:
    request:
      enabled: true
    response:
      enabled: true
```

3. **日志级别**
```java
@Configuration
public class FeignConfig {
    @Bean
    Logger.Level feignLoggerLevel() {
        return Logger.Level.FULL;
    }
}
```

## 学习要点

1. 声明式HTTP客户端的设计思想
2. 接口代理实现机制
3. 与Ribbon、Hystrix的集成原理
4. 微服务间通信的最佳实践
5. 服务降级和熔断策略
