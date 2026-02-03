#!/usr/bin/env node
/**
 * Node.js Express Web框架测试文件
 * 验证RESTful API、路由、中间件等Web开发功能的正确性
 */

const ExpressWebDemo = require('./express_web_demo');
const http = require('http');

// 简单的HTTP客户端
class HttpClient {
    constructor(baseUrl = 'http://localhost:3000') {
        this.baseUrl = baseUrl;
    }

    async request(method, path, body = null) {
        const url = `${this.baseUrl}${path}`;
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };

        return new Promise((resolve, reject) => {
            const req = http.request(url, options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        const jsonData = JSON.parse(data);
                        resolve({
                            statusCode: res.statusCode,
                            headers: res.headers,
                            body: jsonData
                        });
                    } catch (error) {
                        resolve({
                            statusCode: res.statusCode,
                            headers: res.headers,
                            body: data
                        });
                    }
                });
            });

            req.on('error', reject);

            if (body) {
                req.write(JSON.stringify(body));
            }

            req.end();
        });
    }

    get(path) {
        return this.request('GET', path);
    }

    post(path, body) {
        return this.request('POST', path, body);
    }

    put(path, body) {
        return this.request('PUT', path, body);
    }

    delete(path) {
        return this.request('DELETE', path);
    }
}

// 测试断言函数
function assert(condition, message) {
    if (!condition) {
        throw new Error(`Assertion failed: ${message}`);
    }
}

function assertEqual(actual, expected, message) {
    if (actual !== expected) {
        throw new Error(`Assertion failed: ${message}. Expected ${expected}, got ${actual}`);
    }
}

function assertDeepEqual(actual, expected, message) {
    const actualStr = JSON.stringify(actual);
    const expectedStr = JSON.stringify(expected);
    if (actualStr !== expectedStr) {
        throw new Error(`Assertion failed: ${message}. Expected ${expectedStr}, got ${actualStr}`);
    }
}

