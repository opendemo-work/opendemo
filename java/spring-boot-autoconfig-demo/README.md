# Spring Boot 自动配置原理演示

> 理解Spring Boot"约定大于配置"的核心机制

## 🎯 学习目标

- ✅ 理解自动配置的原理
- ✅ 掌握@Conditional条件注解
- ✅ 了解Starter机制
- ✅ 学会自定义自动配置

---

## 📚 核心概念

### 自动配置流程

```
1. 读取 META-INF/spring.factories
2. 加载所有自动配置类
3. 根据@Conditional条件判断
4. 满足条件的配置生效
5. 创建Bean并加入容器
```

### 常用条件注解

| 注解 | 说明 |
|------|------|
| @ConditionalOnClass | 类存在时生效 |
| @ConditionalOnMissingBean | Bean不存在时生效 |
| @ConditionalOnProperty | 配置属性满足时生效 |

---

## 💻 核心代码

### 自动配置类

```java
@Configuration
@ConditionalOnClass(GreetingService.class)
@EnableConfigurationProperties(GreetingProperties.class)
public class GreetingAutoConfiguration {
    
    @Bean
    @ConditionalOnMissingBean
    public GreetingService greetingService() {
        return new SimpleGreetingService();
    }
}
```

### 配置文件

```properties
# META-INF/spring.factories
org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
com.example.demo.config.GreetingAutoConfiguration
```

---

## 🚀 运行

```bash
mvn clean compile
mvn exec:java -Dexec.mainClass="com.example.demo.Application"
```

---

*最后更新：2026年4月*
