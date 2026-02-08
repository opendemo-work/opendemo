# Node.js 技术栈命名大全

本文件定义了Node.js技术栈中各类模块、函数、变量等的标准命名规范，特别针对生产环境中的问题排查和解决方案场景。

## 一、项目结构命名规范

### 1.1 目录结构命名
```javascript
// 标准项目结构
project-root/
├── src/                          // 源代码目录
│   ├── controllers/             // 控制器目录
│   │   ├── userController.js    // 用户控制器
│   │   ├── orderController.js   // 订单控制器
│   │   └── authController.js    // 认证控制器
│   ├── services/                // 服务层目录
│   │   ├── userService.js       // 用户服务
│   │   ├── orderService.js      // 订单服务
│   │   └── emailService.js      // 邮件服务
│   ├── models/                  // 数据模型目录
│   │   ├── userModel.js         // 用户模型
│   │   ├── orderModel.js        // 订单模型
│   │   └── productModel.js      // 产品模型
│   ├── routes/                  // 路由目录
│   │   ├── userRoutes.js        // 用户路由
│   │   ├── orderRoutes.js       // 订单路由
│   │   └── apiRoutes.js         // API路由
│   ├── middleware/              // 中间件目录
│   │   ├── authMiddleware.js    // 认证中间件
│   │   ├── validationMiddleware.js // 验证中间件
│   │   └── errorMiddleware.js   // 错误处理中间件
│   ├── utils/                   // 工具函数目录
│   │   ├── logger.js            // 日志工具
│   │   ├── validator.js         // 验证工具
│   │   └── helper.js            // 辅助工具
│   ├── config/                  // 配置目录
│   │   ├── database.js          // 数据库配置
│   │   ├── server.js            // 服务器配置
│   │   └── environment.js       // 环境配置
│   └── app.js                   // 应用入口文件
├── tests/                       // 测试目录
│   ├── unit/                    // 单元测试
│   ├── integration/             // 集成测试
│   └── e2e/                     // 端到端测试
├── docs/                        // 文档目录
├── scripts/                     // 脚本目录
└── package.json                 // 包配置文件
```

### 1.2 文件命名规范
```javascript
// 控制器文件命名
userController.js                // 用户控制器
orderController.js               // 订单控制器
productController.js             // 产品控制器
authController.js                // 认证控制器

// 服务文件命名
userService.js                   // 用户服务
orderService.js                  // 订单服务
paymentService.js                // 支付服务
emailService.js                  // 邮件服务

// 模型文件命名
userModel.js                     // 用户模型
orderModel.js                    // 订单模型
productModel.js                  // 产品模型
categoryModel.js                 // 分类模型

// 路由文件命名
userRoutes.js                    // 用户路由
orderRoutes.js                   // 订单路由
apiRoutes.js                     // API路由
adminRoutes.js                   // 管理路由

// 中间件文件命名
authMiddleware.js                // 认证中间件
validationMiddleware.js          // 验证中间件
errorMiddleware.js               // 错误中间件
loggingMiddleware.js             // 日志中间件
```

## 二、变量和函数命名规范

### 2.1 变量命名
```javascript
// 常量命名 - 全大写加下划线
const MAX_RETRY_ATTEMPTS = 3;
const DEFAULT_PAGE_SIZE = 20;
const API_BASE_URL = 'https://api.example.com';
const DATABASE_CONNECTION_TIMEOUT = 5000;

// 配置变量命名
const config = {
    serverPort: 3000,
    databaseUrl: 'mongodb://localhost:27017/myapp',
    jwtSecret: process.env.JWT_SECRET,
    logLevel: 'info',
    maxFileSize: 10 * 1024 * 1024, // 10MB
};

// 环境变量命名
const env = {
    NODE_ENV: process.env.NODE_ENV || 'development',
    PORT: parseInt(process.env.PORT) || 3000,
    DATABASE_URL: process.env.DATABASE_URL,
    REDIS_URL: process.env.REDIS_URL,
    JWT_SECRET: process.env.JWT_SECRET,
};

// 业务变量命名 - 驼峰命名法
const userController = new UserController();
const orderService = new OrderService();
const productRepository = new ProductRepository();
const emailValidator = new EmailValidator();

// 临时变量命名
const userData = await userService.findById(userId);
const orderList = await orderService.getUserOrders(userId);
const productInfo = await productService.getProductDetails(productId);
const validationErrors = validateUserInput(userData);
```

