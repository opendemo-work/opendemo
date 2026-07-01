<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Filter Interceptor Demo - Servlet Filter 与 HandlerInterceptor

> Spring Boot 请求处理链演示：Filter、Interceptor、Controller 的协作机制与实战应用

## 目录

- [核心概念](#核心概念)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [Filter 详解](#filter-详解)
- [HandlerInterceptor 详解](#handlerinterceptor-详解)
- [Filter vs Interceptor 对比](#filter-vs-interceptor-对比)
- [注册与配置](#注册与配置)
- [执行顺序](#执行顺序)
- [测试接口](#测试接口)
- [实战场景](#实战场景)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)

## 核心概念

### Spring Boot 请求处理流程

```
HTTP Request
    ↓
Servlet Container (Tomcat)
    ↓
Filter Chain (Filter1 → Filter2 → ...)
    ↓
DispatcherServlet (Spring MVC)
    ↓
HandlerInterceptor (preHandle)
    ↓
Controller Method
    ↓
HandlerInterceptor (postHandle)
    ↓
View Rendering
    ↓
HandlerInterceptor (afterCompletion)
    ↓
Filter Chain (反向)
    ↓
HTTP Response
```

### 为什么需要 Filter 和 Interceptor？

- **横切关注点**：日志、认证、CORS、压缩等逻辑不应写在 Controller 中
- **分层处理**：Filter 处理与 Servlet 容器相关的逻辑，Interceptor 处理与 Spring MVC 相关的逻辑
- **可复用**：通过配置灵活组合，不同接口可应用不同的处理链

## 技术栈

- Java 11+
- Spring Boot 2.7.14
- Spring Web (spring-boot-starter-web)
- JUnit 5 + Spring Boot Test

## 项目结构

```
filter-interceptor-demo/
├── pom.xml
├── README.md
├── metadata.json
└── src/main/java/com/example/demo/
    ├── FilterInterceptorApplication.java       # 启动类
    ├── config/
    │   └── WebConfig.java                      # Web 配置（注册 Filter 和 Interceptor）
    ├── controller/
    │   └── DemoController.java                 # 演示 Controller
    ├── filter/
    │   └── LoggingFilter.java                  # 日志过滤器
    └── interceptor/
        └── AuthInterceptor.java                # 认证拦截器
```

## 快速开始

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 编译项目
mvn clean package

# 运行项目
mvn spring-boot:run

# 运行测试
mvn test
```

应用启动后访问 `http://localhost:8080`

## Filter 详解

### Filter 是什么？

Filter 是 Servlet 规范中的组件，运行在 Servlet 容器层面（Tomcat），在请求到达 DispatcherServlet 之前和响应离开 DispatcherServlet 之后执行。

### Filter 生命周期

```java
public interface Filter {
    void init(FilterConfig filterConfig);          // 初始化（仅执行一次）
    void doFilter(ServletRequest, ServletResponse, FilterChain);  // 每次请求执行
    void destroy();                                 // 销毁（仅执行一次）
}
```

| 阶段 | 方法 | 说明 |
|------|------|------|
| 初始化 | `init()` | Filter 实例化时调用，可加载配置资源 |
| 过滤 | `doFilter()` | 每个请求/响应经过时调用 |
| 销毁 | `destroy()` | Filter 被移除时调用，可释放资源 |

### LoggingFilter 示例

本项目的 `LoggingFilter` 记录每个请求的耗时：

```java
public class LoggingFilter implements Filter {

    @Override
    public void init(FilterConfig filterConfig) {
        // Filter 初始化逻辑
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        long start = System.currentTimeMillis();

        System.out.println("[Filter] 请求开始: " + httpRequest.getMethod() + " " + httpRequest.getRequestURI());

        chain.doFilter(request, response);

        long duration = System.currentTimeMillis() - start;
        System.out.println("[Filter] 请求完成: " + httpRequest.getRequestURI() + " 耗时: " + duration + "ms");
    }

    @Override
    public void destroy() {
        // Filter 销毁逻辑
    }
}
```

### Filter 注册方式

**方式一：FilterRegistrationBean（推荐）**

```java
@Bean
public FilterRegistrationBean<LoggingFilter> loggingFilter() {
    FilterRegistrationBean<LoggingFilter> registration = new FilterRegistrationBean<>();
    registration.setFilter(new LoggingFilter());
    registration.addUrlPatterns("/api/*");
    registration.setOrder(1);
    return registration;
}
```

**方式二：@Component + @Order**

```java
@Component
@Order(1)
public class LoggingFilter implements Filter {
    // ...
}
```

> 注意：使用 `@Component` 方式时，Filter 默认拦截所有请求 (`/*`)，无法精确控制 URL 匹配模式。

### Filter 执行顺序

- `FilterRegistrationBean` 通过 `setOrder()` 控制顺序，数值越小优先级越高
- `@Component` + `@Order` 注解控制顺序
- 多个 Filter 按照 Order 值从小到大依次执行

## HandlerInterceptor 详解

### HandlerInterceptor 是什么？

HandlerInterceptor 是 Spring MVC 框架中的组件，运行在 DispatcherServlet 内部，可以在 Controller 方法执行前后以及请求完成后进行拦截处理。

### 三个回调方法

```java
public interface HandlerInterceptor {
    boolean preHandle(HttpServletRequest, HttpServletResponse, Object handler);
    void postHandle(HttpServletRequest, HttpServletResponse, Object handler, ModelAndView);
    void afterCompletion(HttpServletRequest, HttpServletResponse, Object handler, Exception);
}
```

| 方法 | 执行时机 | 返回值 | 用途 |
|------|----------|--------|------|
| `preHandle` | Controller 执行前 | boolean | 权限校验、登录检查 |
| `postHandle` | Controller 执行后，视图渲染前 | void | 修改 ModelAndView |
| `afterCompletion` | 请求完成后（视图渲染后） | void | 资源清理、异常日志 |

### AuthInterceptor 示例

本项目的 `AuthInterceptor` 演示认证检查和请求日志：

```java
@Component
public class AuthInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        String uri = request.getRequestURI();
        System.out.println("[Interceptor] preHandle: " + uri);
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) {
        System.out.println("[Interceptor] postHandle: " + request.getRequestURI());
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {
        System.out.println("[Interceptor] afterCompletion: " + request.getRequestURI());
    }
}
```

## Filter vs Interceptor 对比

| 特性 | Filter | HandlerInterceptor |
|------|--------|-------------------|
| 规范 | Servlet 规范 | Spring MVC 框架 |
| 作用范围 | 所有请求（包括静态资源） | 仅 Spring MVC 处理的请求 |
| 执行时机 | DispatcherServlet 前后 | Controller 前后 |
| 获取 Controller 信息 | 否 | 是（handler 参数） |
| 获取 Handler 方法名 | 否 | 是（可转换为 HandlerMethod） |
| 注入 Spring Bean | 需额外配置 | 直接 @Component |
| 拦截所有请求 | 默认 /* | 需配置 addPathPatterns |
| 典型场景 | 编码、压缩、CORS | 认证、日志、权限 |

### 选择原则

- **用 Filter 的场景**：字符编码设置、GZIP 压缩、CORS 跨域、XSS 防护
- **用 Interceptor 的场景**：用户认证、权限检查、操作日志、性能监控

## 注册与配置

### WebConfig 配置类

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Autowired
    private AuthInterceptor authInterceptor;

    @Bean
    public FilterRegistrationBean<LoggingFilter> loggingFilter() {
        FilterRegistrationBean<LoggingFilter> registration = new FilterRegistrationBean<>();
        registration.setFilter(new LoggingFilter());
        registration.addUrlPatterns("/api/*");
        registration.setOrder(1);
        return registration;
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(authInterceptor)
                .addPathPatterns("/api/**")
                .excludePathPatterns("/api/public/**");
    }
}
```

### Interceptor 路径匹配

| 模式 | 说明 | 示例 |
|------|------|------|
| `/api/**` | 匹配 /api 下所有路径 | `/api/users`, `/api/users/1` |
| `/api/*` | 匹配 /api 下单层路径 | `/api/users`，不匹配 `/api/users/1` |
| `/**` | 匹配所有路径 | 任何路径 |

## 执行顺序

当请求到达时，完整的执行顺序为：

```
1.  LoggingFilter.doFilter() - 请求前处理
2.  AuthInterceptor.preHandle()
3.  Controller 方法执行
4.  AuthInterceptor.postHandle()
5.  AuthInterceptor.afterCompletion()
6.  LoggingFilter.doFilter() - 响应后处理
```

控制台输出示例：

```
[Filter] 请求开始: GET /api/hello
[Interceptor] preHandle: /api/hello
[Interceptor] postHandle: /api/hello
[Interceptor] afterCompletion: /api/hello
[Filter] 请求完成: /api/hello 耗时: 15ms
```

## 测试接口

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 基本接口
curl http://localhost:8080/api/hello

# 带路径参数
curl http://localhost:8080/api/hello/world

# 查看控制台日志输出，观察 Filter 和 Interceptor 的执行顺序
```

## 实战场景

### 场景一：请求耗时统计（Filter）

```java
public class TimingFilter implements Filter {
    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain) throws IOException, ServletException {
        long start = System.currentTimeMillis();
        chain.doFilter(req, res);
        long elapsed = System.currentTimeMillis() - start;
        System.out.println("Request took " + elapsed + "ms");
    }
}
```

### 场景二：Token 认证（Interceptor）

```java
@Override
public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
    String token = request.getHeader("Authorization");
    if (token == null || !token.startsWith("Bearer ")) {
        response.setStatus(401);
        response.getWriter().write("Unauthorized");
        return false;
    }
    return true;
}
```

### 场景三：多 Filter 链式处理

```
Request → EncodingFilter → CorsFilter → AuthFilter → Interceptor → Controller
```

## 最佳实践

1. **Filter 处理通用逻辑**：编码、CORS、XSS 等与框架无关的通用逻辑放在 Filter
2. **Interceptor 处理业务逻辑**：认证、授权、日志等与业务相关的逻辑放在 Interceptor
3. **注意执行顺序**：Filter 的 Order 值和 Interceptor 的注册顺序都会影响执行
4. **避免重复处理**：Filter 和 Interceptor 不要对同一功能重复处理
5. **合理排除路径**：使用 `excludePathPatterns()` 排除不需要拦截的路径
6. **Filter 中注入 Bean**：通过 `FilterRegistrationBean` 设置 Spring 管理的 Filter 实例

## 常见问题

### Q: Filter 中如何注入 Spring Bean？

使用 `FilterRegistrationBean` 并传入 Spring 管理的 Filter 实例，而非直接 `new`：
```java
@Bean
public FilterRegistrationBean<MyFilter> myFilter(MyFilter filter) {
    FilterRegistrationBean<MyFilter> reg = new FilterRegistrationBean<>(filter);
    reg.addUrlPatterns("/api/*");
    return reg;
}
```

### Q: Interceptor 的 preHandle 返回 false 会怎样？

请求被中断，后续的 Interceptor 和 Controller 都不会执行，直接返回响应。

### Q: 如何让 Filter 只对特定路径生效？

使用 `FilterRegistrationBean.addUrlPatterns()` 精确控制匹配路径。

### Q: 异步请求中 Filter 和 Interceptor 的行为？

- Filter 通过 `AsyncContext` 可以处理异步请求
- Interceptor 有对应的异步版本 `AsyncHandlerInterceptor`（`afterConcurrentHandlingStarted`）

## 扩展阅读

- [Spring Boot Filters 官方文档](https://docs.spring.io/spring-boot/docs/current/reference/html/web.html#web.servlet.embedded-container.servlets-filters-listeners)
- [Spring MVC Interceptor 文档](https://docs.spring.io/spring-framework/docs/current/reference/html/web.html#mvc-config-interceptors)
- [Servlet Filter 规范](https://docs.oracle.com/javaee/7/tutorial/servlets004.htm)

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
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

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际案例替换
./scripts/demo.sh
```
