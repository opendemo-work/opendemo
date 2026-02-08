# Database CLI命令详解

本文档详细解释数据库常用CLI命令的用途、输出示例、内容解析、注意事项以及在生产环境中执行的安全风险。

## 1. mysql (MySQL Client)

### 用途
`mysql` 是MySQL数据库的官方命令行客户端工具，用于连接和管理MySQL数据库服务器。它是数据库管理员和开发人员最常用的工具之一，支持执行SQL语句、管理数据库对象、导入导出数据、执行脚本文件等功能。mysql客户端提供了丰富的命令行选项和交互式操作界面，是MySQL生态系统的核心管理工具。

### 输出示例
```bash
# 基本连接示例
$ mysql -u root -p -h localhost -P 3306 test_db
Enter password: ******
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 12345
Server version: 8.0.35 MySQL Community Server - GPL

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 

# 执行单条SQL命令
$ mysql -u root -p -e "SHOW DATABASES;"
Enter password: ******
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| test_db            |
+--------------------+
```

### 内容解析
- **连接信息**: 显示连接ID、服务器版本、版权信息
- **提示符**: `mysql>` 表示已进入MySQL交互模式
- **命令结束符**: SQL语句以`;`或`\g`结尾
- **输出格式**: 支持表格、垂直、HTML等多种格式

### 常用参数详解
- `-u, --user=name`: 指定用户名
- `-p, --password[=name]`: 指定密码（不带等号会交互式输入）
- `-h, --host=name`: 指定主机名或IP地址
- `-P, --port=#`: 指定端口号
- `-D, --database=name`: 指定数据库名
- `-e, --execute=name`: 执行SQL语句后退出
- `-s, --silent`: 安静模式，减少输出装饰

### 实际应用场景
1. **日常管理**: 连接数据库执行管理操作
2. **脚本执行**: 自动化执行SQL脚本文件
3. **数据导入**: 导入CSV、SQL等格式的数据
4. **备份恢复**: 配合mysqldump进行数据备份恢复
5. **故障排查**: 快速连接数据库进行问题诊断

### 注意事项
- 密码直接在命令行中可见，存在安全风险
- 大量数据查询可能导致客户端内存占用过高
- 长时间运行的查询可能受超时设置影响

### 生产安全风险
- **高风险**: 命令行中明文密码容易被进程查看捕获
- **中等风险**: 可能暴露数据库结构和数据内容
- **低风险**: 连接信息和版本信息的泄露

---

## 2. psql (PostgreSQL Client)

### 用途
`psql` 是PostgreSQL数据库的官方命令行客户端工具，提供了完整的数据库交互功能。它支持SQL执行、元命令操作、脚本执行、数据导入导出等丰富功能。psql具有强大的编辑能力、历史记录、变量替换等特性，是PostgreSQL数据库管理的核心工具。

### 输出示例
```bash
# 基本连接示例
$ psql -U postgres -d test_db -h localhost -p 5432
Password for user postgres: ******
psql (15.3)
Type "help" for help.

test_db=# 

# 执行单条SQL命令
$ psql -U postgres -c "SELECT version();"
                                                 version                                                  
----------------------------------------------------------------------------------------------------------
 PostgreSQL 15.3 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 11.3.1 20221121 (Red Hat 11.3.1-4), 64-bit
(1 row)
```

### 内容解析
- **连接信息**: 显示PostgreSQL版本信息
- **提示符**: `database_name=#` 表示超级用户，`database_name=>` 表示普通用户
- **元命令**: 以反斜杠开头的特殊命令（如`\dt`、`\d`）
- **输出格式**: 表格形式显示查询结果和元数据

### 常用参数详解
- `-U, --username=USERNAME`: 数据库用户名
- `-d, --dbname=DBNAME`: 数据库名称
- `-h, --host=HOSTNAME`: 服务器主机名
- `-p, --port=PORT`: 服务器端口
- `-c, --command=COMMAND`: 执行单条SQL命令
- `-f, --file=FILENAME`: 执行SQL文件

### 实际应用场景
1. **数据库探索**: 使用元命令查看数据库结构
2. **脚本执行**: 批量执行复杂的SQL脚本
3. **数据操作**: 进行复杂的数据查询和修改
4. **权限管理**: 管理用户权限和角色
5. **性能分析**: 执行性能测试和分析查询

### 注意事项
- 需要正确配置.pgpass文件避免频繁输入密码
- 某些元命令可能需要超级用户权限
- 大结果集可能需要调整显示设置

### 生产安全风险
- **中等风险**: 可能暴露数据库结构和敏感数据
- **低风险**: 版本信息和连接信息的泄露
- **注意**: .pgpass文件的权限设置很重要

