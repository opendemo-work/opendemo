// server.js - 主服务器入口文件
// 使用Express启动一个HTTP服务，并集成GraphQL中间件

const express = require('express');
const { graphqlHTTP } = require('express-graphql');
const schema = require('./schema');

// 创建Express应用实例
const app = express();

// 定义端口号
const PORT = process.env.PORT || 4000;

// 挂载GraphQL中间件到 /graphql 路径
// graphiql: true 启用交互式UI，便于开发调试
app.use('/graphql', graphqlHTTP({
  schema: schema,
  graphiql: true, // 开发环境下启用GraphQL Playground
}));

// 启动服务器并监听指定端口
app.listen(PORT, () => {
  console.log(`🚀 Server is running on http://localhost:${PORT}/graphql`);
});

// 注意：生产环境应关闭 graphiql 并添加身份验证和错误处理