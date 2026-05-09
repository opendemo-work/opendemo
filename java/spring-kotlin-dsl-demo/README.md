# Spring Kotlin DSL 演示

## 学习目标

1. 掌握 Kotlin DSL 定义 Bean
2. 理解函数式 Bean 定义
3. 学会使用 YAML 配置转 Kotlin DSL
4. 掌握类型安全的配置

## 环境要求

- JDK 17+
- Kotlin 1.9+
- Maven 3.9+

## 核心概念

### Bean 定义对比

```java
// Java @Bean 方式
@Bean
fun userRepository(): UserRepository {
    return UserRepository(dataSource)
}

// Kotlin DSL 方式
@Bean
fun userRepository() = bean {
    UserRepository(dataSource())
}
```

## 快速开始

```bash
cd spring-kotlin-dsl-demo
mvn compile kotlin:compile
mvn spring-boot:run
```

## 配置示例

```kotlin
@Configuration
class AppConfiguration {

    @Bean
    fun dataSource() = bean {
        // 类型安全的 DataSource 配置
        dataSource {
            url = "jdbc:h2:mem:testdb"
            username = "sa"
            password = ""
        }
    }
}
```

---

**技术栈**: Spring Boot 3.2 | Kotlin 1.9 | Kotlin DSL

**版本**: 1.0.0