### 2.2 函数命名
```javascript
// 控制器函数命名 - 动词+名词形式
class UserController {
    async getAllUsers(req, res, next) {
        try {
            const users = await this.userService.findAll();
            res.json({ success: true, data: users });
        } catch (error) {
            next(error);
        }
    }
    
    async getUserById(req, res, next) {
        try {
            const { id } = req.params;
            const user = await this.userService.findById(id);
            if (!user) {
                return res.status(404).json({ 
                    success: false, 
                    message: 'User not found' 
                });
            }
            res.json({ success: true, data: user });
        } catch (error) {
            next(error);
        }
    }
    
    async createUser(req, res, next) {
        try {
            const userData = req.body;
            const newUser = await this.userService.create(userData);
            res.status(201).json({ success: true, data: newUser });
        } catch (error) {
            next(error);
        }
    }
    
    async updateUser(req, res, next) {
        try {
            const { id } = req.params;
            const updateData = req.body;
            const updatedUser = await this.userService.update(id, updateData);
            res.json({ success: true, data: updatedUser });
        } catch (error) {
            next(error);
        }
    }
    
    async deleteUser(req, res, next) {
        try {
            const { id } = req.params;
            await this.userService.delete(id);
            res.json({ success: true, message: 'User deleted successfully' });
        } catch (error) {
            next(error);
        }
    }
}

// 服务层函数命名
class OrderService {
    async createOrder(orderData) {
        // 订单创建逻辑
        const order = await this.orderRepository.create(orderData);
        await this.notificationService.sendOrderConfirmation(order);
        return order;
    }
    
    async processPayment(orderId, paymentData) {
        // 支付处理逻辑
        const order = await this.orderRepository.findById(orderId);
        const paymentResult = await this.paymentGateway.charge(paymentData);
        await this.orderRepository.updateStatus(orderId, 'paid');
        return paymentResult;
    }
    
    async cancelOrder(orderId, reason) {
        // 订单取消逻辑
        const order = await this.orderRepository.findById(orderId);
        await this.inventoryService.restoreStock(order.items);
        await this.orderRepository.updateStatus(orderId, 'cancelled');
        return { success: true, orderId };
    }
    
    async getOrderHistory(userId, filters) {
        // 获取订单历史
        return await this.orderRepository.findByUser(userId, filters);
    }
}

// 工具函数命名
class ValidationUtils {
    static isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    static isValidPhoneNumber(phone) {
        const phoneRegex = /^\+?[\d\s\-\(\)]{10,}$/;
        return phoneRegex.test(phone);
    }
    
    static validatePassword(password) {
        return {
            isValid: password.length >= 8,
            hasUpperCase: /[A-Z]/.test(password),
            hasLowerCase: /[a-z]/.test(password),
            hasNumbers: /\d/.test(password),
            hasSpecialChars: /[!@#$%^&*(),.?":{}|<>]/.test(password)
        };
    }
    
    static sanitizeInput(input) {
        if (typeof input === 'string') {
            return input.trim().replace(/<[^>]*>/g, '');
        }
        return input;
    }
}
```

## 三、类和模块命名规范

### 3.1 类命名
```javascript
// 控制器类命名 - Controller后缀
class UserController {
    constructor(userService) {
        this.userService = userService;
    }
    
    async handleGetAllUsers(req, res) {
        // 处理获取所有用户请求
    }
}

class OrderController {
    constructor(orderService) {
        this.orderService = orderService;
    }
    
    async handleCreateOrder(req, res) {
        // 处理创建订单请求
    }
}

// 服务类命名 - Service后缀
class UserService {
    constructor(userRepository, emailService) {
        this.userRepository = userRepository;
        this.emailService = emailService;
    }
    
    async registerUser(userData) {
        // 用户注册逻辑
    }
}

class PaymentService {
    constructor(paymentGateway) {
        this.paymentGateway = paymentGateway;
    }
    
    async processPayment(paymentData) {
        // 支付处理逻辑
    }
}

// 数据访问类命名 - Repository后缀
class UserRepository {
    constructor(database) {
        this.database = database;
    }
    
    async findById(id) {
        // 查找用户逻辑
    }
}

class OrderRepository {
    constructor(database) {
        this.database = database;
    }
    
    async create(orderData) {
        // 创建订单逻辑
    }
}

// 中间件类命名 - Middleware后缀
class AuthMiddleware {
    constructor(jwtService) {
        this.jwtService = jwtService;
    }
    
    authenticate(req, res, next) {
        // 认证逻辑
    }
}

class ValidationMiddleware {
    validateUserInput(req, res, next) {
        // 输入验证逻辑
    }
}
```

