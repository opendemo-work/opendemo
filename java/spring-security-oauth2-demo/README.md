<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Spring Security OAuth2 Resource Server 示例

## 项目简介

本项目是一个基于 Spring Boot 2.7 和 Spring Security 的 OAuth2 Resource Server 示例，演示了如何使用 JWT（JSON Web Token）实现无状态的身份认证与授权。项目涵盖了 JWT 的生成、验证、解析以及基于角色和权限的访问控制。

## 技术栈

- Java 11
- Spring Boot 2.7.12
- Spring Security
- Spring Security OAuth2 Resource Server
- Nimbus JOSE + JWT
- Maven

## OAuth2 核心概念

### 什么是 OAuth2

OAuth2 是一个开放标准的授权框架，允许第三方应用在用户授权下访问用户存储在某个服务提供者上的信息，而不需要将用户名和密码提供给第三方应用。OAuth2 定义了四种授权方式：

### 授权码模式（Authorization Code Grant）

授权码模式是 OAuth2 中最完整、最安全的授权流程，适用于有后端的 Web 应用。其流程如下：

1. 客户端将用户重定向到授权服务器的授权页面
2. 用户在授权页面上登录并同意授权
3. 授权服务器将用户重定向回客户端，并附带授权码（Authorization Code）
4. 客户端使用授权码向授权服务器请求访问令牌（Access Token）
5. 授权服务器返回访问令牌和刷新令牌（Refresh Token）
6. 客户端使用访问令牌访问受保护的资源

这种模式的优势在于授权码只能使用一次，且通过后端通道交换令牌，令牌不会暴露在浏览器中。

### 客户端凭证模式（Client Credentials Grant）

客户端凭证模式适用于服务器到服务器的通信，即客户端以自己的名义而非用户的名义请求访问资源。流程如下：

1. 客户端向授权服务器提供 client_id 和 client_secret
2. 授权服务器验证客户端身份后返回访问令牌
3. 客户端使用访问令牌访问受保护资源

这种模式没有用户参与，适用于微服务之间的认证。

### 密码模式（Resource Owner Password Credentials Grant）

密码模式要求用户直接向客户端提供用户名和密码，客户端使用这些凭据向授权服务器请求令牌。由于安全性较低，这种模式仅在高度信任的场景下使用：

1. 用户向客户端提供用户名和密码
2. 客户端将凭据发送到授权服务器
3. 授权服务器验证后返回访问令牌

这种模式不推荐在生产环境中使用，仅作为遗留系统的兼容方案。

## JWT 令牌结构

JWT 由三部分组成，用点号（.）分隔：

### Header（头部）

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

头部包含令牌类型和签名算法信息，Base64Url 编码后形成 JWT 的第一部分。

### Payload（载荷）

```json
{
  "sub": "alice",
  "iss": "spring-security-oauth2-demo",
  "iat": 1685000000,
  "exp": 1685003600,
  "role": "ADMIN",
  "email": "alice@example.com"
}
```

载荷包含声明（Claims），包括注册声明（如 sub、iss、iat、exp）、公共声明和私有声明。本项目使用以下自定义声明：

- `role`: 用户角色，用于基于角色的访问控制
- `email`: 用户邮箱地址

### Signature（签名）

