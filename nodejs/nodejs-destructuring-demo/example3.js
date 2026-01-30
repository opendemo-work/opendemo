/**
 * example3.js - 综合应用：配置解析与API响应处理
 * 演示解构在真实开发场景中的实用性
 */

// 模拟服务配置对象（可能来自JSON文件或环境变量）
const config = {
  database: {
    host: 'localhost',
    port: 5432,
    username: 'admin',
    password: 'secret'
  },
  server: {
    port: 3000,
    timeout: 5000
  },
  features: {
    logging: true,
    cors: false
  }
};

// 解构配置用于服务启动
const {
  server: { port: serverPort },
  database: { host: dbHost, port: dbPort },
  features: { logging }
} = config;

console.log(`【示例3-配置】启动服务器在端口 ${serverPort}`);
console.log(`【示例3-配置】连接数据库 ${dbHost}:${dbPort}`);
console.log(`【示例3-配置】日志功能：${logging ? '启用' : '禁用'}\n`);

// 模拟API响应数据
const apiResponse = {
  status: 200,
  message: 'success',
  data: {
    users: [
      { id: 1, name: 'Alice' },
      { id: 2, name: 'Bob' }
    ],
    totalCount: 2
  }
};

// 函数：处理API响应（使用解构作为参数）
function handleApiResponse({ status, data: { users, totalCount } }) {
  console.log(`【示例3-API】成功获取${totalCount}位用户，状态码：${status}`);
  users.forEach(({ id, name }) => {
    console.log(`  用户ID: ${id}, 姓名: ${name}`);
  });
}

// 调用函数
handleApiResponse(apiResponse);

// 可选：错误响应处理
const errorResponse = {
  status: 500,
  error: 'Internal Server Error'
};

// 安全解构：提供默认值以应对缺失字段
function safeHandle({ data: { users = [] } = {}, status = 0 } = {}) {
  console.log(`【示例3-安全】处理响应，用户数量：${users.length}，状态：${status}`);
}

safeHandle(errorResponse); // 没有data字段也不会报错