### 3.2 模块导出命名
```javascript
// 单个导出
module.exports = class UserService {
    // 用户服务实现
};

// 多个导出
module.exports = {
    UserService: require('./userService'),
    OrderService: require('./orderService'),
    EmailService: require('./emailService')
};

// 默认导出
exports.default = class MainController {
    // 主控制器
};

// 具名导出
exports.createUser = async (req, res) => {
    // 创建用户逻辑
};

exports.getUserById = async (req, res) => {
    // 获取用户逻辑
};
```

## 四、路由和API命名规范

### 4.1 路由定义
```javascript
// 用户路由定义
const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');

// RESTful路由命名
router.get('/', userController.getAllUsers);           // 获取所有用户
router.get('/:id', userController.getUserById);        // 根据ID获取用户
router.post('/', userController.createUser);           // 创建用户
router.put('/:id', userController.updateUser);         // 更新用户
router.delete('/:id', userController.deleteUser);      // 删除用户
router.patch('/:id/status', userController.updateUserStatus); // 部分更新用户状态

// 订单路由定义
const orderRouter = express.Router();
const orderController = require('../controllers/orderController');

orderRouter.post('/', orderController.createOrder);              // 创建订单
orderRouter.get('/user/:userId', orderController.getUserOrders); // 获取用户订单
orderRouter.get('/:id', orderController.getOrderById);           // 获取订单详情
orderRouter.put('/:id/cancel', orderController.cancelOrder);     // 取消订单
orderRouter.post('/:id/payment', orderController.processPayment); // 处理支付

// API版本控制
const v1Router = express.Router();
v1Router.use('/users', require('./userRoutes'));
v1Router.use('/orders', require('./orderRoutes'));
v1Router.use('/products', require('./productRoutes'));

// 主应用路由
const app = express();
app.use('/api/v1', v1Router);
app.use('/api/v2', require('./routes/v2')); // 未来版本
```

### 4.2 API响应格式
```javascript
// 统一响应格式
class ApiResponse {
    static success(data, message = 'Success') {
        return {
            success: true,
            message,
            data,
            timestamp: new Date().toISOString()
        };
    }
    
    static error(message, code = 500, details = null) {
        return {
            success: false,
            message,
            code,
            details,
            timestamp: new Date().toISOString()
        };
    }
    
    static pagination(data, paginationInfo) {
        return {
            success: true,
            message: 'Success',
            data,
            pagination: paginationInfo,
            timestamp: new Date().toISOString()
        };
    }
}

// 使用示例
app.get('/api/users', async (req, res) => {
    try {
        const { page = 1, limit = 10 } = req.query;
        const users = await userService.getUsers({ page, limit });
        const totalCount = await userService.getUserCount();
        
        const paginationInfo = {
            currentPage: parseInt(page),
            totalPages: Math.ceil(totalCount / limit),
            totalCount,
            hasNext: page * limit < totalCount,
            hasPrev: page > 1
        };
        
        res.json(ApiResponse.pagination(users, paginationInfo));
    } catch (error) {
        res.status(500).json(ApiResponse.error('Failed to fetch users', 500));
    }
});
```

## 五、错误处理命名规范

