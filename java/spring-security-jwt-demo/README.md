# Spring Security JWT Demo

Spring Security JWT认证授权演示项目，演示基于JWT的无状态认证机制。

## 技术栈

- Spring Boot 2.7
- Spring Security
- JJWT (Java JWT库)

## 项目结构

```
spring-security-jwt-demo/
├── src/main/java/com/example/demo/
│   ├── JwtDemoApplication.java            # 应用入口
│   ├── config/
│   │   └── SecurityConfig.java            # Security配置
│   ├── controller/
│   │   ├── AuthController.java            # 认证控制器
│   │   └── UserController.java            # 用户控制器
│   ├── entity/
│   │   └── User.java                      # 用户实体
│   ├── filter/
│   │   └── JwtAuthenticationFilter.java   # JWT认证过滤器
│   ├── service/
│   │   └── AuthService.java               # 认证服务
│   └── util/
│       └── JwtUtil.java                   # JWT工具类
├── src/main/resources/
│   └── application.yml                    # 应用配置
├── pom.xml
└── README.md
```

## JWT简介

### 什么是JWT

JWT (JSON Web Token) 是一种开放标准(RFC 7519)，用于在各方之间安全地传输信息作为JSON对象。

### JWT结构

```
xxxxx.yyyyy.zzzzz
  ↑      ↑      ↑
Header Payload Signature
```

**Header**: 包含令牌类型和签名算法
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload**: 包含声明(claims)
```json
{
  "sub": "username",
  "iat": 1516239022,
  "exp": 1516325422
}
```

**Signature**: 签名，确保令牌未被篡改
```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret
)
```

### JWT vs Session

| 特性 | JWT | Session |
|------|-----|---------|
| 存储位置 | 客户端 | 服务器端 |
| 扩展性 | 好（无状态） | 差（需要共享session） |
| 性能 | 无需查询数据库 | 需要查询session存储 |
| 安全性 | 需要防止令牌泄露 | session id相对安全 |
| 注销处理 | 复杂（令牌无法提前失效） | 简单（删除session） |

## 核心组件说明

### JwtUtil - JWT工具类

```java
@Component
public class JwtUtil {
    
    // 生成令牌
    public String generateToken(String username) {
        return Jwts.builder()
                .setSubject(username)
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + expiration))
                .signWith(key, SignatureAlgorithm.HS256)
                .compact();
    }
    
    // 验证令牌
    public Boolean validateToken(String token, String username) {
        String tokenUsername = getUsernameFromToken(token);
        return (tokenUsername.equals(username) && !isTokenExpired(token));
    }
}
```

### JwtAuthenticationFilter - 认证过滤器

```java
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {
    
    @Override
    protected void doFilterInternal(HttpServletRequest request, ... ) {
        // 1. 从请求头获取令牌
        String token = getTokenFromRequest(request);
        
        // 2. 验证令牌
        if (token != null && !jwtUtil.isTokenExpired(token)) {
            // 3. 设置安全上下文
            UsernamePasswordAuthenticationToken authentication = ...;
            SecurityContextHolder.getContext().setAuthentication(authentication);
        }
        
        filterChain.doFilter(request, response);
    }
}
```

### SecurityConfig - 安全配置

```java
@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf().disable()  // 禁用CSRF
            .sessionManagement()
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)  // 无状态
            .and()
            .authorizeRequests()
                .antMatchers("/api/auth/**").permitAll()  // 公开接口
                .anyRequest().authenticated()  // 其他需要认证
            .and()
            .addFilterBefore(jwtAuthenticationFilter, 
                UsernamePasswordAuthenticationFilter.class);
        
        return http.build();
    }
}
```

## 快速开始

### 1. 启动应用

```bash
mvn spring-boot:run
```

### 2. 登录获取Token

```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "123456"}'
```

响应：
```json
{
  "token": "eyJhbGciOiJIUzI1NiJ9...",
  "type": "Bearer",
  "username": "admin"
}
```

### 3. 访问受保护接口

```bash
# 获取用户信息（需要JWT）
curl http://localhost:8080/api/user/profile \
  -H "Authorization: Bearer {your-token}"

# 访问公开接口（无需JWT）
curl http://localhost:8080/api/public/info
```

### 4. 测试用户

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | 123456 | ADMIN, USER |
| user | 123456 | USER |
| guest | 123456 | GUEST |

## 认证流程

```
┌─────────┐                    ┌─────────────┐                    ┌─────────┐
│  Client │ ──1. 登录请求────▶ │ Auth Server │ ──2. 验证身份────▶ │   DB    │
└─────────┘                    └─────────────┘                    └─────────┘
     │                                │
     │ ◀────────3. 返回JWT───────────│
     │
     │ 4. 携带JWT访问API
     ▼
┌─────────────┐
│  API Server │ ──5. 验证JWT──▶ 返回数据
└─────────────┘
```

## API端点

### 认证接口

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | /api/auth/login | 用户登录 | 否 |

### 用户接口

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | /api/user/profile | 获取当前用户信息 | 是 |
| GET | /api/admin/users | 获取所有用户（ADMIN） | 是 |
| GET | /api/public/info | 公开信息 | 否 |

## 生产环境建议

### 1. 密钥安全

```yaml
# 使用环境变量存储密钥
jwt:
  secret: ${JWT_SECRET:defaultSecret}
```

### 2. 令牌刷新机制

```java
// 刷新令牌
public String refreshToken(String token) {
    if (validateToken(token)) {
        String username = getUsernameFromToken(token);
        return generateToken(username);
    }
    throw new RuntimeException("无效令牌");
}
```

### 3. 黑名单机制（注销）

```java
@Service
public class TokenBlacklistService {
    @Autowired
    private RedisTemplate<String, String> redisTemplate;
    
    public void addToBlacklist(String token) {
        redisTemplate.opsForValue().set(
            "blacklist:" + token, "1", 
            jwtUtil.getExpirationDateFromToken(token).getTime() - System.currentTimeMillis(), 
            TimeUnit.MILLISECONDS
        );
    }
    
    public boolean isBlacklisted(String token) {
        return Boolean.TRUE.equals(redisTemplate.hasKey("blacklist:" + token));
    }
}
```

### 4. HTTPS强制

```java
http.requiresChannel()
    .anyRequest()
    .requiresSecure();  // 强制HTTPS
```

## 常见问题

### Q: JWT令牌被盗怎么办？
A: 使用短期令牌 + 刷新令牌机制，或实现黑名单机制。

### Q: 如何存储JWT？
A: 推荐存储在内存中，需要持久化时可使用httpOnly cookie。

### Q: 令牌过期了怎么办？
A: 返回401，客户端使用刷新令牌获取新令牌，或重新登录。

## 学习要点

1. JWT结构和工作原理
2. 无状态认证的优势和限制
3. Spring Security过滤器链
4. 认证与授权的区别
5. 令牌的生成、验证、刷新
6. 安全最佳实践
