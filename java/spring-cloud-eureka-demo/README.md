# Spring Cloud Eureka 服务注册发现演示

> 微服务架构的核心：服务注册与发现

## 🎯 学习目标

- ✅ 理解服务注册与发现的概念
- ✅ 掌握Eureka Server搭建
- ✅ 掌握Eureka Client注册
- ✅ 理解服务健康检查

---

## 📚 核心概念

### 服务注册与发现流程

```
┌─────────────┐     注册      ┌─────────────┐
│  Service A  │ ─────────────▶│   Eureka    │
│  (Client)   │               │  (Server)   │
└─────────────┘               └──────┬──────┘
       │                              │
       │                              │ 查询
       │                              │
       │       发现                   ▼
       │◀────────────────────┌─────────────┐
       │                     │  Service B  │
       └────────────────────▶│  (Client)   │
                             └─────────────┘
```

---

## 🚀 快速开始

### 1. 启动Eureka Server

```bash
cd eureka-server
mvn spring-boot:run
```

访问: http://localhost:8761

### 2. 启动Eureka Client

```bash
cd eureka-client
mvn spring-boot:run
```

---

## 💻 核心代码

### Eureka Server

```java
@SpringBootApplication
@EnableEurekaServer
public class EurekaServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(EurekaServerApplication.class, args);
    }
}
```

### Eureka Client

```java
@SpringBootApplication
@EnableEurekaClient
public class EurekaClientApplication {
    public static void main(String[] args) {
        SpringApplication.run(EurekaClientApplication.class, args);
    }
}
```

---

*最后更新：2026年4月*
