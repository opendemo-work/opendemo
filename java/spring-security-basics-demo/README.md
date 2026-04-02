# Spring Security 基础安全演示

> 掌握认证和授权的核心概念

## 🎯 学习目标

- ✅ 理解认证(Authentication)和授权(Authorization)
- ✅ 掌握UserDetails接口
- ✅ 了解Spring Security架构
- ✅ 掌握内存用户配置

---

## 📚 核心概念

### 认证 vs 授权

| 概念 | 英文 | 说明 |
|------|------|------|
| 认证 | Authentication | 验证你是谁（用户名密码） |
| 授权 | Authorization | 决定你能做什么（权限角色） |

### 核心接口

```java
UserDetails          // 用户信息
UserDetailsService   // 用户查询服务
AuthenticationManager // 认证管理器
GrantedAuthority     // 权限/角色
```

---

## 💻 核心代码

```java
@Service
public class UserService implements UserDetailsService {
    
    @Override
    public UserDetails loadUserByUsername(String username) {
        // 加载用户信息
    }
}

@Configuration
public class SecurityConfig {
    
    @Bean
    public AuthenticationManager authenticationManager() {
        // 配置认证
    }
}
```

---

## 🚀 运行

```bash
mvn clean compile
mvn exec:java -Dexec.mainClass="com.example.demo.Application"
```

---

*最后更新：2026年4月*