### 5.1 自定义错误类
```javascript
// 基础错误类
class AppError extends Error {
    constructor(message, statusCode, isOperational = true) {
        super(message);
        this.statusCode = statusCode;
        this.isOperational = isOperational;
        this.timestamp = new Date().toISOString();
        
        Error.captureStackTrace(this, this.constructor);
    }
}

// 业务错误类
class ValidationError extends AppError {
    constructor(message, field = null) {
        super(message, 400);
        this.field = field;
        this.errorCode = 'VALIDATION_ERROR';
    }
}

class AuthenticationError extends AppError {
    constructor(message = 'Authentication failed') {
        super(message, 401);
        this.errorCode = 'AUTHENTICATION_ERROR';
    }
}

class AuthorizationError extends AppError {
    constructor(message = 'Insufficient permissions') {
        super(message, 403);
        this.errorCode = 'AUTHORIZATION_ERROR';
    }
}

class NotFoundError extends AppError {
    constructor(resource = 'Resource') {
        super(`${resource} not found`, 404);
        this.errorCode = 'NOT_FOUND_ERROR';
    }
}

class BusinessLogicError extends AppError {
    constructor(message, errorCode) {
        super(message, 422); // Unprocessable Entity
        this.errorCode = errorCode;
    }
}

// 数据库错误类
class DatabaseError extends AppError {
    constructor(message, originalError = null) {
        super(message, 500);
        this.errorCode = 'DATABASE_ERROR';
        this.originalError = originalError;
    }
}

// 外部服务错误类
class ExternalServiceError extends AppError {
    constructor(serviceName, message, originalError = null) {
        super(`External service error: ${serviceName} - ${message}`, 502);
        this.errorCode = 'EXTERNAL_SERVICE_ERROR';
        this.serviceName = serviceName;
        this.originalError = originalError;
    }
}
```

### 5.2 错误处理中间件
```javascript
// 全局错误处理中间件
const globalErrorHandler = (err, req, res, next) => {
    // 记录错误日志
    logger.error('Global error handler caught:', {
        message: err.message,
        stack: err.stack,
        url: req.url,
        method: req.method,
        userId: req.user?.id,
        timestamp: new Date().toISOString()
    });
    
    // 设置默认值
    err.statusCode = err.statusCode || 500;
    err.message = err.message || 'Internal Server Error';
    
    // 生产环境不暴露错误细节
    const isProduction = process.env.NODE_ENV === 'production';
    
    // 操作性错误处理
    if (err.isOperational) {
        return res.status(err.statusCode).json({
            success: false,
            message: err.message,
            ...(isProduction ? {} : { stack: err.stack }),
            errorCode: err.errorCode,
            timestamp: err.timestamp
        });
    }
    
    // 编程错误处理
    if (!isProduction) {
        console.error('Programming error:', err);
    }
    
    // 返回通用错误响应
    return res.status(500).json({
        success: false,
        message: isProduction ? 'Something went wrong!' : err.message,
        ...(isProduction ? {} : { stack: err.stack }),
        timestamp: new Date().toISOString()
    });
};

// 特定错误处理中间件
const handleValidationError = (err, req, res, next) => {
    if (err instanceof ValidationError) {
        return res.status(400).json({
            success: false,
            message: err.message,
            errorCode: err.errorCode,
            field: err.field,
            timestamp: err.timestamp
        });
    }
    next(err);
};

const handleAuthenticationError = (err, req, res, next) => {
    if (err instanceof AuthenticationError) {
        return res.status(401).json({
            success: false,
            message: err.message,
            errorCode: err.errorCode,
            timestamp: err.timestamp
        });
    }
    next(err);
};

// 应用错误处理中间件
app.use(handleValidationError);
app.use(handleAuthenticationError);
app.use(globalErrorHandler);
```

## 六、配置和环境变量命名

