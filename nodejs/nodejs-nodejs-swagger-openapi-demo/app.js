// app.js - 主服务器文件
// 导入核心模块
const express = require('express');
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');

// 创建Express应用实例
const app = express();
const PORT = process.env.PORT || 3000;

// 加载OpenAPI规范文件（YAML格式）
// 使用YAML可以更清晰地组织复杂的API结构
const swaggerDocument = YAML.load('./api-docs.yaml');

// 挂载Swagger UI中间件到指定路由
// 访问 /api-docs 即可查看交互式API文档
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// 模拟一个简单的用户API端点
// 实际业务逻辑可在此基础上扩展
app.get('/users', (req, res) => {
  res.json({
    success: true,
    data: [
      { id: 1, name: '张三', email: 'zhangsan@example.com' },
      { id: 2, name: '李四', email: 'lisi@example.com' }
    ]
  });
});

// 根路径提示信息
app.get('/', (req, res) => {
  res.send('Welcome to the API! Visit <a href="/api-docs">/api-docs</a> for documentation.');
});

// 启动HTTP服务器
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
  console.log(`Swagger UI available at http://localhost:${PORT}/api-docs`);
});

// 导出app用于测试或其他用途（最佳实践）
module.exports = app;