```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

签名用于验证令牌的完整性和真实性，防止令牌被篡改。

## Spring Security OAuth2 Resource Server 配置

### 安全过滤器链

本项目通过 `SecurityConfig` 配置安全过滤器链：

- 禁用 CSRF（因为是无状态的 REST API）
- 设置 Session 管理策略为无状态（STATELESS）
- 配置 URL 路径的访问规则：
  - `/api/auth/**` 和 `/api/public/**` 允许匿名访问
  - `/api/admin/**` 需要 ADMIN 角色
  - `/api/user/**` 需要 USER 或 ADMIN 角色
  - 其他所有请求需要认证
- 配置 OAuth2 Resource Server 使用 JWT

### JWT 解码器

使用 NimbusJwtDecoder 配合 HMAC-SHA256 对称密钥来验证和解析 JWT 令牌。在生产环境中，推荐使用 RSA 或 ECDSA 非对称密钥。

## 令牌验证流程

1. 客户端在请求头中携带 Bearer Token
2. Spring Security 的 OAuth2 Resource Server 拦截请求
3. JWT 解码器验证签名、过期时间、签发者等
4. 验证通过后，将 JWT 中的 Claims 映射为 Spring Security 的 Authentication 对象
5. 基于认证信息进行授权检查

## Scopes 和 Authorities

OAuth2 中的 Scope 和 Spring Security 中的 Authority/Role 是两个不同的概念：

- **Scope**: OAuth2 令牌的权限范围，由授权服务器在签发令牌时指定，表示客户端可以访问的资源范围
- **Authority/Role**: Spring Security 中的权限概念，表示用户的角色或权限

在本项目中，JWT 中的 `role` 字段被映射为 Spring Security 的 Authority，格式为 `ROLE_<role>`。例如，`role` 为 `ADMIN` 的用户将拥有 `ROLE_ADMIN` 权限。

## API 端点说明

### 公开端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/public/health` | 健康检查 |

### 认证端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/token` | 生成 JWT 令牌 |
| GET | `/api/auth/token-info` | 获取当前令牌信息 |
| GET | `/api/auth/userinfo` | 获取当前用户信息 |

### 用户端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/user/profile` | 获取当前用户资料 |

### 管理端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/admin/users` | 获取用户列表 |
| DELETE | `/api/admin/users/{username}` | 删除用户 |

## 使用示例

### 1. 生成令牌

```bash
curl -X POST http://localhost:8080/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "role": "ADMIN", "email": "alice@example.com"}'
```

响应：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "admin"
}
```

### 2. 访问受保护资源

```bash
curl http://localhost:8080/api/user/profile \
  -H "Authorization: Bearer <access_token>"
```

### 3. 获取令牌信息

```bash
curl http://localhost:8080/api/auth/token-info \
  -H "Authorization: Bearer <access_token>"
```

### 4. 管理员操作

```bash
curl http://localhost:8080/api/admin/users \
  -H "Authorization: Bearer <admin_access_token>"
```

## 安全最佳实践

### 令牌安全

- 使用 HTTPS 传输令牌，防止中间人攻击
- 设置合理的令牌过期时间，Access Token 通常不超过 1 小时
- 使用强密钥（256 位以上），生产环境推荐 RSA-2048 或更强的密钥
- 不要在令牌中存储敏感信息

### Resource Server 安全

- 始终验证令牌的签名和过期时间
- 实施最小权限原则，按角色和权限控制访问
- 使用无状态会话管理，避免 Session 固定攻击
- 记录所有认证失败事件，用于安全审计

### 生产环境建议

- 使用专业的授权服务器（如 Keycloak、Auth0、Okta）
- 使用非对称加密算法（RS256、ES256）而非对称加密
- 实施 Token Introspection 端点用于令牌状态查询
- 配置令牌撤销机制
- 使用短期 Access Token + 长期 Refresh Token 策略

## 项目结构

```
src/
├── main/
│   ├── java/com/example/demo/
│   │   ├── OAuth2DemoApplication.java
│   │   ├── config/
│   │   │   └── SecurityConfig.java
│   │   ├── controller/
│   │   │   ├── AuthController.java
│   │   │   └── ResourceController.java
│   │   ├── dto/
│   │   │   └── UserDto.java
│   │   ├── service/
│   │   │   └── TokenService.java
│   │   └── util/
│   │       └── JwtUtil.java
│   └── resources/
│       └── application.yml
└── test/
    └── java/com/example/demo/
        └── OAuth2DemoApplicationTest.java
```

## 构建与运行

```bash
mvn clean package
java -jar target/spring-security-oauth2-demo-1.0.0.jar
```

## 总结

本示例项目完整演示了 Spring Security OAuth2 Resource Server 的配置与使用，包括 JWT 令牌的生成与验证、基于角色的访问控制以及安全最佳实践。在实际项目中，应当结合专业的授权服务器使用，并遵循 OAuth2 和 OIDC 的最佳实践。

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
