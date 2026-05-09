# Spring GraphQL 演示

## 学习目标

1. 掌握 Spring GraphQL 核心概念
2. 理解 GraphQL Schema 定义
3. 学会实现 Query 和 Mutation
4. 理解 DataLoader 优化

## 环境要求

- JDK 17+
- Maven 3.9+

## 核心概念

### GraphQL vs REST

```
REST:
GET /users/1        → 返回完整 User
GET /users/1/posts  → 返回 User 的 Posts
GET /users/1/profile → 返回 User 的 Profile

GraphQL:
POST /graphql
{
  user(id: 1) {
    name
    posts { title }
    profile { avatar }
  }
}
```

## 快速开始

```bash
cd spring-graphql-demo
mvn spring-boot:run
```

## GraphQL 端点

```
POST /graphql  # 查询和变更
GET /graphql    # GraphiQL IDE (开发模式)
```

## Schema 定义

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
}

type Query {
  user(id: ID!): User
  users: [User!]!
  post(id: ID!): Post
}

type Mutation {
  createUser(name: String!, email: String!): User!
  createPost(title: String!, content: String!, authorId: ID!): Post!
}
```

## 查询示例

```bash
# 查询单个用户
curl -X POST http://localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ user(id: 1) { name email posts { title } } }"}'

# 创建用户
curl -X POST http://localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { createUser(name: \"张三\", email: \"zhangsan@example.com\") { id name } }"}'
```

---

**技术栈**: Spring Boot 3.2 | Spring GraphQL | GraphQL Java

**版本**: 1.0.0