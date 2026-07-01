<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

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


---

## 📚 扩展阅读

### 相关概念

- 概念 1：补充说明
- 概念 2：补充说明
- 概念 3：补充说明

### 常见问题

#### Q1：本案例适用于哪些场景？

**A**：本案例适用于学习、实验和工程参考。

#### Q2：如何验证运行结果？

**A**：按照 README 中的命令执行，并观察输出是否符合预期。

#### Q3：遇到问题时如何排查？

**A**：检查环境依赖是否正确安装，查看命令输出和日志信息。

### 推荐资源

- [OpenDemo 官方文档](https://github.com/opendemo)
- [相关技术官方文档](https://example.com)

### 进阶主题

- [ ] 进阶主题 1
- [ ] 进阶主题 2
- [ ] 进阶主题 3

---

*本 README 为自动生成模板，请根据实际案例内容补充完善。*
