# AOP 日志切面演示

> 深入理解 Spring AOP 的日志切面、性能监控和自定义注解

## 🎯 学习目标

- ✅ 掌握 @Around、@Before、@AfterReturning 等通知类型
- ✅ 学会创建自定义注解 @Loggable
- ✅ 理解 AOP 在日志记录和性能监控中的应用
- ✅ 掌握切点表达式的编写

---

## 📚 AOP 核心概念

| 概念 | 说明 |
|------|------|
| **Aspect** | 切面，横切关注点的模块化（如日志、事务） |
| **JoinPoint** | 连接点，方法调用、异常抛出等执行点 |
| **Pointcut** | 切点表达式，匹配需要增强的方法 |
| **Advice** | 通知，在切点处执行的增强逻辑 |
| **Target** | 目标对象，被 AOP 代理的原始对象 |
| **Weaving** | 织入，将切面应用到目标对象的过程 |

---

## 🛠️ 五种通知类型

```
┌──────────────────────────────────────────────┐
│              通知执行顺序                      │
├──────────────────────────────────────────────┤
│  @Around (前置部分)                           │
│       ↓                                      │
│  @Before                                      │
│       ↓                                      │
│  ┌──────────────┐                            │
│  │  目标方法     │                            │
│  └──────────────┘                            │
│       ↓                                      │
│  @Around (后置部分)                           │
│       ↓                                      │
│  @AfterReturning 或 @AfterThrowing            │
│       ↓                                      │
│  @After                                       │
└──────────────────────────────────────────────┘
```

---

## 💻 核心代码

### 1. 自定义注解 @Loggable

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Loggable {
    String value() default "";
    boolean logParams() default true;
    boolean logResult() default true;
    boolean logExecutionTime() default true;
}
```

### 2. 日志切面 LoggingAspect

```java
@Aspect
@Component
public class LoggingAspect {

    @Around("@annotation(loggable)")
    public Object logMethod(ProceedingJoinPoint joinPoint, Loggable loggable) throws Throwable {
        Logger logger = LoggerFactory.getLogger(joinPoint.getTarget().getClass());
        String description = loggable.value().isEmpty()
            ? joinPoint.getSignature().getName() : loggable.value();

        if (loggable.logParams()) {
            logger.info("[{}] 开始执行, 参数: {}", description, Arrays.toString(joinPoint.getArgs()));
        }

        long startTime = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        long elapsedTime = System.currentTimeMillis() - startTime;

        if (loggable.logResult()) {
            logger.info("[{}] 执行成功, 返回值: {}", description, result);
        }
        if (loggable.logExecutionTime()) {
            logger.info("[{}] 执行耗时: {}ms", description, elapsedTime);
        }
        return result;
    }
}
```

### 3. 性能监控切面 PerformanceMonitorAspect

```java
@Aspect
@Component
public class PerformanceMonitorAspect {

    private final Map<String, AtomicLong> methodCallCount = new ConcurrentHashMap<>();
    private final Map<String, AtomicLong> methodTotalTime = new ConcurrentHashMap<>();

    @Around("execution(* com.example.demo.service.*.*(..))")
    public Object monitorPerformance(ProceedingJoinPoint joinPoint) throws Throwable {
        StopWatch stopWatch = new StopWatch();
        stopWatch.start();
        Object result = joinPoint.proceed();
        stopWatch.stop();
        recordMetrics(joinPoint.getSignature().toShortString(), stopWatch.getTotalTimeMillis());
        return result;
    }
}
```

### 4. 使用 @Loggable 注解

```java
@Service
public class UserService {

    @Loggable(value = "查询用户", logParams = true, logResult = true)
    public String findById(Long id) {
        return userStore.get(id);
    }

    @Loggable(value = "创建用户")
    public String createUser(Long id, String name) {
        userStore.put(id, name);
        return "用户创建成功: " + name;
    }
}
```

---

## 🚀 快速开始

### 1. 启动应用

```bash
cd java/aop-logging-demo
mvn spring-boot:run
```

### 2. 观察日志输出

启动后应用会自动执行演示方法，控制台将输出：

```
[查询用户] 开始执行, 参数: [1]
[查询用户] 执行成功, 返回值: 张三
[查询用户] 执行耗时: 45ms
调用服务方法: findById
服务方法 findById 执行完成, 耗时: 46ms
[性能监控] 方法: UserService.findById(..), 调用次数: 1, 平均耗时: 46.00ms
```

---

## 📁 项目结构

```
aop-logging-demo/
├── src/main/java/com/example/demo/
│   ├── AopLoggingApplication.java              # 应用入口
│   ├── annotation/
│   │   └── Loggable.java                       # 自定义日志注解
│   ├── aspect/
│   │   ├── LoggingAspect.java                  # 日志切面
│   │   └── PerformanceMonitorAspect.java       # 性能监控切面
│   └── service/
│       └── UserService.java                    # 用户服务（演示用）
├── src/test/java/com/example/demo/
│   └── AopLoggingDemoTest.java                 # 单元测试
├── pom.xml
└── README.md
```

---

## 📋 常用切点表达式

| 表达式 | 说明 |
|--------|------|
| `execution(* com.example.service.*.*(..))` | 匹配 service 包下所有方法 |
| `execution(* com.example..*.*(..))` | 匹配 com.example 及子包所有方法 |
| `@annotation(Loggable)` | 匹配带 @Loggable 注解的方法 |
| `within(com.example.service.*)` | 匹配指定包下的所有方法 |
| `bean(userService)` | 匹配指定 Bean 名称的方法 |
| `args(java.lang.Long)` | 匹配参数类型为 Long 的方法 |

---

## 🔧 注意事项

- `@Around` 通知必须调用 `joinPoint.proceed()` 才能执行目标方法
- 切面类必须标注 `@Component` 才能被 Spring 管理
- 切点表达式要精确，避免范围过大影响性能
- 日志切面中避免使用 `System.out.println`，应使用 SLF4J Logger
- 自调用（同一类中方法互调）不会触发 AOP 代理

---

## 🧪 测试

```bash
mvn test
```

---

## 📚 扩展学习

- [Spring AOP Demo](../spring-aop-demo/) - AOP 基础概念
- [Logback Demo](../logback-demo/) - 日志框架配置

---

*最后更新：2026年4月*