### 6.1 配置文件结构
```javascript
// config/index.js - 配置入口文件
const environment = process.env.NODE_ENV || 'development';
const config = require(`./${environment}`);

module.exports = {
    ...config,
    environment,
    isDevelopment: environment === 'development',
    isProduction: environment === 'production',
    isTest: environment === 'test'
};

// config/development.js - 开发环境配置
module.exports = {
    server: {
        port: parseInt(process.env.PORT) || 3000,
        host: process.env.HOST || 'localhost'
    },
    
    database: {
        url: process.env.DATABASE_URL || 'mongodb://localhost:27017/dev_database',
        options: {
            useNewUrlParser: true,
            useUnifiedTopology: true
        }
    },
    
    redis: {
        host: process.env.REDIS_HOST || 'localhost',
        port: parseInt(process.env.REDIS_PORT) || 6379,
        password: process.env.REDIS_PASSWORD
    },
    
    jwt: {
        secret: process.env.JWT_SECRET || 'dev_jwt_secret',
        expiresIn: process.env.JWT_EXPIRES_IN || '24h'
    },
    
    email: {
        host: process.env.EMAIL_HOST || 'smtp.gmail.com',
        port: parseInt(process.env.EMAIL_PORT) || 587,
        secure: false,
        auth: {
            user: process.env.EMAIL_USER,
            pass: process.env.EMAIL_PASS
        }
    },
    
    logging: {
        level: process.env.LOG_LEVEL || 'debug',
        format: 'combined'
    }
};

// config/production.js - 生产环境配置
module.exports = {
    server: {
        port: parseInt(process.env.PORT) || 80,
        host: process.env.HOST || '0.0.0.0'
    },
    
    database: {
        url: process.env.DATABASE_URL,
        options: {
            useNewUrlParser: true,
            useUnifiedTopology: true,
            ssl: true,
            maxPoolSize: 100,
            serverSelectionTimeoutMS: 5000
        }
    },
    
    redis: {
        host: process.env.REDIS_HOST,
        port: parseInt(process.env.REDIS_PORT) || 6379,
        password: process.env.REDIS_PASSWORD,
        tls: true
    },
    
    jwt: {
        secret: process.env.JWT_SECRET,
        expiresIn: process.env.JWT_EXPIRES_IN || '24h'
    },
    
    email: {
        host: process.env.EMAIL_HOST,
        port: parseInt(process.env.EMAIL_PORT) || 465,
        secure: true,
        auth: {
            user: process.env.EMAIL_USER,
            pass: process.env.EMAIL_PASS
        }
    },
    
    logging: {
        level: process.env.LOG_LEVEL || 'info',
        format: 'json',
        transports: ['file', 'console']
    }
};
```

### 6.2 环境变量验证
```javascript
// utils/envValidator.js - 环境变量验证工具
const Joi = require('joi');

const envSchema = Joi.object({
    NODE_ENV: Joi.string()
        .valid('development', 'production', 'test')
        .default('development'),
    
    PORT: Joi.number()
        .port()
        .default(3000),
    
    DATABASE_URL: Joi.string()
        .uri({ scheme: ['mongodb', 'postgresql', 'mysql'] })
        .required(),
    
    REDIS_HOST: Joi.string()
        .hostname()
        .when('NODE_ENV', {
            is: 'production',
            then: Joi.required(),
            otherwise: Joi.optional()
        }),
    
    REDIS_PORT: Joi.number()
        .port()
        .default(6379),
    
    JWT_SECRET: Joi.string()
        .min(32)
        .required(),
    
    JWT_EXPIRES_IN: Joi.string()
        .pattern(/^(\d+[smhdw])$/)
        .default('24h'),
    
    EMAIL_HOST: Joi.string()
        .hostname()
        .required(),
    
    EMAIL_PORT: Joi.number()
        .port()
        .default(587),
    
    EMAIL_USER: Joi.string()
        .email()
        .required(),
    
    EMAIL_PASS: Joi.string()
        .required(),
    
    LOG_LEVEL: Joi.string()
        .valid('error', 'warn', 'info', 'debug')
        .default('info')
}).unknown();

class EnvironmentValidator {
    static validate() {
        const { error, value } = envSchema.validate(process.env, {
            abortEarly: false,
            stripUnknown: true
        });
        
        if (error) {
            const errorMessage = error.details
                .map(detail => `${detail.path.join('.')}: ${detail.message}`)
                .join('\n');
            
            throw new Error(`Environment validation failed:\n${errorMessage}`);
        }
        
        // 将验证后的值赋回process.env
        Object.assign(process.env, value);
        
        return value;
    }
    
    static getDatabaseConfig() {
        return {
            url: process.env.DATABASE_URL,
            options: {
                useNewUrlParser: true,
                useUnifiedTopology: true,
                ...(process.env.NODE_ENV === 'production' ? {
                    ssl: true,
                    maxPoolSize: 100
                } : {})
            }
        };
    }
    
    static getJwtConfig() {
        return {
            secret: process.env.JWT_SECRET,
            expiresIn: process.env.JWT_EXPIRES_IN
        };
    }
}

module.exports = EnvironmentValidator;
```

## 七、测试相关命名规范

### 7.1 测试文件命名
```javascript
// 单元测试文件命名 - .test.js后缀
userController.test.js           // 用户控制器测试
orderService.test.js             // 订单服务测试
validationUtils.test.js          // 验证工具测试
database.test.js                 // 数据库测试

// 集成测试文件命名 - .integration.test.js后缀
user.integration.test.js         // 用户集成测试
order.integration.test.js        // 订单集成测试
payment.integration.test.js      // 支付集成测试

// 端到端测试文件命名 - .e2e.test.js后缀
user.e2e.test.js                 // 用户端到端测试
order.e2e.test.js                // 订单端到端测试
api.e2e.test.js                  // API端到端测试
```