---

## 3. mongo (MongoDB Client)

### 用途
`mongo` 是MongoDB数据库的官方命令行客户端工具，提供对MongoDB数据库的交互式访问。它支持JavaScript语法的操作、数据库管理、集合操作、数据查询和修改等功能。作为NoSQL数据库的代表性工具，mongo客户端为文档数据库的操作提供了直观便捷的界面。

### 输出示例
```bash
# 基本连接示例
$ mongo localhost:27017/test_db
MongoDB shell version v5.0.15
connecting to: mongodb://localhost:27017/test_db
Implicit session: session { "id" : UUID("12345678-1234-1234-1234-123456789012") }
MongoDB server version: 5.0.15
> 

# 执行JavaScript命令
> db.version()
5.0.15

> db.stats()
{
        "db" : "test_db",
        "collections" : 2,
        "views" : 0,
        "objects" : 1000,
        "avgObjSize" : 256,
        "dataSize" : 256000,
        "storageSize" : 1048576,
        "indexes" : 3,
        "indexSize" : 81920,
        "ok" : 1
}
```

### 内容解析
- **连接信息**: 显示shell和服务器版本
- **提示符**: `>` 表示MongoDB交互模式
- **JavaScript语法**: 支持完整的JavaScript操作
- **文档格式**: JSON格式的文档显示

### 常用参数详解
- `--host <hostname>`: 指定主机名
- `--port <port>`: 指定端口
- `-u <username> -p <password>`: 认证信息
- `--authenticationDatabase <dbname>`: 认证数据库
- `--eval <javascript>`: 执行JavaScript代码

### 实际应用场景
1. **数据探索**: 交互式查询和浏览文档数据
2. **数据操作**: 插入、更新、删除文档
3. **集合管理**: 创建、删除、索引管理
4. **性能测试**: 执行查询性能测试
5. **脚本执行**: 运行JavaScript脚本文件

### 注意事项
- JavaScript语法的学习曲线
- 大文档集的查询性能考虑
- 连接池和超时设置

### 生产安全风险
- **高风险**: 可能直接修改生产数据
- **中等风险**: 暴露数据库结构和数据内容
- **注意**: 默认情况下可能存在安全警告

---

## 4. redis-cli (Redis Client)

### 用途
`redis-cli` 是Redis数据库的官方命令行客户端工具，提供对Redis键值存储的完整访问能力。它支持所有Redis命令的执行、管道操作、发布订阅、Lua脚本执行等功能。作为高性能内存数据库的管理工具，redis-cli以其简洁高效的特点深受开发者喜爱。

### 输出示例
```bash
# 基本连接示例
$ redis-cli -h localhost -p 6379 -a password
127.0.0.1:6379> 

# 执行Redis命令
127.0.0.1:6379> SET mykey "Hello Redis"
OK

127.0.0.1:6379> GET mykey
"Hello Redis"

127.0.0.1:6379> TTL mykey
(integer) -1

# 查看服务器信息
127.0.0.1:6379> INFO
# Server
redis_version:7.0.8
redis_git_sha1:00000000
redis_mode:standalone
os:Linux 5.15.0-ubuntu x86_64
multiplexing_api:epoll
process_id:12345
tcp_port:6379
uptime_in_seconds:3600
```

### 内容解析
- **连接信息**: 显示服务器地址和端口
- **命令响应**: OK表示成功，错误信息显示具体问题
- **数据类型**: 字符串、整数、数组等不同类型的结果
- **服务器信息**: 详细的服务器状态和配置信息

### 常用参数详解
- `-h <hostname>`: 服务器主机名
- `-p <port>`: 服务器端口
- `-a <password>`: 认证密码
- `-n <database>`: 数据库编号(0-15)
- `--raw`: 原始格式输出
- `--stat`: 实时统计信息

### 实际应用场景
1. **数据操作**: 键值的增删改查操作
2. **性能测试**: 延迟和吞吐量测试
3. **监控诊断**: 实时查看服务器状态
4. **批量处理**: 管道和脚本批量操作
5. **发布订阅**: 消息队列功能测试

### 注意事项
- 某些危险命令(如FLUSHALL)需要谨慎使用
- 大量KEY操作可能影响性能
- 连接超时和重试机制的配置

### 生产安全风险
- **高风险**: 可能执行破坏性命令(FLUSHALL, FLUSHDB)
- **中等风险**: 暴露内存数据和配置信息
- **低风险**: 服务器版本和统计信息泄露

---

## 5. mysqldump

