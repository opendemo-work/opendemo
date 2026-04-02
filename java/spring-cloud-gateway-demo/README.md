# Spring Cloud Gateway API网关演示

> 统一入口，智能路由

## 🎯 学习目标

- ✅ 理解API网关的作用
- ✅ 掌握路由配置
- ✅ 了解过滤器链
- ✅ 掌握负载均衡

---

## 📚 核心概念

### API网关架构

```
     客户端
        │
        ▼
   ┌─────────┐
   │ Gateway │  ← 路由、过滤、限流
   └────┬────┘
        │
   ┌────┴────┐
   ▼         ▼
ServiceA  ServiceB
```

---

## 💻 核心配置

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: http://localhost:8081
          predicates:
            - Path=/users/**
```

---

## 🚀 运行

```bash
mvn spring-boot:run
```

---

*最后更新：2026年4月*