### 7.2 测试用例命名
```javascript
// 使用describe和it的测试结构
describe('UserController', () => {
    describe('getAllUsers', () => {
        it('should return all users when successful', async () => {
            // 测试逻辑
        });
        
        it('should return empty array when no users exist', async () => {
            // 测试逻辑
        });
        
        it('should handle database errors gracefully', async () => {
            // 测试逻辑
        });
    });
    
    describe('getUserById', () => {
        it('should return user when valid id provided', async () => {
            // 测试逻辑
        });
        
        it('should return 404 when user not found', async () => {
            // 测试逻辑
        });
        
        it('should validate user id format', async () => {
            // 测试逻辑
        });
    });
});

describe('OrderService', () => {
    describe('createOrder', () => {
        it('should create order successfully with valid data', async () => {
            // 测试逻辑
        });
        
        it('should validate required order fields', async () => {
            // 测试逻辑
        });
        
        it('should handle inventory shortage', async () => {
            // 测试逻辑
        });
        
        it('should send confirmation email after creation', async () => {
            // 测试逻辑
        });
    });
});
```

## 八、日志和监控命名规范

### 8.1 日志记录
```javascript
// utils/logger.js - 日志工具
const winston = require('winston');
const path = require('path');

// 定义日志级别
const levels = {
    error: 0,
    warn: 1,
    info: 2,
    http: 3,
    debug: 4
};

// 定义日志颜色
const colors = {
    error: 'red',
    warn: 'yellow',
    info: 'green',
    http: 'magenta',
    debug: 'white'
};

winston.addColors(colors);

// 定义日志格式
const format = winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss:ms' }),
    winston.format.errors({ stack: true }),
    winston.format.splat(),
    winston.format.json()
);

// 定义传输方式
const transports = [
    // 控制台输出
    new winston.transports.Console({
        format: winston.format.combine(
            winston.format.colorize({ all: true }),
            winston.format.printf(
                (info) => `${info.timestamp} ${info.level}: ${info.message}`
            )
        )
    }),
    
    // 错误日志文件
    new winston.transports.File({
        filename: path.join(__dirname, '../logs/error.log'),
        level: 'error',
        format
    }),
    
    // 组合日志文件
    new winston.transports.File({
        filename: path.join(__dirname, '../logs/combined.log'),
        format
    })
];

// 创建logger实例
const logger = winston.createLogger({
    level: process.env.LOG_LEVEL || 'info',
    levels,
    format,
    transports
});

// 在开发环境中添加更详细的日志
if (process.env.NODE_ENV !== 'production') {
    transports.push(
        new winston.transports.File({
            filename: path.join(__dirname, '../logs/debug.log'),
            level: 'debug',
            format
        })
    );
}

module.exports = logger;

// 使用示例
const logger = require('./utils/logger');

// 不同级别的日志记录
logger.error('Database connection failed', {
    error: dbError.message,
    stack: dbError.stack,
    connectionString: dbConfig.url
});

logger.warn('High memory usage detected', {
    currentUsage: process.memoryUsage(),
    threshold: '80%'
});

logger.info('User registered successfully', {
    userId: newUser.id,
    email: newUser.email,
    registrationMethod: 'email'
});

logger.debug('Processing request', {
    requestId: req.id,
    method: req.method,
    url: req.url,
    userAgent: req.get('User-Agent')
});
```

