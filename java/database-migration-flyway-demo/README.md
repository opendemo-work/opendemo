# 数据库迁移 Flyway 演示项目

## 项目简介

本项目是一个基于 Spring Boot 2.7.12 的 Flyway 数据库迁移演示应用，使用 Flyway 管理数据库版本，H2 作为内存数据库。项目展示了数据库迁移的核心概念、Flyway 的配置和使用方法、迁移脚本编写规范以及 CI/CD 集成策略。

## 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Java | 11 | JDK 版本 |
| Spring Boot | 2.7.12 | 应用框架 |
| Flyway | - | 数据库迁移工具 |
| H2 | Runtime | 内存数据库 |
| Maven | - | 构建工具 |

## 数据库迁移概念

### 什么是数据库迁移

数据库迁移（Database Migration）是指对数据库结构进行版本化管理的过程。就像代码使用 Git 进行版本控制一样，数据库迁移工具将数据库的每一次结构变更（DDL）记录为一个迁移脚本，并按照版本顺序依次执行。

### 为什么需要数据库迁移

在没有迁移工具的情况下，数据库管理面临以下问题：

1. **手动执行 SQL 的风险** - 容易遗漏或重复执行 SQL 脚本
2. **环境不一致** - 开发、测试、生产环境的数据库结构可能不同
3. **无法追踪变更** - 不知道数据库经历了哪些变更
4. **团队协作困难** - 多人同时修改数据库结构容易冲突
5. **回滚困难** - 出问题后无法快速回退到之前的版本

### 数据库迁移的工作原理

```
应用启动
   |
   v
Flyway 检查数据库中是否存在 flyway_schema_history 表
   |
   +-- 不存在 --> 创建 flyway_schema_history 表，执行所有迁移脚本
   |
   +-- 已存在 --> 对比已执行和未执行的迁移脚本
                    |
                    +-- 按版本号顺序执行未执行的迁移脚本
                    |
                    +-- 记录执行结果到 flyway_schema_history 表
```

### flyway_schema_history 表

Flyway 会在数据库中自动创建一张 `flyway_schema_history` 表来记录迁移历史：

| 列名 | 说明 |
|------|------|
| installed_rank | 执行顺序 |
| version | 版本号 |
| description | 描述 |
| type | 类型（SQL、JDBC 等） |
| script | 脚本文件名 |
| checksum | 校验和 |
| installed_by | 执行者 |
| installed_on | 执行时间 |
| execution_time | 执行耗时（毫秒） |
| success | 是否成功 |

## Flyway vs Liquibase

### Flyway 简介

Flyway 是一款开源的数据库迁移工具，由 Axel Fontaine 创建。它的核心理念是"简单至上"，使用纯 SQL 脚本作为迁移文件。

### Liquibase 简介

Liquibase 是另一款流行的数据库迁移工具，支持 XML、YAML、JSON 和 SQL 多种格式的迁移文件。

### 详细对比

| 特性 | Flyway | Liquibase |
|------|--------|-----------|
| 学习曲线 | 低 | 中 |
| 迁移文件格式 | SQL | XML/YAML/JSON/SQL |
| 回滚支持 | 付费版 | 免费支持 |
| 条件执行 | 有限 | 强大 |
| 数据库支持 | 广泛 | 广泛 |
| Spring Boot 集成 | 优秀 | 优秀 |
| 社区活跃度 | 高 | 高 |
| 中文支持 | UTF-8 | 支持中文注释 |

### 如何选择

- **选择 Flyway**：团队习惯直接编写 SQL，追求简单高效
- **选择 Liquibase**：需要跨数据库支持，需要回滚功能，需要条件执行

## 迁移脚本版本命名

### Flyway 命名规则

Flyway 的迁移脚本文件名遵循严格的命名规则：

```
V{version}__{description}.sql
```

### 版本号格式

| 格式 | 示例 | 说明 |
|------|------|------|
| 单数字 | V1__Create_table.sql | 简单版本号 |
| 点分数字 | V1.1__Add_column.sql | 次版本 |
| 日期时间 | V20230601120000__Init.sql | 时间戳版本 |
| 下划线分隔 | V1_1_0__Major_release.sql | 多段版本 |

### 命名规则详解

- **前缀 V** - 代表 Versioned migration（版本化迁移）
- **版本号** - 数字、点、下划线组成，按自然顺序排序
- **双下划线** - 分隔版本号和描述
- **描述** - 用下划线分隔单词，描述此次迁移的内容
- **后缀** - 默认 `.sql`

### 特殊类型

| 前缀 | 类型 | 说明 |
|------|------|------|
| V | Versioned | 版本化迁移，只执行一次 |
| R | Repeatable | 可重复执行，每次 checksum 变化时重新执行 |
| U | Undo | 撤销迁移（付费版） |

### 示例

```
db/migration/
├── V1__Create_customer_table.sql
├── V2__Add_email_column.sql
├── V2.1__Add_phone_index.sql
├── V3__Create_order_table.sql
├── V4__Add_customer_status.sql
├── R__Insert_default_data.sql
```

