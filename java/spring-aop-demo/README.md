# Spring AOP 面向切面编程演示

> 深入理解Spring AOP的核心概念和5种通知类型

## 🎯 学习目标

- ✅ 理解AOP的核心概念（切面、连接点、切点、通知）
- ✅ 掌握5种Advice类型（Before/AfterReturning/AfterThrowing/After/Around）
- ✅ 理解切点表达式（Pointcut Expression）
- ✅ 了解JDK动态代理和CGLIB代理的区别

---

## 📚 AOP核心概念

| 概念 | 说明 |
|------|------|
| **Aspect** | 切面，横切关注点的模块化 |
| **JoinPoint** | 连接点，程序执行过程中的点（如方法调用） |
| **Pointcut** | 切点，匹配连接点的表达式 |
| **Advice** | 通知，在切点处执行的增强代码 |
| **Target** | 目标对象，被代理的对象 |
| **Proxy** | 代理对象，AOP框架生成的对象 |

---

## 🛠️ 5种Advice类型

```
┌─────────────────────────────────────────────────────────────────┐
│                      Advice执行顺序                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   @Around (前置)                                                │
│        ↓                                                        │
│   @Before                                                       │
│        ↓                                                        │
│   ┌─────────────────┐                                          │
│   │   目标方法       │                                          │
│   └─────────────────┘                                          │
│        ↓                                                        │
│   @Around (后置)                                                │
│        ↓                                                        │
│   @AfterReturning (成功) 或 @AfterThrowing (异常)                │
│        ↓                                                        │
│   @After (最终)                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💻 核心代码

### 切面定义

```java
@Aspect
@Component
public class LoggingAspect {
    
    // 切点表达式
    @Pointcut("execution(* com.example.demo.service.*.*(..))")
    public void servicePointcut() {}
    
    @Before("servicePointcut()")
    public void before(JoinPoint jp) {
        // 方法执行前
    }
    
    @AfterReturning(pointcut = "servicePointcut()", returning = "result")
    public void afterReturning(Object result) {
        // 方法成功返回后
    }
    
    @Around("servicePointcut()")
    public Object around(ProceedingJoinPoint pjp) throws Throwable {
        // 环绕通知
        long start = System.currentTimeMillis();
        Object result = pjp.proceed(); // 执行目标方法
        long end = System.currentTimeMillis();
        return result;
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

## 📚 扩展学习

- [Spring Core IoC](../spring-core-ioc-demo/)
- [Spring Bean生命周期](../spring-bean-lifecycle-demo/)

---

*最后更新：2026年4月*
