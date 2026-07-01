<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Node.js Express Web框架基础

## 🎯 案例概述

这是一个全面展示Node.js Express Web框架使用的示例，涵盖RESTful API设计、路由配置、中间件使用、错误处理等Web开发核心概念。

## 📚 学习目标

通过本示例你将掌握：
- Express框架的基本使用和配置
- RESTful API设计原则和实现
- 路由系统和参数处理
- 中间件的开发和应用
- 错误处理和异常管理
- Web应用的安全配置

## 🔧 核心知识点

### 1. Express基础配置
- 应用实例创建和基本配置
- 中间件的注册和使用顺序
- 静态文件服务配置
- 请求体解析设置

### 2. RESTful API设计
- HTTP方法的正确使用(GET、POST、PUT、DELETE)
- 资源URI设计规范
- 状态码的合理返回
- 响应数据格式标准化

### 3. 路由系统
- 路由定义和分组管理
- 路径参数和查询参数处理
- 路由级别的中间件应用
- API版本控制实现

### 4. 中间件机制
- 应用级中间件
- 路由级中间件
- 错误处理中间件
- 第三方中间件集成

## 🚀 运行示例

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 启动生产服务器
npm start

# 运行测试
npm test
```

## 📖 代码详解

### 主要类结构

```javascript
class ExpressWebDemo {
    setupMiddleware()      // 中间件配置
    setupRoutes()          // 路由配置
    setupApiRoutes()       // API路由配置
    startServer()          // 服务器启动
}
```

### 关键技术点演示

#### 1. Express应用配置
```javascript
const app = express();

// 安全配置
app.use(helmet());  // 安全头部设置

// CORS配置
app.use(cors({
    origin: ['http://localhost:3000'],
    credentials: true
}));

// 请求解析
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 静态文件服务
app.use('/static', express.static('public'));
```

#### 2. RESTful路由设计
```javascript
// 用户资源API
app.get('/api/v1/users', getUsers);        // 获取用户列表
app.post('/api/v1/users', createUser);     // 创建用户
app.get('/api/v1/users/:id', getUser);     // 获取特定用户
app.put('/api/v1/users/:id', updateUser);  // 更新用户
app.delete('/api/v1/users/:id', deleteUser); // 删除用户
```

#### 3. 中间件应用
```javascript
// 自定义中间件
app.use((req, res, next) => {
    req.requestTime = new Date().toISOString();
    console.log(`${req.method} ${req.path}`);
    next();
});

// 参数验证中间件
app.use('/api/v1/users/:id', (req, res, next) => {
    const userId = parseInt(req.params.id);
    if (isNaN(userId) || userId <= 0) {
        return res.status(400).json({ error: 'Invalid user ID' });
    }
    req.userId = userId;
    next();
});
```

#### 4. 错误处理
```javascript
// 404处理
app.use('*', (req, res) => {
    res.status(404).json({
        error: 'Not Found',
        message: `Route ${req.originalUrl} not found`
    });
});

// 全局错误处理
app.use((err, req, res, next) => {
    console.error('Error:', err.stack);
    res.status(err.status || 500).json({
        error: 'Internal Server Error',
        message: err.message
    });
});
```

## 🧪 测试覆盖

测试文件 `test_express_web.js` 包含以下测试：

✅ 根路径访问测试  
✅ 健康检查测试  
✅ 用户列表获取测试  
✅ 分页功能测试  
✅ 搜索功能测试  
✅ 用户创建测试  
✅ 用户获取测试  
✅ 用户更新测试  
✅ 用户删除测试  
✅ 错误处理测试  
✅ 404处理测试  

## 🎯 实际应用场景

### 1. 用户管理系统API
```javascript
// 完整的用户管理API示例
const userRoutes = express.Router();

// 获取用户列表（支持分页和搜索）
userRoutes.get('/', (req, res) => {
    const { page = 1, limit = 10, search } = req.query;
    // 实现分页和搜索逻辑
});

// 创建用户（带验证）
userRoutes.post('/', [
    validateUserInput,
    checkEmailExists,
    createUser
]);

// 用户详情
userRoutes.get('/:id', validateUserId, getUser);

// 更新用户
userRoutes.put('/:id', validateUserId, updateUser);

// 删除用户
userRoutes.delete('/:id', validateUserId, deleteUser);
```

### 2. 认证中间件
```javascript
// JWT认证中间件
function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];
    
    if (!token) {
        return res.status(401).json({ error: 'Access token required' });
    }
    
    jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
        if (err) {
            return res.status(403).json({ error: 'Invalid token' });
        }
        req.user = user;
        next();
    });
}
```

### 3. 日志和监控
```javascript
// 请求日志中间件
app.use(morgan('combined'));

// 性能监控
app.use((req, res, next) => {
    const start = Date.now();
    res.on('finish', () => {
        const duration = Date.now() - start;
        console.log(`${req.method} ${req.path} - ${duration}ms`);
    });
    next();
});
```

## ⚡ 最佳实践建议

### 1. API设计原则
- 使用名词而非动词表示资源
- 合理使用HTTP状态码
- 保持API版本控制
- 提供一致的错误响应格式

### 2. 安全考虑
- 使用Helmet增强安全性
- 配置适当的CORS策略
- 实施速率限制
- 验证所有输入数据

### 3. 性能优化
- 合理使用缓存策略
- 实施分页和限制查询
- 优化数据库查询
- 使用适当的索引

### 4. 可维护性
- 模块化路由设计
- 统一的错误处理
- 详细的API文档
- 充分的测试覆盖

## 🔍 常见问题和解决方案

### 1. CORS跨域问题
```javascript
// 问题：前端请求被浏览器阻止
// 解决：正确配置CORS
app.use(cors({
    origin: ['http://localhost:3000', 'https://yourdomain.com'],
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization']
}));
```

### 2. 请求体解析问题
```javascript
// 问题：req.body为undefined
// 解决：正确配置body-parser
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));
```

### 3. 异步错误处理
```javascript
// 问题：异步操作中的错误未被捕获
// 解决：使用async/await包装器
function asyncHandler(fn) {
    return (req, res, next) => {
        Promise.resolve(fn(req, res, next)).catch(next);
    };
}

app.get('/users', asyncHandler(async (req, res) => {
    const users = await User.find();
    res.json(users);
}));
```

## 📚 扩展学习资源

### 官方文档
- [Express官方文档](https://expressjs.com/)
- [Node.js HTTP模块](https://nodejs.org/api/http.html)
- [RESTful API设计指南](https://restfulapi.net/)

### 推荐书籍
- 《Node.js实战》
- 《深入浅出Node.js》
- 《Web API的设计与开发》

### 相关技术
- 数据库集成（MongoDB、MySQL）
- 身份认证（JWT、OAuth）
- API文档（Swagger/OpenAPI）
- 测试框架（Jest、Supertest）

## 🔄 版本历史

- v1.0.0 (2024-01-15): 初始版本，包含完整的Express Web框架演示

---
**注意**: Express是Node.js最受欢迎的Web框架，掌握其核心概念对Web开发至关重要。建议结合实际项目练习来加深理解。
## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/demo.sh
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际案例替换
./scripts/demo.sh
```