## 本项目的迁移脚本详解

### V1 - 创建客户表

```sql
CREATE TABLE customer (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20)
);
```

初始表结构，包含基本的客户信息。

### V2 - 添加邮箱列

```sql
ALTER TABLE customer ADD COLUMN email VARCHAR(100);
UPDATE customer SET email = CONCAT(LOWER(REPLACE(name, ' ', '.')), '@example.com');
```

演示了 DDL（ALTER TABLE）和 DML（UPDATE）可以在同一个迁移脚本中混合使用。

### V3 - 创建订单表

```sql
CREATE TABLE customer_order (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0,
    status VARCHAR(20) DEFAULT 'PENDING',
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customer(id)
);
```

演示了外键约束、索引创建和默认值设置。

### V4 - 添加客户状态

```sql
ALTER TABLE customer ADD COLUMN status VARCHAR(20) DEFAULT 'ACTIVE';
UPDATE customer SET status = 'ACTIVE' WHERE status IS NULL;
```

为已有数据设置默认值的最佳实践。

## 迁移策略

### 开发阶段策略

1. **频繁的小迁移** - 每次变更创建一个新的迁移文件
2. **开发数据库可重建** - 开发阶段可以随时重建数据库
3. **版本号留余量** - 如 V1、V2、V3... 不需要 V1.1、V1.2

### 测试阶段策略

1. **迁移前备份** - 在测试环境验证前先备份数据库
2. **测试迁移和回滚** - 确保迁移脚本能正确执行
3. **数据迁移测试** - 验证数据迁移的正确性

### 生产阶段策略

1. **零停机迁移** - 使用向后兼容的迁移方式
2. **分步迁移** - 将大的结构变更拆分为多个小步骤
3. **回滚预案** - 准备回滚脚本（即使 Flyway 免费版不支持自动回滚）

### 向后兼容迁移示例

假设要将 name 列拆分为 first_name 和 last_name：

```
步骤1（V5）：添加新列（不删除旧列）
  ALTER TABLE customer ADD COLUMN first_name VARCHAR(50);
  ALTER TABLE customer ADD COLUMN last_name VARCHAR(50);

步骤2（V6）：迁移数据
  UPDATE customer SET first_name = SUBSTRING(name, 1, INSTR(name, ' ') - 1);
  UPDATE customer SET last_name = SUBSTRING(name, INSTR(name, ' ') + 1);

步骤3（代码部署）：更新应用代码使用新列

步骤4（V7）：删除旧列
  ALTER TABLE customer DROP COLUMN name;
```

## 回滚概念

### Flyway 的回滚机制

Flyway 的付费版本（Teams Edition）支持自动回滚，通过 `U` 前缀的 Undo 迁移脚本实现：

```
U1__Drop_customer_table.sql    -- 撤销 V1
U2__Remove_email_column.sql    -- 撤销 V2
```

### 免费版的回滚方案

免费版不提供自动回滚，但可以采用以下策略：

#### 1. 手动回滚脚本

为每个迁移创建对应的回滚 SQL，手动执行：

```sql
-- 回滚 V4
ALTER TABLE customer DROP COLUMN status;

-- 回滚 V3
DROP TABLE customer_order;

-- 回滚 V2
ALTER TABLE customer DROP COLUMN email;
```

#### 2. 数据库备份恢复

在生产环境执行迁移前先备份数据库，出问题时恢复备份。

#### 3. 向前修复

不回滚，而是创建新的迁移脚本来修复问题：

```
V5__Fix_customer_status_default.sql
```

这也是业界最推荐的做法，因为回滚可能导致数据丢失。

## CI/CD 集成

### Flyway 在 CI/CD 流水线中的位置

```
代码提交 --> 单元测试 --> 构建打包 --> [Flyway 迁移] --> 部署应用
```

### Maven 集成

```xml
<plugin>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-maven-plugin</artifactId>
    <configuration>
        <url>jdbc:h2:file:./target/database</url>
        <user>sa</user>
        <locations>
            <location>classpath:db/migration</location>
        </locations>
    </configuration>
</plugin>
```

### 命令行执行

```bash
# 执行迁移
mvn flyway:migrate

# 查看迁移状态
mvn flyway:info

# 验证迁移脚本
mvn flyway:validate

# 基线化（已存在的数据库）
mvn flyway:baseline
```

### GitHub Actions 集成示例

```yaml
name: Database Migration
on:
  push:
    branches: [main]
jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up JDK 11
        uses: actions/setup-java@v3
        with:
          java-version: '11'
      - name: Run Flyway Migration
        run: mvn flyway:migrate
        env:
          FLYWAY_URL: ${{ secrets.DB_URL }}
          FLYWAY_USER: ${{ secrets.DB_USER }}
          FLYWAY_PASSWORD: ${{ secrets.DB_PASSWORD }}
```

### 最佳实践

