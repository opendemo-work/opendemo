# CSRF 防护示例

## 项目简介

本项目是一个基于 Spring Boot 2.7 和 Spring Security 的 CSRF（Cross-Site Request Forgery，跨站请求伪造）防护示例。项目演示了 Spring Security 内置的 CSRF 防护机制、同步令牌模式、Cookie-based CSRF Token 以及在 REST API 中的防护策略。

## 技术栈

- Java 11
- Spring Boot 2.7.12
- Spring Security
- Thymeleaf
- Maven

## CSRF 攻击详解

### 什么是 CSRF 攻击

CSRF（跨站请求伪造）是一种 Web 安全漏洞，攻击者利用已认证用户的身份，在用户不知情的情况下发起恶意请求。攻击者不需要获取用户的密码或 Session ID，只需要诱骗用户访问一个恶意页面。

### CSRF 攻击原理

1. 用户登录受信任的网站 A，浏览器保存了 Session Cookie
2. 用户在同一浏览器中访问了恶意网站 B
3. 恶意网站 B 的页面中包含对网站 A 的请求（如自动提交的表单）
4. 浏览器会自动携带网站 A 的 Cookie，因此请求看起来是合法的
5. 网站 A 无法区分这是用户的真实操作还是攻击者伪造的请求

### CSRF 攻击示例

假设银行网站的转账接口为：

```html
<form action="/api/transfer" method="POST">
    <input name="toAccount" value="attacker"/>
    <input name="amount" value="10000"/>
</form>
```

攻击者可以构造如下恶意页面：

```html
<html>
<body>
    <h1>恭喜中奖！</h1>
    <form action="http://bank.com/api/transfer" method="POST" style="display:none">
        <input name="toAccount" value="attacker_account"/>
        <input name="amount" value="10000"/>
    </form>
    <script>document.forms[0].submit();</script>
</body>
</html>
```

当已登录银行网站的用户访问此恶意页面时，转账请求会自动提交，浏览器携带有效的 Session Cookie，服务器无法区分这是攻击。

### CSRF 攻击条件

- 用户必须已登录目标网站
- 攻击者需要知道目标网站的请求格式
- 目标网站必须仅依赖 Cookie 进行身份验证
- 请求必须是状态改变的（POST、PUT、DELETE 等）

## 同步令牌模式（Synchronizer Token Pattern）

### 工作原理

同步令牌模式是最常见的 CSRF 防护方式：

1. 服务器为每个用户会话生成一个随机的 CSRF Token
2. Token 被嵌入到每个表单的隐藏字段中
3. 用户提交表单时，Token 随表单一起发送
4. 服务器验证提交的 Token 是否与会话中的 Token 匹配
5. 如果不匹配，请求被拒绝

由于攻击者无法获取用户的 CSRF Token（同源策略限制），因此无法构造有效的伪造请求。

### Spring Security 中的实现

Spring Security 默认启用 CSRF 防护，自动在所有表单中注入 CSRF Token。使用 Thymeleaf 时，只需在表单中添加：

```html
<input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/>
```

或者在 `<form>` 标签中使用 Thymeleaf 的 `th:action` 属性，Thymeleaf 会自动添加隐藏的 CSRF Token 字段。

## SameSite Cookie 属性

### SameSite 属性值

SameSite 是一个 Cookie 属性，用于控制 Cookie 在跨站请求中是否发送：

- **Strict**: Cookie 仅在同站请求中发送。即使用户从外部链接点击进入网站，Cookie 也不会发送。安全性最高但可能影响用户体验。
- **Lax**: Cookie 在同站请求和安全的跨站导航请求（如 GET 请求的链接点击）中发送。这是大多数浏览器的默认值。安全性与可用性的平衡。
- **None**: Cookie 在所有请求中发送。必须配合 Secure 属性（仅 HTTPS）。适用于需要跨站携带 Cookie 的场景。

### SameSite 与 CSRF 防护

SameSite=Lax 可以有效防止大多数 CSRF 攻击，因为跨站的 POST 请求不会携带 Cookie。但 SameSite 不能完全替代 CSRF Token：

- 某些旧浏览器不支持 SameSite 属性
- SameSite=Strict 可能影响合法的跨站导航
- 依赖浏览器实现，不同浏览器行为可能不同

最佳实践是同时使用 CSRF Token 和 SameSite Cookie，实现深度防御。

## Spring Security CSRF 防护配置

### 默认行为

Spring Security 默认对以下情况启用 CSRF 防护：
- 所有使用 Session 的应用
- 所有状态改变的 HTTP 方法（POST、PUT、DELETE、PATCH）
- GET、HEAD、OPTIONS、TRACE 请求不需要 CSRF Token

### CookieCsrfTokenRepository

本项目使用 `CookieCsrfTokenRepository`，将 CSRF Token 存储在 Cookie 中：

```java
CookieCsrfTokenRepository repository = new CookieCsrfTokenRepository();
repository.setCookieHttpOnly(false);
repository.setCookieName("XSRF-TOKEN");
repository.setHeaderName("X-XSRF-TOKEN");
```

