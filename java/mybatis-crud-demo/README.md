# MyBatis CRUD 演示项目

## 项目简介

本项目是一个基于 Spring Boot 2.7.12 的 MyBatis CRUD 演示应用，使用 MyBatis 作为 ORM 框架，H2 作为内存数据库。项目展示了 MyBatis 注解和 XML 两种映射方式、动态 SQL、分页查询等核心功能。

## 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Java | 11 | JDK 版本 |
| Spring Boot | 2.7.12 | 应用框架 |
| MyBatis | 2.3.1 (starter) | ORM 框架 |
| H2 | Runtime | 内存数据库 |
| Maven | - | 构建工具 |

## MyBatis vs JPA

### 基本概念

**MyBatis** 是一款优秀的持久层框架，它支持自定义 SQL、存储过程以及高级映射。MyBatis 免除了几乎所有的 JDBC 代码和参数手动设置以及获取结果集的工作。

**JPA**（Java Persistence API）是 Java 持久化 API 的标准规范，Hibernate 是其最常见的实现。JPA 采用面向对象的方式操作数据库。

### 详细对比

| 特性 | MyBatis | JPA (Hibernate) |
|------|---------|-----------------|
| SQL 控制 | 完全手动控制 SQL | 自动生成 SQL（可自定义） |
| 学习曲线 | 较低，SQL 基础即可 | 较高，需要理解 ORM 概念 |
| 映射方式 | 注解 + XML | 注解为主 |
| 动态 SQL | 内置强大的动态 SQL | 通过 Criteria API |
| 数据库迁移 | SQL 可控，迁移容易 | 需要注意方言差异 |
| 缓存 | 一级缓存 + 二级缓存 | 一级缓存 + 二级缓存 + 查询缓存 |
| 适合场景 | 复杂 SQL、报表、DBA 参与的项目 | 快速开发、领域驱动设计 |

### 如何选择

- **选择 MyBatis** 的场景：
  - 项目有复杂 SQL 需求，需要精细控制 SQL
  - 团队中有 DBA，需要审核 SQL
  - 需要进行数据库性能调优
  - 已有大量存储过程
  - 数据库经常变更

- **选择 JPA** 的场景：
  - 快速迭代开发的互联网项目
  - 领域模型相对简单，以 CRUD 为主
  - 团队习惯面向对象编程
  - 需要快速切换底层数据库

## 注解 vs XML 映射

MyBatis 提供了两种 SQL 映射方式：注解和 XML。本项目同时展示了这两种方式的使用。

### 注解方式

注解方式适合简单的 SQL 语句，代码简洁直观：

```java
@Mapper
public interface UserMapper {

    @Insert("INSERT INTO user (username, email, age, phone, status) " +
            "VALUES (#{username}, #{email}, #{age}, #{phone}, #{status})")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(User user);

    @Select("SELECT * FROM user WHERE id = #{id}")
    User findById(@Param("id") Long id);

    @Update("UPDATE user SET username = #{username}, email = #{email} " +
            "WHERE id = #{id}")
    int update(User user);

    @Delete("DELETE FROM user WHERE id = #{id}")
    int deleteById(@Param("id") Long id);
}
```

**注解方式优点**：
- SQL 和 Java 代码在同一文件中，查看方便
- 编译期可以发现部分错误
- 适合简单查询

**注解方式缺点**：
- 复杂 SQL 难以维护
- 无法使用动态 SQL 的高级特性
- SQL 过长时代码可读性差

### XML 方式

XML 方式适合复杂 SQL 和动态 SQL：

```xml
<select id="findByCondition" parameterType="User" resultMap="userResultMap">
    SELECT id, username, email, age, phone, status
    FROM user
    <where>
        <if test="username != null and username != ''">
            AND username LIKE CONCAT('%', #{username}, '%')
        </if>
        <if test="email != null and email != ''">
            AND email = #{email}
        </if>
        <if test="status != null and status != ''">
            AND status = #{status}
        </if>
    </where>
    ORDER BY id
</select>
```

**XML 方式优点**：
- 支持动态 SQL
- SQL 和 Java 代码分离
- 复杂 SQL 易于维护和格式化
- 可以复用 SQL 片段

**XML 方式缺点**：
- 需要额外维护 XML 文件
- 切换文件查看 SQL 和接口定义
- XML 语法有学习成本

### 最佳实践

在实际项目中，建议**混合使用**两种方式：
- 简单的 CRUD 操作使用注解方式
- 复杂查询和动态 SQL 使用 XML 方式
- 同一个 Mapper 接口中可以同时使用两种方式

## 动态 SQL

### 什么是动态 SQL

动态 SQL 是 MyBatis 最强大的特性之一。通过动态 SQL，可以根据不同的条件动态地拼接 SQL 语句，避免了在 Java 代码中进行繁琐的字符串拼接。

