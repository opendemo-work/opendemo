# CORS 跨域配置演示

> 深入理解 Spring Boot 跨域配置的三种方式：全局配置、Filter 过滤器、@CrossOrigin 注解

## 🎯 学习目标

- ✅ 理解 CORS（Cross-Origin Resource Sharing）概念
- ✅ 掌握 WebMvcConfigurer 全局 CORS 配置
- ✅ 学会使用 Servlet Filter 实现 CORS
- ✅ 了解 @CrossOrigin 注解的用法
- ✅ 掌握预检请求（Preflight Request）的处理

---

## 📚 CORS 核心概念

| 概念 | 说明 |
|------|------|
| **Origin** | 请求来源（协议 + 域名 + 端口） |
| **Simple Request** | 简单请求，浏览器直接发送 |
| **Preflight Request** | 预检请求（OPTIONS），复杂请求前先发送 |
| **Access-Control-* ** | CORS 相关响应头 |

---

## 🛠️ CORS 三种配置方式

```
┌─────────────────────────────────────────────────────┐
│              CORS 配置方式对比                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. WebMvcConfigurer (全局配置)                      │
│     └── 适用于所有匹配的路径                          │
│                                                     │
│  2. CorsFilter (过滤器)                              │
│     └── 在 Servlet 层面处理，优先级最高               │
│                                                     │
│  3. @CrossOrigin (注解)                              │
│     └── 精确到单个 Controller 或方法                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 💻 核心代码

### 1. WebMvcConfigurer 全局配置

```java
@Configuration
public class CorsConfig {

    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                registry.addMapping("/api/**")
                        .allowedOrigins("http://localhost:3000")
                        .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                        .allowedHeaders("*")
                        .allowCredentials(true)
                        .maxAge(3600);
            }
        };
    }
}
```

### 2. CorsFilter 过滤器

```java
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class CorsFilter implements Filter {

    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain) {
        HttpServletResponse response = (HttpServletResponse) res;
        HttpServletRequest request = (HttpServletRequest) req;

        String origin = request.getHeader("Origin");
        response.setHeader("Access-Control-Allow-Origin", origin != null ? origin : "*");
        response.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
        response.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");

        if ("OPTIONS".equalsIgnoreCase(request.getMethod())) {
            response.setStatus(HttpServletResponse.SC_OK);
            return;
        }

        chain.doFilter(req, res);
    }
}
```

---

## 🚀 快速开始

### 1. 启动应用

```bash
cd java/cors-demo
mvn spring-boot:run
```

### 2. 测试 CORS

```bash
# GET 请求
curl -H "Origin: http://localhost:3000" http://localhost:8080/api/data

# POST 请求
curl -X POST -H "Origin: http://localhost:3000" \
  -H "Content-Type: application/json" \
  -d '{"name":"新项目"}' \
  http://localhost:8080/api/data

# OPTIONS 预检请求
curl -X OPTIONS -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  http://localhost:8080/api/data
```

### 3. 前端调用示例

```javascript
// 前端代码
fetch('http://localhost:8080/api/data')
  .then(response => response.json())
  .then(data => console.log(data));

// 使用 axios
axios.get('http://localhost:8080/api/data')
  .then(response => console.log(response.data));
```

---

## 📁 项目结构

```
cors-demo/
├── src/main/java/com/example/demo/
│   ├── CorsApplication.java              # 应用入口
│   ├── config/
│   │   └── CorsConfig.java               # 全局 CORS 配置
│   ├── filter/
│   │   └── CorsFilter.java               # CORS 过滤器
│   └── controller/
│       └── ApiController.java            # REST 控制器
├── src/test/java/com/example/demo/
│   └── CorsDemoTest.java                 # 单元测试
├── pom.xml
└── README.md
```

---

## 📋 CORS 响应头说明

| 响应头 | 说明 |
|--------|------|
| `Access-Control-Allow-Origin` | 允许的来源 |
| `Access-Control-Allow-Methods` | 允许的 HTTP 方法 |
| `Access-Control-Allow-Headers` | 允许的请求头 |
| `Access-Control-Allow-Credentials` | 是否允许携带凭证 |
| `Access-Control-Max-Age` | 预检请求缓存时间 |

---

## 🔧 安全注意事项

- 生产环境不应使用 `*` 作为 `Allow-Origin`
- `allowCredentials(true)` 时不能使用 `*`
- 注意区分简单请求和复杂请求
- 预检请求会增加额外开销，合理设置 `Max-Age`

---

## 🧪 测试

```bash
mvn test
```

---

## 📚 扩展学习

- [Spring Security JWT](../spring-security-jwt-demo/) - 安全认证
- [CSRF Protection](../csrf-protection-demo/) - CSRF 防护

---

*最后更新：2026年4月*
