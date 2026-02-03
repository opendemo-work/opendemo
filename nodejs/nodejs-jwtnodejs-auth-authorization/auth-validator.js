// auth-validator.js
// JWT令牌验证器和受保护路由示例
// 演示如何验证JWT并保护API端点

// 引入依赖
const express = require('express');
const jwt = require('jsonwebtoken');

// 导入共享的密钥和生成函数
const { generateToken, SECRET_KEY } = require('./auth-generator');

// 创建Express应用
const app = express();
const PORT = 3000;

// 中间件：解析JSON请求体
app.use(express.json());

// 认证中间件 - 验证JWT令牌
const authenticateToken = (req, res, next) => {
  // 从Authorization头获取令牌
  // 格式应为: "Bearer <token>"
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // 提取Bearer后的部分

  // 如果没有提供令牌
  if (!token) {
    return res.status(401).json({ 
      error: '访问被拒绝，缺少令牌' 
    });
  }

  // 验证令牌
  jwt.verify(token, SECRET_KEY, (err, user) => {
    if (err) {
      // 常见错误：令牌过期、签名无效
      return res.status(403).json({ 
        error: '令牌无效或已过期' 
      });
    }
    
    // 将用户信息附加到请求对象，供后续处理函数使用
    req.user = user;
    next(); // 继续执行下一个中间件或路由处理器
  });
};

// 公开路由 - 无需认证
app.get('/public', (req, res) => {
  res.json({ message: '这是公开信息，任何人都可以访问' });
});

// 受保护的路由 - 需要有效JWT令牌
app.get('/protected', authenticateToken, (req, res) => {
  res.json({ 
    message: '访问成功', 
    user: req.user // 包含解码的用户信息
  });
});

// 自动生成测试令牌的端点（仅用于演示，生产环境应移除）
app.get('/generate-token', (req, res) => {
  const token = generateToken();
  res.json({ token });
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`服务器运行在 http://localhost:${PORT}`);
  
  // 自动生成一个令牌供测试使用
  generateToken();
});

// 错误处理中间件
app.use((err, req, res, next) => {
  console.error('服务器错误:', err.stack);
  res.status(500).send('服务器内部错误');
});