# Spring 声明式事务管理演示

> 理解ACID特性和事务传播行为

## 🎯 学习目标

- ✅ 理解事务的ACID特性
- ✅ 掌握@Transactional注解
- ✅ 理解事务传播行为
- ✅ 了解事务隔离级别
- ✅ 掌握事务回滚机制

---

## 📚 核心概念

### ACID特性

| 特性 | 说明 |
|------|------|
| **A**tomicity | 原子性：要么全部成功，要么全部失败 |
| **C**onsistency | 一致性：数据状态始终保持一致 |
| **I**solation | 隔离性：并发事务互不干扰 |
| **D**urability | 持久性：事务完成后数据永久保存 |

### 传播行为

```java
@Transactional(propagation = Propagation.REQUIRED)      // 默认
@Transactional(propagation = Propagation.REQUIRES_NEW)  // 新建事务
@Transactional(propagation = Propagation.NESTED)        // 嵌套事务
```

---

## 💻 核心代码

```java
@Service
public class BankService {
    
    @Transactional
    public void transfer(String from, String to, BigDecimal amount) {
        // 扣款
        debit(from, amount);
        
        // 收款
        credit(to, amount);
        
        // 异常时自动回滚
    }
    
    @Transactional(readOnly = true)
    public BigDecimal getBalance() {
        // 只读操作
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

*最后更新：2026年4月*