### 用途
`mysqldump` 是MySQL数据库的逻辑备份工具，用于创建数据库、表结构和数据的SQL转储文件。它支持完整备份、增量备份、特定表备份等多种备份策略，是MySQL数据库备份恢复的标准工具。mysqldump生成的SQL文件可以在任何MySQL实例上恢复，具有良好的移植性。

### 输出示例
```bash
# 基本备份示例
$ mysqldump -u root -p test_db > backup.sql
Enter password: ******

# 查看备份文件内容
$ head -20 backup.sql
-- MySQL dump 10.13  Distrib 8.0.35, for Linux (x86_64)
--
-- Host: localhost    Database: test_db
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;

# 压缩备份
$ mysqldump -u root -p test_db | gzip > backup.sql.gz

# 仅备份结构
$ mysqldump -u root -p --no-data test_db > schema_only.sql
```

### 内容解析
- **头部信息**: 包含MySQL版本、服务器信息、字符集设置
- **SQL语句**: CREATE TABLE、INSERT等标准SQL语句
- **注释标记**: /*! */格式的MySQL特有语法注释
- **完整性保证**: 包含外键约束、索引等完整定义

### 常用参数详解
- `--single-transaction`: 在单一事务中执行备份(适用于InnoDB)
- `--routines`: 备份存储过程和函数
- `--triggers`: 备份触发器
- `--events`: 备份事件调度器
- `--master-data`: 包含二进制日志位置信息
- `--where='condition'`: 条件备份特定数据

### 实际应用场景
1. **定期备份**: 自动化每日/每周备份任务
2. **迁移准备**: 数据库迁移前的完整备份
3. **灾难恢复**: 系统故障后的数据恢复
4. **开发测试**: 为开发环境提供生产数据副本
5. **版本控制**: 数据库结构变更的历史记录

### 注意事项
- 备份过程中可能影响数据库性能
- 大型数据库备份需要充足的时间和存储空间
- 需要考虑备份期间的数据一致性

### 生产安全风险
- **中等风险**: 备份文件包含完整的数据和结构信息
- **注意**: 备份文件的存储安全和访问控制
- **建议**: 加密敏感数据的备份文件

---

## 6. pg_dump

### 用途
`pg_dump` 是PostgreSQL数据库的逻辑备份工具，用于创建数据库的备份文件。它支持多种输出格式(custom、tar、directory、plain)，可以备份整个数据库、特定表或特定数据。pg_dump是PostgreSQL生态系统中最重要的备份工具，具有高度的灵活性和可靠性。

### 输出示例
```bash
# 基本备份示例
$ pg_dump -U postgres test_db > backup.sql
Password: ******

# 自定义格式备份(支持并行恢复)
$ pg_dump -U postgres -Fc test_db > backup.dump

# 目录格式备份
$ pg_dump -U postgres -Fd test_db -f backup_directory

# 仅备份结构
$ pg_dump -U postgres --schema-only test_db > schema.sql

# 备份特定表
$ pg_dump -U postgres -t users -t orders test_db > specific_tables.sql
```

### 内容解析
- **格式多样性**: 支持纯文本SQL、自定义二进制、tar包等多种格式
- **并行处理**: 自定义格式支持并行备份和恢复
- **增量能力**: 可以配合时间戳进行增量备份
- **压缩支持**: 内置或外部压缩选项

### 常用参数详解
- `-Fc, --format=custom`: 自定义格式(推荐)
- `-Fd, --format=directory`: 目录格式
- `-Ft, --format=tar`: tar格式
- `-Fp, --format=plain`: 纯文本格式
- `-j, --jobs=NUM`: 并行作业数
- `-t, --table=TABLE`: 备份特定表
- `-n, --schema=SCHEMA`: 备份特定模式

### 实际应用场景
1. **生产备份**: 企业级数据库的定期备份策略
2. **版本升级**: 数据库版本迁移的准备工作
3. **开发支持**: 为开发团队提供生产数据快照
4. **合规要求**: 满足数据保留和审计要求
5. **灾难恢复**: 构建完整的数据保护体系

### 注意事项
- 备份过程中的锁机制和性能影响
- 大型数据库的备份时间和存储需求
- 不同格式的适用场景和限制

### 生产安全风险
- **中等风险**: 备份文件包含敏感业务数据
- **注意**: 备份传输和存储过程中的安全性
- **建议**: 实施备份文件的加密和访问控制

---

## 7. mongodump

### 用途
`mongodump` 是MongoDB数据库的备份工具，用于创建数据库的BSON格式备份。它支持完整备份、集合级别备份、查询条件备份等功能，是MongoDB数据保护的核心工具。mongodump生成的备份文件保持了MongoDB文档的原生格式，便于高效的恢复操作。