配置说明：
- `setCookieHttpOnly(false)`: 允许 JavaScript 读取 Cookie，前端 AJAX 可以获取 Token
- `setCookieName("XSRF-TOKEN")`: Cookie 名称，符合 Angular 等前端框架的约定
- `setHeaderName("X-XSRF-TOKEN")`: 通过请求头传递 Token 的名称

### HttpSessionCsrfTokenRepository

另一种选择是使用 `HttpSessionCsrfTokenRepository`，将 Token 存储在服务器 Session 中：

```java
CsrfTokenRepository repository = new HttpSessionCsrfTokenRepository();
```

这种方式更安全（Token 不暴露在 Cookie 中），但不适合无状态的 REST API。

## REST API 中的 CSRF 防护

### 何时可以禁用 CSRF

对于纯无状态的 REST API（使用 JWT 或 Bearer Token 认证），可以安全地禁用 CSRF：

```java
http.csrf().disable();
```

原因：
- REST API 通常不依赖 Cookie 进行认证
- Bearer Token 需要手动添加到请求头中
- 攻击者无法通过跨站请求获取 Bearer Token

### 何时应该保留 CSRF

- 使用 Session Cookie 认证的 API
- 浏览器直接访问的 API（如传统 Web 应用）
- 同时支持 Cookie 和 Token 认证的 API

### Double Submit Cookie 模式

Double Submit Cookie 是一种适用于 REST API 的 CSRF 防护模式：

1. 服务器在 Cookie 中设置一个随机 Token
2. 前端 JavaScript 读取 Cookie 中的 Token
3. 前端在请求头或参数中携带该 Token
4. 服务器比较 Cookie 中的 Token 和请求中的 Token

```javascript
// 前端获取 CSRF Token
function getCsrfToken() {
    const match = document.cookie.match(/XSRF-TOKEN=([^;]+)/);
    return match ? match[1] : null;
}

// 在请求头中携带 Token
fetch('/api/transfer', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-XSRF-TOKEN': getCsrfToken()
    },
    body: JSON.stringify({ toAccount: 'bob', amount: 100 })
});
```

这种模式的安全性基于攻击者无法读取跨域 Cookie 的值（同源策略）。

## API 端点说明

| 方法 | 路径 | 说明 | CSRF 保护 |
|------|------|------|-----------|
| GET | `/home` | 首页 | 否 |
| GET | `/api/csrf/token` | 获取 CSRF Token | 否 |
| POST | `/api/transfer` | 执行转账 | 是 |
| GET | `/api/transfer/history` | 查询转账历史 | 否 |

## 使用示例

### 1. 获取 CSRF Token

```bash
curl -c cookies.txt http://localhost:8081/api/csrf/token
```

### 2. 执行受保护的转账操作

```bash
curl -b cookies.txt -X POST http://localhost:8081/api/transfer \
  -H "Content-Type: application/json" \
  -H "X-XSRF-TOKEN: <token_from_step_1>" \
  -d '{"toAccount": "bob", "amount": 500}'
```

### 3. 查询转账历史

```bash
curl -b cookies.txt http://localhost:8081/api/transfer/history
```

## 安全最佳实践

### 防护策略组合

- 同时使用 CSRF Token 和 SameSite Cookie
- 对所有状态改变的请求强制 CSRF 验证
- 使用安全随机数生成器创建 CSRF Token
- Token 应具有足够的长度和熵

### Token 管理

- 每个会话使用唯一的 CSRF Token
- Token 在登录后重新生成
- Token 在登出后失效
- 考虑 Token 的定期轮换

### 其他防护措施

- 实施 Content Security Policy（CSP）
- 设置 X-Frame-Options 头防止 Clickjacking
- 使用 HTTPS 防止 Token 被窃取
- 验证 Referer/Origin 头作为额外防护

## 项目结构

```
src/
├── main/
│   ├── java/com/example/demo/
│   │   ├── CsrfProtectionDemoApplication.java
│   │   ├── config/
│   │   │   └── SecurityConfig.java
│   │   ├── controller/
│   │   │   ├── HomeController.java
│   │   │   ├── TransferController.java
│   │   │   └── CsrfController.java
│   │   ├── service/
│   │   │   └── TransferService.java
│   │   └── model/
│   │       └── TransferRequest.java
│   └── resources/
│       ├── application.yml
│       └── templates/
│           └── home.html
└── test/
    └── java/com/example/demo/
        └── CsrfProtectionDemoApplicationTest.java
```

## 构建与运行

```bash
mvn clean package
java -jar target/csrf-protection-demo-1.0.0.jar
```

访问 http://localhost:8081 查看演示。

## 测试账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| alice | password123 | USER |
| bob | admin456 | USER, ADMIN |

## 总结

本示例项目完整演示了 CSRF 攻击的原理和 Spring Security 的 CSRF 防护机制。通过同步令牌模式、SameSite Cookie 和 Double Submit Cookie 等多种防护策略的组合，可以有效防止 CSRF 攻击。在实际项目中，应根据应用类型选择合适的防护策略，并遵循深度防御原则。