### 动态 SQL 标签

#### if 标签

最常用的条件判断标签：

```xml
<if test="username != null and username != ''">
    AND username LIKE CONCAT('%', #{username}, '%')
</if>
```

当 `username` 不为空时，才会将条件拼接到 SQL 中。

#### where 标签

智能处理 WHERE 关键字和 AND/OR：

```xml
<where>
    <if test="username != null">AND username = #{username}</if>
    <if test="age != null">AND age = #{age}</if>
</where>
```

`where` 标签会自动：
- 在有条件时添加 WHERE 关键字
- 去除第一个条件前多余的 AND/OR

#### choose/when/otherwise 标签

类似 Java 中的 switch-case：

```xml
<choose>
    <when test="id != null">
        AND id = #{id}
    </when>
    <when test="username != null">
        AND username = #{username}
    </when>
    <otherwise>
        AND status = 'ACTIVE'
    </otherwise>
</choose>
```

#### set 标签

用于 UPDATE 语句，动态设置更新的字段：

```xml
<update id="updateSelective">
    UPDATE user
    <set>
        <if test="username != null">username = #{username},</if>
        <if test="email != null">email = #{email},</if>
        <if test="age != null">age = #{age},</if>
    </set>
    WHERE id = #{id}
</update>
```

#### foreach 标签

用于 IN 查询和批量操作：

```xml
<select id="findByIds" resultMap="userResultMap">
    SELECT * FROM user WHERE id IN
    <foreach collection="ids" item="id" open="(" separator="," close=")">
        #{id}
    </foreach>
</select>
```

#### sql/include 标签

可复用的 SQL 片段：

```xml
<sql id="userColumns">
    id, username, email, age, phone, status
</sql>

<select id="findAll" resultMap="userResultMap">
    SELECT <include refid="userColumns"/> FROM user
</select>
```

#### trim 标签

自定义前缀和后缀：

```xml
<trim prefix="WHERE" prefixOverrides="AND | OR">
    <if test="username != null">AND username = #{username}</if>
</trim>
```

## 结果映射

### 自动映射

当数据库列名和 Java 属性名一致（或开启驼峰映射后一致）时，MyBatis 可以自动映射：

```yaml
mybatis:
  configuration:
    map-underscore-to-camel-case: true
```

开启后，`user_name` 列会自动映射到 `userName` 属性。

### resultMap

对于复杂的映射关系，可以使用 resultMap：

```xml
<resultMap id="userResultMap" type="User">
    <id property="id" column="id"/>
    <result property="username" column="username"/>
    <result property="email" column="email"/>
    <result property="age" column="age"/>
    <result property="phone" column="phone"/>
    <result property="status" column="status"/>
</resultMap>
```

resultMap 支持以下映射类型：
- **result** - 普通字段映射
- **association** - 一对一关联映射
- **collection** - 一对多关联映射
- **discriminator** - 根据某列的值决定使用哪个映射

### 关联查询映射

```xml
<resultMap id="userWithOrdersMap" type="User">
    <id property="id" column="id"/>
    <result property="username" column="username"/>
    <collection property="orders" ofType="Order">
        <id property="id" column="order_id"/>
        <result property="amount" column="amount"/>
    </collection>
</resultMap>
```

## 分页查询

### 手动分页

最简单的分页方式，使用 LIMIT 和 OFFSET：

```xml
<select id="findWithPagination" resultMap="userResultMap">
    SELECT id, username, email, age, phone, status
    FROM user
    ORDER BY id
    LIMIT #{limit} OFFSET #{offset}
</select>
```

对应的 Java 接口：

```java
List<User> findWithPagination(@Param("offset") int offset, @Param("limit") int limit);
```

调用方式：

```java
int page = 1;
int size = 10;
int offset = (page - 1) * size;
List<User> users = userMapper.findWithPagination(offset, size);
```

### PageHelper 插件

更推荐使用 PageHelper 插件实现分页：

```xml
<dependency>
    <groupId>com.github.pagehelper</groupId>
    <artifactId>pagehelper-spring-boot-starter</artifactId>
    <version>1.4.7</version>
</dependency>
```

使用方式：

```java
PageHelper.startPage(pageNum, pageSize);
List<User> users = userMapper.findAll();
PageInfo<User> pageInfo = new PageInfo<>(users);
```

PageHelper 提供了完整的分页信息：
- 总记录数
- 总页数
- 当前页数据
- 是否有下一页/上一页

## 项目结构