### 8.2 监控指标收集
```javascript
// utils/metrics.js - 监控指标收集
const prometheus = require('prom-client');

// 创建注册表
const register = new prometheus.Registry();

// HTTP请求指标
const httpRequestDuration = new prometheus.Histogram({
    name: 'http_request_duration_seconds',
    help: 'Duration of HTTP requests in seconds',
    labelNames: ['method', 'route', 'status_code'],
    buckets: [0.1, 0.5, 1, 2, 5, 10]
});

const httpRequestTotal = new prometheus.Counter({
    name: 'http_requests_total',
    help: 'Total number of HTTP requests',
    labelNames: ['method', 'route', 'status_code']
});

// 业务指标
const userRegistrations = new prometheus.Counter({
    name: 'user_registrations_total',
    help: 'Total number of user registrations',
    labelNames: ['source']
});

const orderCreations = new prometheus.Counter({
    name: 'order_creations_total',
    help: 'Total number of order creations',
    labelNames: ['order_type']
});

const paymentProcessing = new prometheus.Histogram({
    name: 'payment_processing_duration_seconds',
    help: 'Duration of payment processing in seconds',
    labelNames: ['payment_method', 'status'],
    buckets: [0.1, 0.5, 1, 2, 5]
});

// 系统指标
const activeUsers = new prometheus.Gauge({
    name: 'active_users_count',
    help: 'Number of currently active users'
});

const databaseConnections = new prometheus.Gauge({
    name: 'database_connections_count',
    help: 'Number of active database connections',
    labelNames: ['state']
});

// 注册所有指标
register.registerMetric(httpRequestDuration);
register.registerMetric(httpRequestTotal);
register.registerMetric(userRegistrations);
register.registerMetric(orderCreations);
register.registerMetric(paymentProcessing);
register.registerMetric(activeUsers);
register.registerMetric(databaseConnections);

// 中间件收集HTTP指标
const metricsMiddleware = (req, res, next) => {
    const start = Date.now();
    
    res.on('finish', () => {
        const duration = (Date.now() - start) / 1000;
        const route = req.route ? req.route.path : req.path;
        
        httpRequestDuration
            .labels(req.method, route, res.statusCode)
            .observe(duration);
            
        httpRequestTotal
            .labels(req.method, route, res.statusCode)
            .inc();
    });
    
    next();
};

// 导出指标和中间件
module.exports = {
    register,
    metricsMiddleware,
    userRegistrations,
    orderCreations,
    paymentProcessing,
    activeUsers,
    databaseConnections
};

// 在应用中使用
const express = require('express');
const { metricsMiddleware, register } = require('./utils/metrics');

const app = express();

// 使用指标中间件
app.use(metricsMiddleware);

// 暴露指标端点
app.get('/metrics', async (req, res) => {
    res.set('Content-Type', register.contentType);
    res.end(await register.metrics());
});
```

## 九、最佳实践示例

### 9.1 生产环境应用模板
```javascript
// app.js - 生产环境应用入口
const express = require('express');
const helmet = require('helmet');
const compression = require('compression');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const morgan = require('morgan');
const { errors } = require('celebrate');

// 自定义模块导入
const config = require('./config');
const logger = require('./utils/logger');
const { metricsMiddleware } = require('./utils/metrics');
const EnvironmentValidator = require('./utils/envValidator');

// 路由导入
const userRoutes = require('./routes/userRoutes');
const orderRoutes = require('./routes/orderRoutes');
const authRoutes = require('./routes/authRoutes');

// 错误处理中间件
const { 
    handleValidationError, 
    handleAuthenticationError,
    globalErrorHandler 
} = require('./middleware/errorHandler');

class Application {
    constructor() {
        this.app = express();
        this.setupMiddleware();
        this.setupRoutes();
        this.setupErrorHandling();
    }
    
    setupMiddleware() {
        // 安全中间件
        this.app.use(helmet({
            contentSecurityPolicy: {
                directives: {
                    defaultSrc: ["'self'"],
                    styleSrc: ["'self'", "'unsafe-inline'"],
                    scriptSrc: ["'self'"],
                    imgSrc: ["'self'", "data:", "https:"]
                }
            }
        }));
        
        // CORS配置
        this.app.use(cors({
            origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
            credentials: true
        }));
        
        // 压缩中间件
        this.app.use(compression());
        
        // 速率限制
        this.app.use('/api/', rateLimit({
            windowMs: 15 * 60 * 1000, // 15分钟
            max: 100, // 限制每个IP 100个请求
            message: {
                success: false,
                message: 'Too many requests from this IP, please try again later.'
            },
            standardHeaders: true,
            legacyHeaders: false
        }));
        
        // 日志中间件
        this.app.use(morgan('combined', {
            stream: {
                write: (message) => logger.http(message.trim())
            }
        }));
        
        // 监控指标中间件
        this.app.use(metricsMiddleware);
        
        // 请求解析中间件
        this.app.use(express.json({ limit: '10mb' }));
        this.app.use(express.urlencoded({ extended: true, limit: '10mb' }));
        
        // 静态文件服务
        this.app.use(express.static('public'));
    }
    
    setupRoutes() {
        // 健康检查端点
        this.app.get('/health', (req, res) => {
            res.json({
                status: 'OK',
                timestamp: new Date().toISOString(),
                uptime: process.uptime()
            });
        });
        
        // API路由
        this.app.use('/api/v1/users', userRoutes);
        this.app.use('/api/v1/orders', orderRoutes);
        this.app.use('/api/v1/auth', authRoutes);
        
        // 404处理
        this.app.use('*', (req, res) => {
            res.status(404).json({
                success: false,
                message: 'Route not found'
            });
        });
    }
    
    setupErrorHandling() {
        // Celebrate验证错误处理
        this.app.use(errors());
        
        // 自定义错误处理中间件
        this.app.use(handleValidationError);
        this.app.use(handleAuthenticationError);
        this.app.use(globalErrorHandler);
    }
    
    async start() {
        try {
            // 验证环境变量
            EnvironmentValidator.validate();
            
            // 数据库连接
            const database = require('./config/database');
            await database.connect();
            
            // 启动服务器
            const server = this.app.listen(config.server.port, config.server.host, () => {
                logger.info(`Server running on ${config.server.host}:${config.server.port}`);
                logger.info(`Environment: ${config.environment}`);
            });
            
            // 优雅关闭
            process.on('SIGTERM', () => {
                logger.info('SIGTERM received, shutting down gracefully');
                server.close(() => {
                    logger.info('Process terminated');
                    process.exit(0);
                });
            });
            
            process.on('SIGINT', () => {
                logger.info('SIGINT received, shutting down gracefully');
                server.close(() => {
                    logger.info('Process terminated');
                    process.exit(0);
                });
            });
            
        } catch (error) {
            logger.error('Failed to start application:', error);
            process.exit(1);
        }
    }
}

// 启动应用
const app = new Application();
app.start();

module.exports = app.app;
```