### 输出示例
```bash
# 基本备份示例
$ mongodump --host localhost --port 27017 --db test_db --out /backup/
2024-01-15T14:30:45.123+0000	writing test_db.users to /backup/test_db/users.bson
2024-01-15T14:30:45.456+0000	writing test_db.orders to /backup/test_db/orders.bson
2024-01-15T14:30:45.789+0000	done dumping test_db.users (1000 documents)
2024-01-15T14:30:45.890+0000	done dumping test_db.orders (500 documents)

# 压缩备份
$ mongodump --host localhost --gzip --archive=/backup/backup.archive

# 备份特定集合
$ mongodump --host localhost --db test_db --collection users --out /backup/

# 条件备份
$ mongodump --host localhost --db test_db --collection users --query '{"age": {"$gte": 18}}' --out /backup/
```

### 内容解析
- **BSON格式**: MongoDB原生二进制JSON格式
- **元数据文件**: 包含索引、校验和其他集合信息的JSON文件
- **进度显示**: 实时显示备份进度和文档数量
- **多种输出**: 支持目录、压缩档案等输出方式

### 常用参数详解
- `--host <hostname:port>`: 指定MongoDB实例
- `--db <database>`: 指定数据库名
- `--collection <collection>`: 指定集合名
- `--query <json>`: 查询条件过滤
- `--out <path>`: 输出目录路径
- `--gzip`: 启用压缩
- `--archive=<file>`: 输出到单个压缩档案文件

### 实际应用场景
1. **日常备份**: 自动化的定期数据保护
2. **迁移准备**: 数据库迁移前的完整备份
3. **开发支持**: 为开发环境提供真实数据
4. **合规审计**: 满足数据保留要求
5. **版本升级**: 新版本部署前的数据保障

### 注意事项
- 备份过程对数据库性能的影响
- 大集合备份的时间和存储考量
- 分片集群备份的复杂性

### 生产安全风险
- **高风险**: 备份文件包含完整的业务数据
- **注意**: 备份文件的传输和存储安全
- **建议**: 实施备份文件加密和访问控制策略

---

## 8. pt-query-digest

### 用途
`pt-query-digest` 是Percona Toolkit中的SQL分析工具，专门用于分析MySQL慢查询日志。它能够解析慢查询日志，统计查询模式、执行时间、资源消耗等关键指标，帮助DBA识别性能瓶颈和优化机会。这是MySQL性能优化不可或缺的专业工具。

### 输出示例
```bash
# 基本分析示例
$ pt-query-digest /var/log/mysql/slow.log

# Sample output structure:
# Rank Query ID           Response time Calls  R/Call V/M   Item
# ==== ================== ============= ====== ====== ===== ==============
#    1 0x123456789ABCDEF  15.2345s 33.8%    123 0.1234  0.45 SELECT users
#    2 0xFEDCBA987654321  12.3456s 27.4%     89 0.1387  0.38 SELECT orders

# Detailed breakdown for top query:
# Query_time sparkline: |    ^ _ _ _ _ _ _ _ 
# Count         10     123
# Exec time     34   15.2s   102ms   2.3s   123ms   890ms   234ms   110ms
# Lock time     25   301ms    50us    45ms     2ms     8ms     4ms   800us
# Rows sent     15    847      1     1234    6.89     10     23.4     1
# Rows examine  20  24691      0    56789   200.7    400    456.7    10
```

### 内容解析
- **总体统计**: 查询总数、总执行时间、平均每秒查询数
- **排名分析**: 按资源消耗排序的查询列表
- **详细剖析**: 单个查询的完整性能分析
- **可视化图表**: ASCII艺术形式的趋势图
- **优化建议**: 基于分析结果的改进建议

### 常用参数详解
- `--limit`: 限制显示的查询数量
- `--filter`: 过滤特定条件的查询
- `--group-by`: 按指定维度分组统计
- `--order-by`: 指定排序依据
- `--since/--until`: 指定时间范围
- `--explain`: 为慢查询生成EXPLAIN计划

### 实际应用场景
1. **性能诊断**: 识别最消耗资源的SQL查询
2. **优化指导**: 为查询优化提供数据支撑
3. **容量规划**: 分析查询模式预测资源需求
4. **问题追溯**: 定位性能下降的根本原因
5. **基准建立**: 建立正常的性能基准线

### 注意事项
- 需要启用MySQL慢查询日志
- 分析大型日志文件可能消耗较多资源
- 某些复杂查询的分析可能不够准确
- 需要结合业务场景理解分析结果

### 生产安全风险
- **中等风险**: 可能暴露SQL查询逻辑和数据结构
- **注意**: 分析报告的访问控制和分发范围
- **建议**: 敏感查询信息的脱敏处理

---