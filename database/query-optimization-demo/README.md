# SQL 查询优化演示 - 从慢查询到高性能

> 使用 MySQL 演示如何识别慢查询、分析执行计划、创建合适的索引，将查询性能从秒级优化到毫秒级。

---

## 📋 目录

- [🎯 学习目标](#-学习目标)
- [📐 架构图](#-架构图)
- [🚀 快速开始](#-快速开始)
- [📖 核心概念](#-核心概念)
- [💻 代码示例](#-代码示例)
- [🔧 配置说明](#-配置说明)
- [🧪 验证测试](#-验证测试)
- [📊 运行结果](#-运行结果)
- [🐛 常见问题](#-常见问题)
- [📚 扩展学习](#-扩展学习)

---

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 使用 EXPLAIN 分析 SQL 执行计划
- ✅ 识别全表扫描、索引失效等性能问题
- ✅ 设计复合索引和覆盖索引
- ✅ 使用慢查询日志定位问题 SQL

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    SQL 查询优化流程                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   慢查询日志 ──▶ EXPLAIN 分析 ──▶ 索引优化 ──▶ 性能验证        │
│                                                                 │
│        │              │              │              │          │
│        ▼              ▼              ▼              ▼          │
│   定位问题 SQL    查看扫描方式    创建合适索引    对比执行时间   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

```bash
cd database/query-optimization-demo
./scripts/start.sh
sleep 20
./scripts/check.sh
```

---

## 📖 核心概念

### 1. EXPLAIN 输出字段

| 字段 | 含义 |
|------|------|
| id | 查询标识符 |
| select_type | 查询类型 |
| table | 访问的表 |
| type | 访问类型（system > const > eq_ref > ref > range > index > ALL） |
| possible_keys | 可能使用的索引 |
| key | 实际使用的索引 |
| rows | 扫描行数估算 |
| Extra | 额外信息（Using index, Using where, Using filesort 等） |

### 2. 索引优化原则

- 选择性高的列优先
- 最左前缀原则
- 避免冗余索引
- 利用覆盖索引减少回表

### 3. 慢查询日志

```sql
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;
```

---

## 💻 代码示例

### 创建测试表和数据

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50),
    email VARCHAR(100),
    created_at DATETIME,
    INDEX idx_username (username)
);

INSERT INTO users (username, email, created_at) VALUES
('alice', 'alice@example.com', '2026-01-01'),
('bob', 'bob@example.com', '2026-02-01'),
('charlie', 'charlie@example.com', '2026-03-01');
```

### 全表扫描示例

```sql
EXPLAIN SELECT * FROM users WHERE email = 'alice@example.com';
-- type: ALL（全表扫描）
```

### 添加索引后

```sql
ALTER TABLE users ADD INDEX idx_email (email);

EXPLAIN SELECT * FROM users WHERE email = 'alice@example.com';
-- type: ref（使用索引）
```

### 复合索引

```sql
ALTER TABLE users ADD INDEX idx_created_username (created_at, username);

-- 符合最左前缀
EXPLAIN SELECT * FROM users WHERE created_at > '2026-01-01' AND username = 'alice';
```

---

## 🧪 验证测试

```bash
# 连接 MySQL
mysql -h127.0.0.1 -uroot -prootpass demo < sql/init.sql

# 分析查询
mysql -h127.0.0.1 -uroot -prootpass demo -e "EXPLAIN SELECT * FROM users WHERE email='alice@example.com'"
```

---

## 📚 扩展学习

- [索引设计](../index-design-demo/)
- [慢查询分析](../slow-query-analysis-demo/)
- [MySQL EXPLAIN 文档](https://dev.mysql.com/doc/refman/8.0/en/explain-output.html)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