### 9.2 配置管理最佳实践
```javascript
// config/database.js - 数据库配置管理
const mongoose = require('mongoose');
const logger = require('../utils/logger');

class DatabaseManager {
    constructor() {
        this.connection = null;
        this.isConnected = false;
    }
    
    async connect() {
        try {
            const options = {
                useNewUrlParser: true,
                useUnifiedTopology: true,
                maxPoolSize: process.env.DB_POOL_SIZE || 10,
                serverSelectionTimeoutMS: process.env.DB_TIMEOUT || 5000,
                socketTimeoutMS: 45000,
                family: 4 // Use IPv4, skip trying IPv6
            };
            
            // 生产环境额外配置
            if (process.env.NODE_ENV === 'production') {
                options.ssl = true;
                options.tlsAllowInvalidCertificates = false;
            }
            
            this.connection = await mongoose.connect(process.env.DATABASE_URL, options);
            this.isConnected = true;
            
            logger.info('Database connected successfully');
            
            // 连接事件监听
            mongoose.connection.on('connected', () => {
                logger.info('Mongoose connected to database');
            });
            
            mongoose.connection.on('error', (err) => {
                logger.error('Mongoose connection error:', err);
            });
            
            mongoose.connection.on('disconnected', () => {
                logger.warn('Mongoose disconnected from database');
                this.isConnected = false;
            });
            
            // 监听进程退出事件
            process.on('SIGINT', async () => {
                await mongoose.connection.close();
                logger.info('Mongoose connection closed due to app termination');
                process.exit(0);
            });
            
        } catch (error) {
            logger.error('Database connection failed:', error);
            throw error;
        }
    }
    
    async disconnect() {
        if (this.connection) {
            await mongoose.connection.close();
            this.isConnected = false;
            logger.info('Database disconnected');
        }
    }
    
    getConnectionStatus() {
        return {
            isConnected: this.isConnected,
            readyState: mongoose.connection.readyState,
            host: mongoose.connection.host,
            port: mongoose.connection.port,
            name: mongoose.connection.name
        };
    }
}

module.exports = new DatabaseManager();
```

---

**注意事项：**
1. 遵循JavaScript/Node.js社区的命名约定和最佳实践
2. 错误处理应该分层且具体，提供有意义的错误信息
3. 生产环境中必须包含完善的日志记录和监控指标
4. API设计应该遵循RESTful原则和一致性
5. 配置管理应该支持多环境和外部化配置