async function runTests() {
    console.log('🧪 开始运行Express Web框架测试...\n');

    // 启动测试服务器
    const demo = new ExpressWebDemo();
    demo.startServer();
    
    // 等待服务器启动
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const client = new HttpClient();

    try {
        // 测试1: 根路径访问
        console.log('1. 测试根路径访问...');
        const rootResponse = await client.get('/');
        assertEqual(rootResponse.statusCode, 200, '根路径应该返回200状态码');
        assert(rootResponse.body.message, '响应应该包含message字段');
        console.log('   ✓ 根路径访问测试通过\n');

        // 测试2: 健康检查
        console.log('2. 测试健康检查...');
        const healthResponse = await client.get('/health');
        assertEqual(healthResponse.statusCode, 200, '健康检查应该返回200状态码');
        assert(healthResponse.body.status === 'healthy', '健康状态应该为healthy');
        assert(healthResponse.body.timestamp, '应该包含时间戳');
        console.log('   ✓ 健康检查测试通过\n');

        // 测试3: 获取用户列表
        console.log('3. 测试获取用户列表...');
        const usersResponse = await client.get('/api/v1/users');
        assertEqual(usersResponse.statusCode, 200, '获取用户列表应该返回200状态码');
        assert(Array.isArray(usersResponse.body.data), '数据应该是一个数组');
        assert(usersResponse.body.pagination, '应该包含分页信息');
        console.log(`   ✓ 获取用户列表测试通过 (共${usersResponse.body.data.length}个用户)\n`);

        // 测试4: 分页功能
        console.log('4. 测试分页功能...');
        const paginatedResponse = await client.get('/api/v1/users?page=1&limit=2');
        assertEqual(paginatedResponse.statusCode, 200, '分页请求应该返回200状态码');
        assert(paginatedResponse.body.data.length <= 2, '返回的数据条数应该不超过限制');
        assert(paginatedResponse.body.pagination.currentPage === 1, '当前页码应该正确');
        console.log('   ✓ 分页功能测试通过\n');

        // 测试5: 搜索功能
        console.log('5. 测试搜索功能...');
        const searchResponse = await client.get('/api/v1/users?search=张');
        assertEqual(searchResponse.statusCode, 200, '搜索请求应该返回200状态码');
        assert(Array.isArray(searchResponse.body.data), '搜索结果应该是数组');
        console.log('   ✓ 搜索功能测试通过\n');

        // 测试6: 创建用户
        console.log('6. 测试创建用户...');
        const newUser = {
            name: '测试用户',
            email: 'test@example.com',
            age: 25
        };
        const createResponse = await client.post('/api/v1/users', newUser);
        assertEqual(createResponse.statusCode, 201, '创建用户应该返回201状态码');
        assert(createResponse.body.data.id, '新用户应该有ID');
        assert(createResponse.body.data.name === newUser.name, '用户名应该正确');
        console.log('   ✓ 创建用户测试通过\n');

        // 测试7: 获取特定用户
        console.log('7. 测试获取特定用户...');
        const userId = createResponse.body.data.id;
        const getUserResponse = await client.get(`/api/v1/users/${userId}`);
        assertEqual(getUserResponse.statusCode, 200, '获取用户应该返回200状态码');
        assert(getUserResponse.body.data.id === userId, '用户ID应该匹配');
        console.log('   ✓ 获取特定用户测试通过\n');

        // 测试8: 更新用户
        console.log('8. 测试更新用户...');
        const updateData = { name: '更新后的用户', age: 30 };
        const updateResponse = await client.put(`/api/v1/users/${userId}`, updateData);
        assertEqual(updateResponse.statusCode, 200, '更新用户应该返回200状态码');
        assert(updateResponse.body.data.name === updateData.name, '用户名应该已更新');
        assert(updateResponse.body.data.age === updateData.age, '年龄应该已更新');
        console.log('   ✓ 更新用户测试通过\n');

        // 测试9: 删除用户
        console.log('9. 测试删除用户...');
        const deleteResponse = await client.delete(`/api/v1/users/${userId}`);
        assertEqual(deleteResponse.statusCode, 200, '删除用户应该返回200状态码');
        assert(deleteResponse.body.data.id === userId, '应该返回被删除的用户信息');
        console.log('   ✓ 删除用户测试通过\n');

        // 测试10: 错误处理
        console.log('10. 测试错误处理...');
        
        // 测试无效用户ID
        const invalidIdResponse = await client.get('/api/v1/users/abc');
        assertEqual(invalidIdResponse.statusCode, 400, '无效ID应该返回400状态码');
        
        // 测试不存在的用户
        const notFoundResponse = await client.get('/api/v1/users/999');
        assertEqual(notFoundResponse.statusCode, 404, '不存在的用户应该返回404状态码');
        
        // 测试缺少必需字段
        const missingFieldResponse = await client.post('/api/v1/users', { name: '测试' });
        assertEqual(missingFieldResponse.statusCode, 400, '缺少必需字段应该返回400状态码');
        
        console.log('   ✓ 错误处理测试通过\n');

        // 测试11: 404处理
        console.log('11. 测试404处理...');
        const notFoundRouteResponse = await client.get('/nonexistent-route');
        assertEqual(notFoundRouteResponse.statusCode, 404, '不存在的路由应该返回404状态码');
        assert(notFoundRouteResponse.body.error, '404响应应该包含错误信息');
        console.log('   ✓ 404处理测试通过\n');

        console.log('🎉 所有Express Web框架测试通过!');
        console.log('='.repeat(50));
        
        // 关闭服务器
        if (demo.server) {
            demo.server.close();
        }

    } catch (error) {
        console.error('❌ 测试失败:', error.message);
        if (demo.server) {
            demo.server.close();
        }
        process.exit(1);
    }
}

// 运行测试
if (require.main === module) {
    runTests().catch(error => {
        console.error('测试执行出错:', error);
        process.exit(1);
    });
}

module.exports = { runTests, HttpClient };