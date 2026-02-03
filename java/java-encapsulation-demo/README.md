# Java封装原则完整示例

## 🎯 案例概述

这是一个全面展示Java封装原则的完整示例，通过银行账户、不可变对象、验证工具、配置管理等多个场景演示数据隐藏、访问控制、信息封装等核心面向对象设计原则。

## 📚 学习目标

通过本示例你将掌握：
- 数据隐藏和访问控制的实现
- 不可变对象的设计和应用
- 验证逻辑的封装和复用
- 配置管理的安全实现
- 线程安全的封装设计
- 构建器模式和单例模式的应用

## 🔧 核心知识点

### 1. 基本封装原则
- `private`成员变量实现数据隐藏
- `public`方法提供受控访问
- 参数验证和业务规则封装
- 同步方法保证线程安全

### 2. 不可变对象设计
- `final`字段确保不可变性
- 防御性拷贝防止外部修改
- 构建器模式简化对象创建
- with方法支持安全修改

### 3. 验证逻辑封装
- 静态工具方法集中管理
- 正则表达式预编译优化
- 综合验证结果封装
- 验证失败的优雅处理

### 4. 配置管理封装
- 单例模式确保全局唯一
- 多来源配置加载（文件、环境、系统）
- 线程安全的配置访问
- 配置验证和默认值处理

## 🚀 运行示例

```bash
# 编译项目
mvn compile

# 运行主程序
mvn exec:java -Dexec.mainClass="com.opendemo.java.encapsulation.EncapsulationDemo"

# 运行测试
mvn test
```

## 📖 代码详解

### 主要类结构

```java
// 基本封装示例
BankAccount - 银行账户类，演示数据隐藏和访问控制

// 不可变对象示例  
ImmutablePerson - 不可变人类，演示不可变设计模式
├── Address - 内部不可变地址类
└── Builder - 构建器类

// 验证工具示例
ValidationUtils - 验证工具类，演示静态方法封装
└── ValidationResult - 验证结果封装类

// 配置管理示例
Configuration - 配置管理类，演示单例和线程安全
├── ConfigListener - 配置监听器接口
└── Builder - 配置构建器类
```

### 关键技术点演示

#### 1. 数据隐藏实现
```java
public class BankAccount {
    private String accountNumber;     // 私有字段
    private BigDecimal balance;       // 私有字段
    private AccountStatus status;     // 私有字段
    
    public String getAccountNumber() {  // 受控访问
        return "****" + accountNumber.substring(accountNumber.length() - 4);
    }
    
    public synchronized boolean deposit(BigDecimal amount) {  // 同步方法
        // 参数验证和业务逻辑封装
    }
}
```

#### 2. 不可变对象设计
```java
public final class ImmutablePerson {
    private final String name;        // final字段
    private final List<String> hobbies; // 不可变集合
    
    private ImmutablePerson(Builder builder) {
        // 防御性拷贝
        this.hobbies = Collections.unmodifiableList(new ArrayList<>(builder.hobbies));
    }
    
    public List<String> getHobbies() {
        // 返回拷贝，防止外部修改
        return new ArrayList<>(hobbies);
    }
}
```

#### 3. 验证逻辑封装
```java
public class ValidationUtils {
    private static final Pattern EMAIL_PATTERN = Pattern.compile("...");
    
    public static boolean isValidEmail(String email) {
        if (email == null || email.trim().isEmpty()) {
            return false;
        }
        return EMAIL_PATTERN.matcher(email.trim()).matches();
    }
    
    public static ValidationResult validatePersonInfo(...) {
        // 综合多项验证
    }
}
```

#### 4. 配置管理封装
```java
public class Configuration {
    private static volatile Configuration instance;  // volatile保证可见性
    private final Map<String, String> configMap;     // 线程安全集合
    
    public static Configuration getInstance() {
        // 双重检查锁定单例
    }
    
    public synchronized void setProperty(String key, String value) {
        // 同步方法保证线程安全
    }
}
```

## 🧪 测试覆盖

测试类 `EncapsulationDemoTest` 包含以下测试：

✅ 银行账户封装测试  
✅ 银行账户验证测试  
✅ 不可变对象测试  
✅ 验证工具类测试  
✅ 配置管理测试  
✅ 线程安全性测试  
✅ 工具类实例化防护测试  
✅ Address不可变性测试  

## 🎯 实际应用场景

