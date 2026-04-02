# MongoDB Integration Demo

Spring Data MongoDB集成演示项目，演示如何使用MongoDB进行文档存储。

## 技术栈

- Spring Boot 2.7
- Spring Data MongoDB
- MongoDB 4.x/5.x/6.x

## 项目结构

```
mongodb-integration-demo/
├── src/main/java/com/example/demo/
│   ├── MongoDbDemoApplication.java        # 应用入口
│   ├── config/
│   │   └── MongoConfig.java               # MongoDB配置
│   ├── controller/
│   │   └── UserController.java            # 用户控制器
│   ├── entity/
│   │   └── User.java                      # 用户实体（嵌套文档示例）
│   ├── repository/
│   │   └── UserRepository.java            # MongoDB仓库
│   └── service/
│       └── UserService.java               # 用户服务
├── src/main/resources/
│   └── application.yml                    # 应用配置
├── pom.xml
└── README.md
```

## MongoDB简介

### 什么是MongoDB

MongoDB是一个开源的文档型NoSQL数据库，使用JSON-like的BSON格式存储数据。特点：
- 灵活的文档模型
- 水平可扩展
- 高性能
- 丰富的查询语言

### 核心概念对比

| MongoDB | 关系型数据库 |
|---------|-------------|
| Database | Database |
| Collection | Table |
| Document | Row |
| Field | Column |
| Embedded Document | Join |

### 文档模型优势

```javascript
// MongoDB - 一个文档包含完整信息
{
  _id: ObjectId("..."),
  username: "john",
  email: "john@example.com",
  address: {           // 嵌套文档
    city: "北京",
    street: "xxx街道"
  },
  tags: ["developer", "java"]  // 数组
}
```

## 核心注解说明

### @Document

```java
@Document(collection = "users")
public class User {
    @Id
    private String id;
}
```

### @Id

标记文档的主键字段。MongoDB使用`_id`作为主键。

### @Indexed

```java
@Indexed(unique = true)
private String username;
```

创建索引，提高查询性能。

### @Field

```java
@Field("user_name")
private String username;
```

指定字段在文档中的名称。

### @CreatedDate / @LastModifiedDate

```java
@CreatedDate
private Date createdAt;

@LastModifiedDate
private Date updatedAt;
```

自动填充创建时间和更新时间（需要配合`@EnableMongoAuditing`）。

### @DBRef

```java
@DBRef
private Department department;
```

引用另一个文档（类似于外键）。

## 快速开始

### 1. 启动MongoDB

使用Docker启动：

```bash
docker run -d --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=123456 \
  mongo:latest
```

或使用本地MongoDB：

```bash
mongod --dbpath /data/db
```

### 2. 启动应用

```bash
mvn spring-boot:run
```

### 3. 初始化数据

```bash
curl -X POST http://localhost:8080/api/users/init
```

### 4. 测试接口

```bash
# 添加用户
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "age": 28,
    "address": {
      "city": "深圳",
      "street": "南山区xxx路",
      "zipCode": "518000"
    },
    "tags": ["developer", "python"]
  }'

# 查询所有用户
curl http://localhost:8080/api/users

# 根据ID查询
curl http://localhost:8080/api/users/{id}

# 根据用户名查询
curl http://localhost:8080/api/users/username/john

# 根据年龄范围查询
curl "http://localhost:8080/api/users/age-range?min=20&max=30"

# 根据城市查询
curl http://localhost:8080/api/users/city/北京

# 根据标签查询
curl http://localhost:8080/api/users/tag/developer

# 删除用户
curl -X DELETE http://localhost:8080/api/users/{id}
```

## Repository方法

### 自动生成的方法

```java
// 根据字段查询
User findByUsername(String username);
List<User> findByEmail(String email);

// 范围查询
List<User> findByAgeBetween(Integer minAge, Integer maxAge);
List<User> findByAgeGreaterThan(Integer age);

// 嵌套字段查询
List<User> findByAddressCity(String city);

// 数组查询
List<User> findByTagsContaining(String tag);

// 模糊查询
List<User> findByUsernameContaining(String username);
```

### 自定义查询

```java
@Query("{ 'age': { $gte: ?0, $lte: ?1 } }")
List<User> findByAgeRange(Integer minAge, Integer maxAge);

@Query("{ 'tags': ?0, 'age': { $gt: ?1 } }")
List<User> findByTagAndMinAge(String tag, Integer minAge);
```

## MongoDB Shell命令

```bash
# 进入MongoDB shell
mongo

# 显示数据库
show dbs

# 切换数据库
use demo

# 显示集合
show collections

# 查询文档
db.users.find()
db.users.find({"age": {$gt: 25}})
db.users.find({"address.city": "北京"})

# 插入文档
db.users.insertOne({
  username: "test",
  email: "test@example.com",
  age: 25
})

# 更新文档
db.users.updateOne(
  {"username": "test"},
  {$set: {"age": 26}}
)

# 删除文档
db.users.deleteOne({"username": "test"})

# 创建索引
db.users.createIndex({"username": 1}, {unique: true})
```

## 聚合操作

```java
// 使用MongoTemplate进行聚合
@Autowired
private MongoTemplate mongoTemplate;

public List<Document> aggregateUsersByCity() {
    Aggregation aggregation = Aggregation.newAggregation(
        Aggregation.group("address.city")
            .count().as("count")
            .avg("age").as("avgAge"),
        Aggregation.sort(Sort.Direction.DESC, "count")
    );
    
    AggregationResults<Document> results = 
        mongoTemplate.aggregate(aggregation, "users", Document.class);
    
    return results.getMappedResults();
}
```

## 生产环境建议

### 1. 连接池配置

```yaml
spring:
  data:
    mongodb:
      uri: mongodb://user:password@host1:27017,host2:27017/dbname?replicaSet=rs0
      connection-pool:
        min-size: 10
        max-size: 100
        max-wait-time: 2000
        max-connection-life-time: 0
```

### 2. 索引优化

```java
@Document(collection = "users")
@CompoundIndex(def = "{'username': 1, 'email': 1}", unique = true)
public class User {
    @Indexed
    private String username;
    
    @Indexed(direction = IndexDirection.DESC)
    private Date createdAt;
}
```

### 3. 事务支持

```java
@Autowired
private MongoTransactionManager transactionManager;

@Transactional
public void transferData(String fromId, String toId) {
    // 事务操作
    User fromUser = userRepository.findById(fromId).orElseThrow();
    User toUser = userRepository.findById(toId).orElseThrow();
    // ...
}
```

## 与关系型数据库对比

| 场景 | 推荐数据库 |
|------|-----------|
| 结构化数据，复杂事务 | 关系型数据库 |
| 快速迭代，灵活Schema | MongoDB |
| 大量读写，水平扩展 | MongoDB |
| 复杂查询，报表分析 | 关系型数据库 |
| 内容管理，文档存储 | MongoDB |

## 学习要点

1. 文档模型的设计原则
2. 嵌套文档 vs DBRef的选择
3. 索引的创建和优化
4. 聚合管道的使用
5. 事务和一致性
6. 分片和集群部署
