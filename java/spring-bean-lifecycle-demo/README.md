# Spring Bean 生命周期演示

> 深入理解Spring Bean从实例化到销毁的完整生命周期

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解Bean生命周期的12个阶段
- ✅ 掌握各种生命周期回调方式（注解、接口、自定义方法）
- ✅ 理解BeanPostProcessor的作用和使用
- ✅ 理解Aware接口的作用
- ✅ 掌握Bean的初始化和销毁配置

---

## 📚 Bean生命周期概览

```
┌─────────────────────────────────────────────────────────────────┐
│                     Spring Bean 生命周期                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [1] 构造器实例化                                                  │
│       ↓                                                         │
│  [2] 属性赋值（依赖注入）                                           │
│       ↓                                                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Aware接口回调                                             │  │
│  │  • BeanNameAware.setBeanName()                            │  │
│  │  • BeanFactoryAware.setBeanFactory()                      │  │
│  │  • ApplicationContextAware.setApplicationContext()        │  │
│  └──────────────────────────────────────────────────────────┘  │
│       ↓                                                         │
│  [3] BeanPostProcessor.postProcessBeforeInitialization()         │
│       ↓                                                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  初始化回调                                                │  │
│  │  • @PostConstruct                                         │  │
│  │  • InitializingBean.afterPropertiesSet()                  │  │
│  │  • 自定义init-method                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│       ↓                                                         │
│  [4] BeanPostProcessor.postProcessAfterInitialization()          │
│       ↓                                                         │
│  [5] Bean就绪使用                                                │
│       ↓                                                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  销毁回调                                                  │  │
│  │  • @PreDestroy                                            │  │
│  │  • DisposableBean.destroy()                               │  │
│  │  • 自定义destroy-method                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ 环境准备

### 要求

- JDK 11+
- Maven 3.6+
- Spring Framework 5.3+

### 运行

```bash
mvn clean compile
mvn exec:java -Dexec.mainClass="com.example.demo.Application"
```

---

## 💻 核心代码

### Bean生命周期演示类

```java
@Component
public class LifecycleBean implements 
        BeanNameAware,
        BeanFactoryAware,
        ApplicationContextAware,
        InitializingBean,
        DisposableBean {
    
    // 1. 构造器
    public LifecycleBean() {
        System.out.println("[1] 构造器");
    }
    
    // 2. Aware接口
    @Override
    public void setBeanName(String name) {
        System.out.println("[2] BeanNameAware");
    }
    
    // 3. BeanPostProcessor前置处理
    
    // 4. 初始化
    @PostConstruct
    public void postConstruct() {
        System.out.println("[4] @PostConstruct");
    }
    
    @Override
    public void afterPropertiesSet() {
        System.out.println("[5] InitializingBean");
    }
    
    public void customInit() {
        System.out.println("[6] 自定义init-method");
    }
    
    // 5. BeanPostProcessor后置处理
    
    // 6. 销毁
    @PreDestroy
    public void preDestroy() {
        System.out.println("[7] @PreDestroy");
    }
    
    @Override
    public void destroy() {
        System.out.println("[8] DisposableBean");
    }
    
    public void customDestroy() {
        System.out.println("[9] 自定义destroy-method");
    }
}
```

### BeanPostProcessor

```java
@Component
public class CustomBeanPostProcessor implements BeanPostProcessor {
    
    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) {
        // 初始化前处理
        return bean;
    }
    
    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) {
        // 初始化后处理（如AOP代理）
        return bean;
    }
}
```

---

## 🔍 三种初始化/销毁方式对比

| 方式 | 注解/接口 | 优先级 | 推荐使用 |
|------|----------|--------|----------|
| JSR-250 | `@PostConstruct` / `@PreDestroy` | 1 | ✅ 推荐 |
| Spring接口 | `InitializingBean` / `DisposableBean` | 2 | ⚠️ 侵入性强 |
| 自定义方法 | `init-method` / `destroy-method` | 3 | ✅ 推荐 |

**优先级顺序**: @PostConstruct > InitializingBean > init-method

---

## ❓ 常见问题

### Q: 为什么初始化回调有多种方式？
**A**: 
- `@PostConstruct`: 标准注解，与Spring解耦
- `InitializingBean`: Spring早期方式，侵入性较强
- `init-method`: XML时代的遗留，配置灵活

### Q: BeanPostProcessor有什么用？
**A**: 
- AOP代理创建
- 属性校验和修改
- 统一处理所有Bean

### Q: 单例Bean和原型Bean生命周期有何不同？
**A**: 
- 单例: 容器启动时创建，容器关闭时销毁
- 原型: 每次获取时创建，Spring不管理销毁

---

## 📚 扩展学习

- [Spring Core IoC](../spring-core-ioc-demo/)
- [Spring AOP](../spring-aop-demo/)

---

*最后更新：2026年4月*