```
mybatis-crud-demo/
├── pom.xml                                        # Maven 项目配置
├── README.md                                      # 项目说明文档
├── metadata.json                                  # 项目元数据
└── src/
    ├── main/
    │   ├── java/com/example/demo/
    │   │   ├── MybatisCrudDemoApplication.java    # 应用启动类
    │   │   ├── entity/
    │   │   │   └── User.java                      # 用户实体类
    │   │   ├── mapper/
    │   │   │   └── UserMapper.java                # MyBatis Mapper 接口
    │   │   ├── service/
    │   │   │   └── UserService.java               # 业务逻辑层
    │   │   ├── controller/
    │   │   │   └── UserController.java            # REST API 控制器
    │   │   └── config/
    │   │       └── MyBatisConfig.java             # MyBatis 配置
    │   └── resources/
    │       ├── application.yml                    # 应用配置
    │       ├── schema.sql                         # 数据库表结构
    │       └── mapper/
    │           └── UserMapper.xml                 # XML Mapper 文件
    └── test/
        └── java/com/example/demo/
            ├── MybatisCrudDemoApplicationTest.java # 启动测试
            └── mapper/
                └── UserMapperTest.java             # Mapper 测试
```

## 快速开始

### 环境要求

- JDK 11+
- Maven 3.6+

### 运行步骤

1. **克隆项目**

```bash
git clone <repository-url>
cd mybatis-crud-demo
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

### API 测试示例

```bash
# 创建用户
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"张三","email":"zhangsan@example.com","age":25,"phone":"13800138000","status":"ACTIVE"}'

# 获取所有用户
curl http://localhost:8080/api/users

# 获取指定用户
curl http://localhost:8080/api/users/1

# 按状态查询
curl http://localhost:8080/api/users/status/ACTIVE

# 条件搜索
curl -X POST http://localhost:8080/api/users/search \
  -H "Content-Type: application/json" \
  -d '{"username":"张","status":"ACTIVE"}'

# 分页查询
curl "http://localhost:8080/api/users/page?page=1&size=10"

# 更新用户
curl -X PUT http://localhost:8080/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"username":"李四","email":"lisi@example.com","age":30,"phone":"13900139000","status":"ACTIVE"}'

# 删除用户
curl -X DELETE http://localhost:8080/api/users/1
```

## MyBatis 配置详解

### application.yml 配置项

```yaml
mybatis:
  type-aliases-package: com.example.demo.entity
  mapper-locations: classpath:mapper/*.xml
  configuration:
    map-underscore-to-camel-case: true
```

| 配置项 | 说明 |
|--------|------|
| type-aliases-package | 类型别名包路径，简化 XML 中的类型引用 |
| mapper-locations | XML Mapper 文件位置 |
| map-underscore-to-camel-case | 开启下划线到驼峰的自动映射 |
| default-fetch-size | 设置默认的 fetchSize |
| default-statement-timeout | SQL 执行超时时间（秒） |
| cache-enabled | 是否开启二级缓存（默认 true） |
| lazy-loading-enabled | 是否开启懒加载 |

### SqlSessionFactory 配置

可以通过 Java Config 自定义 SqlSessionFactory：

```java
@Bean
public SqlSessionFactory sqlSessionFactory(DataSource dataSource) throws Exception {
    SqlSessionFactoryBean sessionFactory = new SqlSessionFactoryBean();
    sessionFactory.setDataSource(dataSource);
    sessionFactory.setTypeAliasesPackage("com.example.demo.entity");
    sessionFactory.setMapperLocations(...);
    Configuration configuration = new Configuration();
    configuration.setMapUnderscoreToCamelCase(true);
    sessionFactory.setConfiguration(configuration);
    return sessionFactory.getObject();
}
```

## 常见问题

### 1. Mapper 接口无法注入

**原因**：未添加 `@Mapper` 注解或未配置 `@MapperScan`。

**解决方案**：在 Mapper 接口上添加 `@Mapper` 注解，或在启动类上添加 `@MapperScan("com.example.demo.mapper")`。

### 2. XML Mapper 文件找不到

**原因**：mapper-locations 配置路径不正确。

**解决方案**：确认 XML 文件路径与配置一致，默认为 `classpath:mapper/*.xml`。

### 3. 属性映射失败

**原因**：数据库列名与 Java 属性名不匹配。

**解决方案**：开启 `map-underscore-to-camel-case`，或使用 `@Result` 注解/`resultMap` 手动映射。

### 4. 动态 SQL 不生效

**原因**：参数名未使用 `@Param` 注解。

**解决方案**：多参数方法必须使用 `@Param` 注解指定参数名。

## 学习资源

- [MyBatis 官方文档](https://mybatis.org/mybatis-3/zh/index.html)
- [MyBatis Spring Boot Starter](https://mybatis.org/spring-boot-starter/mybatis-spring-boot-autoconfigure/)
- [Spring Boot 集成 MyBatis](https://spring.io/guides/gs/mybatis/)
