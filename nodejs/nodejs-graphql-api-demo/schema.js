// schema.js - 定义GraphQL Schema和解析器
// 包含类型定义（SDL）和数据解析逻辑

const { buildSchema } = require('graphql');

// 使用GraphQL Schema Definition Language (SDL) 定义数据结构
// 定义了User、Post类型及根查询
const schema = buildSchema(`

  # Post 类型：表示一篇文章
  type Post {
    title: String!
    published: Boolean!
  }

  # User 类型：表示一个用户，包含姓名、邮箱和发布的文章列表
  type User {
    id: ID!
    name: String!
    email: String!
    posts: [Post]!
  }

  # Query 根类型：定义可执行的查询操作
  type Query {
    # 查询单个用户，接收id参数，返回User对象
    user(id: Int!): User
  }
`);

// 模拟数据：实际项目中应从数据库获取
const users = [
  {
    id: 1,
    name: 'Alice',
    email: 'alice@example.com',
    posts: [
      { title: '我的第一篇博客', published: true },
      { title: 'GraphQL入门', published: false }
    ]
  },
  {
    id: 2,
    name: 'Bob',
    email: 'bob@example.com',
    posts: [
      { title: 'Node.js技巧', published: true }
    ]
  }
];

// 解析器（Resolvers）：定义每个查询如何获取数据
const resolvers = {
  // 对应Schema中的 user(id: Int): User
  user: ({ id }) => {
    // 查找匹配id的用户，未找到则返回null
    return users.find(user => user.id === id) || null;
  }
};

// 导出Schema对象，供server.js使用
// 注意：buildSchema不直接支持resolvers，因此需手动结合
module.exports = schema;

// 注意：在复杂项目中推荐使用 `graphql-tools` 和 `@graphql-codegen` 进行模块化管理