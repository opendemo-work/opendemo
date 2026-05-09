# Spring Authorization Server 演示

## 学习目标

1. 掌握 OAuth2 Authorization Server 配置
2. 理解 Authorization Code Flow
3. 学会实现自定义授权页面
4. 掌握令牌管理和 JWKS

## 环境要求

- JDK 17+
- Maven 3.9+

## OAuth2 流程

```
┌─────────┐     ┌─────────────┐     ┌──────────┐
│  Client │────→│ Authorization│────→│ Resource │
│         │←────│   Server    │←────│  Server  │
└─────────┘     └─────────────┘     └──────────┘
```

## 快速开始

```bash
cd spring-authorization-server-demo
mvn spring-boot:run
```

## 端点

- `GET /oauth2/authorize` - 授权端点
- `POST /oauth2/token` - 令牌端点
- `GET /.well-known/jwks.json` - JWKS 端点

## 客户端注册

```yaml
spring:
  authorization-server:
    client:
      my-client:
        registration:
          client-id: my-client
          client-secret: secret
          scopes: openid,profile,email
```

---

**技术栈**: Spring Boot 3.2 | Spring Authorization Server | OAuth2

**版本**: 1.0.0