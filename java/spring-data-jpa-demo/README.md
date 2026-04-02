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