### 1. 金融系统封装
```java
// 银行账户的安全封装
public class SecureBankAccount {
    private final String encryptedAccountNumber;
    private volatile BigDecimal balance;
    
    public synchronized boolean transfer(SecureBankAccount target, BigDecimal amount) {
        // 安全的资金转移操作
    }
}
```

### 2. 配置管理系统
```java
// 应用配置的安全管理
public class AppConfig {
    private static final Configuration config = Configuration.getInstance();
    
    public static String getDatabaseUrl() {
        return config.getProperty("database.url", "jdbc:h2:mem:test");
    }
    
    public static int getConnectionTimeout() {
        return config.getIntProperty("database.timeout", 30000);
    }
}
```

### 3. 数据验证框架
```java
// 业务数据验证封装
public class BusinessValidator {
    public static ValidationResult validateUserRegistration(UserRegistrationDto dto) {
        return ValidationUtils.validatePersonInfo(
            dto.getName(), 
            dto.getEmail(), 
            dto.getPhone(), 
            dto.getAge()
        );
    }
}
```

### 4. 不可变值对象
```java
// 领域驱动设计中的值对象
public final class Money {
    private final BigDecimal amount;
    private final Currency currency;
    
    public Money add(Money other) {
        // 返回新的Money对象而不是修改当前对象
    }
}
```

## ⚡ 最佳实践建议

### 1. 封装设计原则
- ✅ 尽可能使用private访问修饰符
- ✅ 提供必要的getter/setter方法
- ✅ 在setter中加入数据验证逻辑
- ✅ 使用final修饰不可变字段

### 2. 线程安全考虑
- ✅ 对共享可变状态使用同步
- ✅ 优先考虑不可变对象
- ✅ 使用线程安全的集合类
- ✅ 合理使用volatile关键字

### 3. 验证和错误处理
- ✅ 参数验证应该尽早进行
- ✅ 提供清晰的错误信息
- ✅ 使用专门的验证结果类
- ✅ 避免在验证中抛出异常

## 🔍 常见陷阱和解决方案

### 1. 不完全的封装
```java
// 问题：返回可修改的内部集合
public List<String> getHobbies() {
    return hobbies;  // 外部可以直接修改内部状态
}

// 解决：返回防御性拷贝
public List<String> getHobbies() {
    return new ArrayList<>(hobbies);
}
```

### 2. 线程安全问题
```java
// 问题：非线程安全的检查后执行模式
if (balance.compareTo(amount) >= 0) {
    balance = balance.subtract(amount);  // 可能出现竞态条件
}

// 解决：使用同步块
public synchronized boolean withdraw(BigDecimal amount) {
    if (balance.compareTo(amount) >= 0) {
        balance = balance.subtract(amount);
        return true;
    }
    return false;
}
```

### 3. 单例模式的线程安全
```java
// 问题：非线程安全的懒加载单例
public static Configuration getInstance() {
    if (instance == null) {
        instance = new Configuration();  // 可能创建多个实例
    }
    return instance;
}

// 解决：双重检查锁定
public static Configuration getInstance() {
    if (instance == null) {
        synchronized (Configuration.class) {
            if (instance == null) {
                instance = new Configuration();
            }
        }
    }
    return instance;
}
```

## 📊 性能考虑

### 1. 不可变对象的权衡
- 优点：线程安全、简化调试、缓存友好
- 缺点：频繁创建新对象可能影响性能
- 建议：对于频繁修改的对象谨慎使用

### 2. 同步的性能影响
- 同步方法会降低并发性能
- 考虑使用更细粒度的锁
- 对于读多写少的场景考虑读写锁

## 📚 扩展学习资源

### 官方文档
- [Java封装教程](https://docs.oracle.com/javase/tutorial/java/javaOO/accesscontrol.html)
- [不可变对象指南](https://docs.oracle.com/javase/tutorial/essential/concurrency/immut.html)

### 推荐书籍
- 《Effective Java》- Joshua Bloch
- 《Java并发编程实战》- Brian Goetz
- 《领域驱动设计》- Eric Evans

### 相关设计模式
- 单例模式
- 构建器模式
- 值对象模式
- 防御性编程

## 🔄 版本历史

- v1.0.0 (2024-01-15): 初始版本，包含完整的封装原则演示

---
**注意**: 良好的封装是软件设计的基础，它不仅能提高代码安全性，还能增强代码的可维护性和可扩展性。