1. **在部署应用之前执行迁移** - 确保数据库结构先更新
2. **迁移失败时停止部署** - 不要在迁移失败的情况下继续部署
3. **在 CI 中验证迁移** - 每次构建都验证迁移脚本的有效性
4. **使用相同的迁移工具** - 开发、测试、生产使用相同的 Flyway 版本

## 项目结构

```
database-migration-flyway-demo/
├── pom.xml                                        # Maven 项目配置
├── README.md                                      # 项目说明文档
├── metadata.json                                  # 项目元数据
└── src/
    ├── main/
    │   ├── java/com/example/demo/
    │   │   ├── FlywayMigrationDemoApplication.java # 应用启动类
    │   │   ├── entity/
    │   │   │   └── Customer.java                   # 客户实体类
    │   │   ├── repository/
    │   │   │   └── CustomerRepository.java         # 数据访问层
    │   │   ├── service/
    │   │   │   └── CustomerService.java            # 业务逻辑层
    │   │   └── controller/
    │   │       └── CustomerController.java         # REST API 控制器
    │   └── resources/
    │       ├── application.yml                     # 应用配置
    │       └── db/migration/
    │           ├── V1__Create_customer_table.sql    # 迁移 V1
    │           ├── V2__Add_email_column.sql         # 迁移 V2
    │           ├── V3__Create_order_table.sql       # 迁移 V3
    │           └── V4__Add_customer_status.sql      # 迁移 V4
    └── test/
        └── java/com/example/demo/
            └── FlywayMigrationDemoApplicationTest.java # 测试类
```

## Flyway 配置详解

### application.yml 配置

```yaml
spring:
  flyway:
    enabled: true
    locations: classpath:db/migration
    baseline-on-migrate: true
    encoding: UTF-8
    validate-on-migrate: true
```

### 常用配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| enabled | true | 是否启用 Flyway |
| locations | classpath:db/migration | 迁移脚本位置 |
| baseline-on-migrate | false | 已存在的数据库是否自动基线化 |
| encoding | UTF-8 | 迁移脚本编码 |
| validate-on-migrate | true | 迁移前是否验证已执行的脚本 |
| table | flyway_schema_history | 历史记录表名 |
| baseline-version | 1 | 基线版本号 |
| out-of-order | false | 是否允许乱序执行 |

## 快速开始

### 环境要求

- JDK 11+
- Maven 3.6+

### 运行步骤

1. **克隆项目**

```bash
git clone <repository-url>
cd database-migration-flyway-demo
```

2. **编译项目**

```bash
mvn clean compile
```

3. **运行测试**

```bash
mvn test
```

4. **启动应用**

```bash
mvn spring-boot:run
```

启动后，Flyway 会自动执行所有迁移脚本，可以在日志中看到迁移执行信息。

### API 测试示例

```bash
# 创建客户
curl -X POST http://localhost:8080/api/customers \
  -H "Content-Type: application/json" \
  -d '{"name":"张三","email":"zhangsan@example.com","phone":"13800138000"}'

# 获取所有客户
curl http://localhost:8080/api/customers

# 获取指定客户
curl http://localhost:8080/api/customers/1

# 更新客户
curl -X PUT http://localhost:8080/api/customers/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"李四","email":"lisi@example.com","phone":"13900139000","status":"VIP"}'

# 删除客户
curl -X DELETE http://localhost:8080/api/customers/1
```

### 查看迁移历史

启动应用后，访问 H2 控制台 `http://localhost:8080/h2-console`，执行以下 SQL 查看迁移历史：

```sql
SELECT * FROM flyway_schema_history ORDER BY installed_rank;
```

## 常见问题

### 1. 迁移脚本校验失败

**现象**：`FlywayValidateException: Migration checksum mismatch`

**原因**：已执行的迁移脚本被修改。

**解决方案**：
- 不要修改已执行的迁移脚本
- 如果必须修改，使用 `flyway repair` 修复校验和
- 新的变更创建新的迁移脚本

### 2. 迁移顺序错误

**现象**：多个开发人员同时提交迁移脚本，版本号冲突。

**解决方案**：
- 使用时间戳作为版本号（如 V20230601120000）
- 合并代码时检查版本号冲突
- 设置 `out-of-order: true`（不推荐）

### 3. 已存在的数据库如何引入 Flyway

**解决方案**：
1. 设置 `baseline-on-migrate: true`
2. 手动执行 `flyway baseline`
3. 之后的新迁移正常执行

### 4. 多环境迁移管理

**解决方案**：
- 开发环境：使用 `create-drop` 或 `create`，可以随时重建
- 测试环境：使用 Flyway 正常迁移，测试迁移过程
- 生产环境：在 CI/CD 中执行迁移，先备份再迁移

## 学习资源

- [Flyway 官方文档](https://flywaydb.org/documentation/)
- [Spring Boot Flyway 集成](https://docs.spring.io/spring-boot/docs/current/reference/html/howto.html#howto.data-initialization.migration-tool.flyway)
- [Flyway 最佳实践](https://flywaydb.org/documentation/concepts/bestpractices)
