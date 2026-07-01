<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Spring Data JPA 数据持久化演示

> 简化数据访问层，让数据库操作更高效

## 🎯 学习目标

- ✅ 理解Spring Data JPA的核心概念
- ✅ 掌握Repository接口的定义和使用
- ✅ 学会方法名解析查询
- ✅ 掌握自定义JPQL和原生SQL
- ✅ 理解分页和排序
- ✅ 掌握事务管理

---

## 📚 核心概念

### 什么是Spring Data JPA？

Spring Data JPA是Spring Data项目的一部分，它简化了基于JPA的数据访问层实现。

**核心优势**:
- 无需实现类，只需定义接口
- 方法名自动解析为查询
- 支持自定义JPQL和SQL
- 内置分页、排序、事务

### 架构层次

```
┌─────────────────────────────────────┐
│         Service Layer               │
├─────────────────────────────────────┤
│         Repository Layer            │
│   (Spring Data JPA自动生成实现)      │
├─────────────────────────────────────┤
│         JPA / Hibernate             │
├─────────────────────────────────────┤
│         Database                    │
└─────────────────────────────────────┘
```

---

## 💻 核心代码

### 1. 定义实体

```java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String username;
    
    @Column(nullable = false)
    private String email;
}
```

### 2. 定义Repository

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    // 方法名解析查询
    Optional<User> findByUsername(String username);
    
    List<User> findByAgeBetween(int minAge, int maxAge);
    
    // 自定义JPQL
    @Query("SELECT u FROM User u WHERE u.age >= :minAge")
    List<User> findAdultUsers(@Param("minAge") int minAge);
    
    // 原生SQL
    @Query(value = "SELECT * FROM users WHERE age > ?1", nativeQuery = true)
    List<User> findUsersOlderThan(int age);
}
```

### 3. 使用Service

```java
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    
    public User createUser(User user) {
        return userRepository.save(user);
    }
    
    public List<User> findAll() {
        return userRepository.findAll();
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

## 🔍 查询方法命名规则

| 关键字 | 示例 | JPQL |
|--------|------|------|
| And | findByAgeAndName | where u.age = ?1 and u.name = ?2 |
| Or | findByAgeOrName | where u.age = ?1 or u.name = ?2 |
| Between | findByAgeBetween | where u.age between ?1 and ?2 |
| Like | findByNameLike | where u.name like ?1 |
| GreaterThan | findByAgeGreaterThan | where u.age > ?1 |
| OrderBy | findByNameOrderByAgeDesc | order by u.age desc |

---

## 📚 扩展学习

- [Spring Core IoC](../spring-core-ioc-demo/)
- [Spring Bean生命周期](../spring-bean-lifecycle-demo/)
- [Spring AOP](../spring-aop-demo/)

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
