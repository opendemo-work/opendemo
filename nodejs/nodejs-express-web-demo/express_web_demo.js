#!/usr/bin/env node
/**
 * Node.js Express Web框架基础演示程序
 * 展示RESTful API、路由、中间件、错误处理等Web开发核心概念
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');

console.log('\n🌐 Node.js Express Web框架基础演示\n');
console.log('=' .repeat(50));

class ExpressWebDemo {
    constructor() {
        this.app = express();
        this.port = process.env.PORT || 3000;
        this.setupMiddleware();
        this.setupRoutes();
        console.log('初始化Express Web演示环境...\n');
    }

    /**
     * 配置中间件
     */
    setupMiddleware() {
        // 安全中间件
        this.app.use(helmet());
        
        // CORS中间件
        this.app.use(cors({
            origin: ['http://localhost:3000', 'http://127.0.0.1:3000'],
            credentials: true
        }));
        
        // 日志中间件
        this.app.use(morgan('combined'));
        
        // 解析JSON请求体
        this.app.use(express.json({ limit: '10mb' }));
        this.app.use(express.urlencoded({ extended: true, limit: '10mb' }));
        
        // 静态文件服务
        this.app.use('/static', express.static('public'));
        
        // 自定义中间件演示
        this.setupCustomMiddleware();
    }

    /**
     * 自定义中间件
     */
    setupCustomMiddleware() {
        // 请求时间记录中间件
        this.app.use((req, res, next) => {
            req.requestTime = new Date().toISOString();
            console.log(`[${req.requestTime}] ${req.method} ${req.path}`);
            next();
        });

        // API版本检查中间件
        this.app.use('/api/v1', (req, res, next) => {
            req.apiVersion = 'v1';
            next();
        });

        // 请求验证中间件
        this.app.use('/api/v1/users/:id', (req, res, next) => {
            const userId = parseInt(req.params.id);
            if (isNaN(userId) || userId <= 0) {
                return res.status(400).json({
                    error: 'Invalid user ID',
                    message: 'User ID must be a positive integer'
                });
            }
            req.userId = userId;
            next();
        });
    }

    /**
     * 配置路由
     */
    setupRoutes() {
        // 根路径
        this.app.get('/', (req, res) => {
            res.json({
                message: '欢迎来到Express Web演示!',
                timestamp: req.requestTime,
                endpoints: {
                    'GET /': '当前页面',
                    'GET /api/v1/users': '获取用户列表',
                    'POST /api/v1/users': '创建新用户',
                    'GET /api/v1/users/:id': '获取指定用户',
                    'PUT /api/v1/users/:id': '更新用户信息',
                    'DELETE /api/v1/users/:id': '删除用户',
                    'GET /health': '健康检查'
                }
            });
        });

        // 健康检查端点
        this.app.get('/health', (req, res) => {
            res.json({
                status: 'healthy',
                timestamp: new Date().toISOString(),
                uptime: process.uptime()
            });
        });

        // API路由组
        this.setupApiRoutes();

        // 404处理
        this.app.use('*', (req, res) => {
            res.status(404).json({
                error: 'Not Found',
                message: `Route ${req.originalUrl} not found`,
                timestamp: new Date().toISOString()
            });
        });

        // 全局错误处理中间件
        this.app.use((err, req, res, next) => {
            console.error('Error:', err.stack);
            res.status(err.status || 500).json({
                error: 'Internal Server Error',
                message: err.message || 'Something went wrong!',
                timestamp: new Date().toISOString()
            });
        });
    }

    /**
     * API路由配置
     */
    setupApiRoutes() {
        const router = express.Router();

        // 模拟数据存储
        const users = [
            { id: 1, name: '张三', email: 'zhangsan@example.com', age: 25 },
            { id: 2, name: '李四', email: 'lisi@example.com', age: 30 },
            { id: 3, name: '王五', email: 'wangwu@example.com', age: 28 }
        ];

        // GET /api/v1/users - 获取所有用户
        router.get('/users', (req, res) => {
            const { page = 1, limit = 10, search } = req.query;
            let filteredUsers = [...users];

            // 搜索功能
            if (search) {
                filteredUsers = filteredUsers.filter(user =>
                    user.name.includes(search) || user.email.includes(search)
                );
            }

            // 分页
            const startIndex = (page - 1) * limit;
            const endIndex = page * limit;
            const paginatedUsers = filteredUsers.slice(startIndex, endIndex);

            res.json({
                data: paginatedUsers,
                pagination: {
                    currentPage: parseInt(page),
                    totalPages: Math.ceil(filteredUsers.length / limit),
                    totalItems: filteredUsers.length,
                    itemsPerPage: parseInt(limit)
                },
                apiVersion: req.apiVersion,
                timestamp: req.requestTime
            });
        });

        // POST /api/v1/users - 创建新用户
        router.post('/users', (req, res) => {
            const { name, email, age } = req.body;

            // 验证必需字段
            if (!name || !email) {
                return res.status(400).json({
                    error: 'Bad Request',
                    message: 'Name and email are required'
                });
            }

            // 验证邮箱格式
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                return res.status(400).json({
                    error: 'Bad Request',
                    message: 'Invalid email format'
                });
            }

            // 检查邮箱是否已存在
            if (users.some(user => user.email === email)) {
                return res.status(409).json({
                    error: 'Conflict',
                    message: 'Email already exists'
                });
            }

            // 创建新用户
            const newUser = {
                id: users.length + 1,
                name,
                email,
                age: age || null
            };

            users.push(newUser);

            res.status(201).json({
                message: 'User created successfully',
                data: newUser,
                apiVersion: req.apiVersion,
                timestamp: req.requestTime
            });
        });

        // GET /api/v1/users/:id - 获取指定用户
        router.get('/users/:id', (req, res) => {
            const user = users.find(u => u.id === req.userId);
            
            if (!user) {
                return res.status(404).json({
                    error: 'Not Found',
                    message: `User with ID ${req.userId} not found`
                });
            }

            res.json({
                data: user,
                apiVersion: req.apiVersion,
                timestamp: req.requestTime
            });
        });

        // PUT /api/v1/users/:id - 更新用户信息
        router.put('/users/:id', (req, res) => {
            const userIndex = users.findIndex(u => u.id === req.userId);
            
            if (userIndex === -1) {
                return res.status(404).json({
                    error: 'Not Found',
                    message: `User with ID ${req.userId} not found`
                });
            }

            const { name, email, age } = req.body;
            
            // 如果提供了邮箱，检查是否与其他用户冲突
            if (email && email !== users[userIndex].email) {
                if (users.some((u, index) => u.email === email && index !== userIndex)) {
                    return res.status(409).json({
                        error: 'Conflict',
                        message: 'Email already exists'
                    });
                }
            }

            // 更新用户信息
            if (name) users[userIndex].name = name;
            if (email) users[userIndex].email = email;
            if (age !== undefined) users[userIndex].age = age;

            res.json({
                message: 'User updated successfully',
                data: users[userIndex],
                apiVersion: req.apiVersion,
                timestamp: req.requestTime
            });
        });

        // DELETE /api/v1/users/:id - 删除用户
        router.delete('/users/:id', (req, res) => {
            const userIndex = users.findIndex(u => u.id === req.userId);
            
            if (userIndex === -1) {
                return res.status(404).json({
                    error: 'Not Found',
                    message: `User with ID ${req.userId} not found`
                });
            }

            const deletedUser = users.splice(userIndex, 1)[0];

            res.json({
                message: 'User deleted successfully',
                data: deletedUser,
                apiVersion: req.apiVersion,
                timestamp: req.requestTime
            });
        });

        // 挂载API路由
        this.app.use('/api/v1', router);
    }

    /**
     * 启动服务器
     */
    startServer() {
        this.server = this.app.listen(this.port, () => {
            console.log(`🚀 Express服务器启动成功!`);
            console.log(`📍 服务器地址: http://localhost:${this.port}`);
            console.log(`📅 启动时间: ${new Date().toLocaleString()}`);
            console.log(`🔧 API文档: http://localhost:${this.port}/`);
            console.log(`❤️  健康检查: http://localhost:${this.port}/health`);
            console.log('\n' + '=' .repeat(50));
        });

        // 优雅关闭
        process.on('SIGTERM', () => {
            console.log('收到SIGTERM信号，正在关闭服务器...');
            this.server.close(() => {
                console.log('服务器已关闭');
                process.exit(0);
            });
        });

        process.on('SIGINT', () => {
            console.log('收到SIGINT信号，正在关闭服务器...');
            this.server.close(() => {
                console.log('服务器已关闭');
                process.exit(0);
            });
        });
    }

    /**
     * 运行演示
     */
    runDemo() {
        try {
            this.startServer();
            this.showUsageInstructions();
        } catch (error) {
            console.error('❌ 服务器启动失败:', error);
            process.exit(1);
        }
    }

    /**
     * 显示使用说明
     */
    showUsageInstructions() {
        console.log('\n📋 API使用说明:');
        console.log('-'.repeat(30));
        console.log('1. 获取用户列表:');
        console.log('   GET http://localhost:3000/api/v1/users');
        console.log('   GET http://localhost:3000/api/v1/users?page=1&limit=5&search=张');
        console.log('');
        console.log('2. 创建用户:');
        console.log('   POST http://localhost:3000/api/v1/users');
        console.log('   Body: {"name": "新用户", "email": "new@example.com", "age": 25}');
        console.log('');
        console.log('3. 获取用户详情:');
        console.log('   GET http://localhost:3000/api/v1/users/1');
        console.log('');
        console.log('4. 更新用户:');
        console.log('   PUT http://localhost:3000/api/v1/users/1');
        console.log('   Body: {"name": "更新的名称", "age": 30}');
        console.log('');
        console.log('5. 删除用户:');
        console.log('   DELETE http://localhost:3000/api/v1/users/1');
        console.log('');
        console.log('💡 提示: 使用curl或Postman等工具测试API');
        console.log('   示例: curl http://localhost:3000/api/v1/users');
    }
}

// 主执行函数
function main() {
    const demo = new ExpressWebDemo();
    demo.runDemo();
}

// 如果直接运行此文件，则执行主函数
if (require.main === module) {
    main();
}

// 导出类供其他模块使用
module.exports = ExpressWebDemo;