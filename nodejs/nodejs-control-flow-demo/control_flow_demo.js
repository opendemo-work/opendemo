#!/usr/bin/env node
/**
 * Node.js控制流基础演示程序
 * 展示条件语句、循环语句、异常处理等JavaScript控制结构的使用
 */

const util = require('util');

console.log('\n🎯 Node.js控制流基础演示\n');
console.log('=' .repeat(50));

class ControlFlowDemo {
    constructor() {
        console.log('初始化控制流演示环境...\n');
    }

    /**
     * 条件语句演示
     */
    demonstrateConditionalStatements() {
        console.log('📋 条件语句演示:');
        console.log('-'.repeat(30));

        // 1. if语句
        console.log('1. if语句:');
        const score = 85;
        if (score >= 90) {
            console.log(`   分数 ${score}: 优秀等级`);
        } else if (score >= 80) {
            console.log(`   分数 ${score}: 良好等级`);
        } else if (score >= 60) {
            console.log(`   分数 ${score}: 及格等级`);
        } else {
            console.log(`   分数 ${score}: 不及格`);
        }

        // 2. switch语句
        console.log('\n2. switch语句:');
        const day = 3;
        switch (day) {
            case 1:
                console.log('   星期一');
                break;
            case 2:
                console.log('   星期二');
                break;
            case 3:
                console.log('   星期三');
                break;
            case 4:
                console.log('   星期四');
                break;
            case 5:
                console.log('   星期五');
                break;
            case 6:
            case 7:
                console.log('   周末');
                break;
            default:
                console.log('   无效的星期数');
        }

        // 3. 三元运算符
        console.log('\n3. 三元运算符:');
        const age = 20;
        const status = age >= 18 ? '成年人' : '未成年人';
        console.log(`   年龄 ${age}: ${status}`);

        // 4. 逻辑运算符短路求值
        console.log('\n4. 逻辑运算符短路求值:');
        const user = { name: '张三', isActive: true };
        const displayName = user && user.name || '匿名用户';
        console.log(`   用户显示名: ${displayName}`);

        const isAdmin = user && user.isActive && user.role === 'admin';
        console.log(`   是否管理员: ${isAdmin || false}`);

        console.log('');
    }

    /**
     * 循环语句演示
     */
    demonstrateLoopStatements() {
        console.log('🔄 循环语句演示:');
        console.log('-'.repeat(30));

        const numbers = [1, 2, 3, 4, 5];
        const fruits = ['苹果', '香蕉', '橙子', '葡萄'];

        // 1. for循环
        console.log('1. for循环:');
        let sum = 0;
        for (let i = 0; i < numbers.length; i++) {
            sum += numbers[i];
        }
        console.log(`   数组求和: ${sum}`);

        // 2. for...of循环 (ES6)
        console.log('\n2. for...of循环:');
        console.log('   水果列表:');
        for (const fruit of fruits) {
            console.log(`     - ${fruit}`);
        }

        // 3. for...in循环
        console.log('\n3. for...in循环:');
        const person = { name: '李四', age: 25, city: '上海' };
        console.log('   人员信息:');
        for (const key in person) {
            if (person.hasOwnProperty(key)) {
                console.log(`     ${key}: ${person[key]}`);
            }
        }

        // 4. while循环
        console.log('\n4. while循环:');
        let count = 0;
        let factorial = 1;
        while (count < 5) {
            count++;
            factorial *= count;
        }
        console.log(`   5的阶乘: ${factorial}`);

        // 5. do...while循环
        console.log('\n5. do...while循环:');
        let num = 1;
        let powers = [];
        do {
            powers.push(Math.pow(2, num));
            num++;
        } while (num <= 5);
        console.log(`   2的1-5次幂: [${powers.join(', ')}]`);

        console.log('');
    }

    /**
     * 高级循环方法演示
     */
    demonstrateAdvancedIteration() {
        console.log('⚡ 高级循环方法演示:');
        console.log('-'.repeat(30));

        const students = [
            { name: '张三', score: 85, subject: '数学' },
            { name: '李四', score: 92, subject: '英语' },
            { name: '王五', score: 78, subject: '数学' },
            { name: '赵六', score: 88, subject: '物理' }
        ];

        // 1. forEach方法
        console.log('1. forEach方法:');
        console.log('   学生名单:');
        students.forEach((student, index) => {
            console.log(`     ${index + 1}. ${student.name} - ${student.subject}: ${student.score}分`);
        });

        // 2. map方法
        console.log('\n2. map方法:');
        const studentNames = students.map(student => student.name);
        console.log(`   学生姓名: [${studentNames.join(', ')}]`);

        const scoreBonuses = students.map(student => ({
            ...student,
            bonusScore: student.score + 5
        }));
        console.log('   加分后成绩:');
        scoreBonuses.forEach(s => console.log(`     ${s.name}: ${s.bonusScore}分`));

        // 3. filter方法
        console.log('\n3. filter方法:');
        const highScorers = students.filter(student => student.score >= 85);
        console.log('   高分学生 (>85分):');
        highScorers.forEach(s => console.log(`     ${s.name}: ${s.score}分`));

        const mathStudents = students.filter(s => s.subject === '数学');
        console.log(`   数学学生: [${mathStudents.map(s => s.name).join(', ')}]`);

        // 4. reduce方法
        console.log('\n4. reduce方法:');
        const totalScore = students.reduce((sum, student) => sum + student.score, 0);
        const averageScore = totalScore / students.length;
        console.log(`   总分: ${totalScore}分`);
        console.log(`   平均分: ${averageScore.toFixed(2)}分`);

        const subjectCount = students.reduce((acc, student) => {
            acc[student.subject] = (acc[student.subject] || 0) + 1;
            return acc;
        }, {});
        console.log('   各科目人数:', subjectCount);

        // 5. find和findIndex方法
        console.log('\n5. find和findIndex方法:');
        const bestStudent = students.find(student => student.score === Math.max(...students.map(s => s.score)));
        console.log(`   最高分学生: ${bestStudent.name} (${bestStudent.score}分)`);

        const englishStudentIndex = students.findIndex(student => student.subject === '英语');
        console.log(`   英语学生索引: ${englishStudentIndex}`);

        // 6. some和every方法
        console.log('\n6. some和every方法:');
        const hasHighScore = students.some(student => student.score > 90);
        console.log(`   是否有超过90分的学生: ${hasHighScore}`);

        const allPassed = students.every(student => student.score >= 60);
        console.log(`   是否所有学生都及格: ${allPassed}`);

        console.log('');
    }

    /**
     * 异常处理演示
     */
    demonstrateErrorHandling() {
        console.log('🛡️ 异常处理演示:');
        console.log('-'.repeat(30));

        // 1. try...catch基本用法
        console.log('1. try...catch基本用法:');
        try {
            const result = riskyOperation(10, 0);
            console.log(`   计算结果: ${result}`);
        } catch (error) {
            console.log(`   捕获错误: ${error.message}`);
        }

        // 2. finally块
        console.log('\n2. finally块:');
        try {
            console.log('   执行一些操作...');
            throw new Error('模拟错误');
        } catch (error) {
            console.log(`   处理错误: ${error.message}`);
        } finally {
            console.log('   清理资源 (finally总是执行)');
        }

        // 3. 自定义错误类型
        console.log('\n3. 自定义错误类型:');
        try {
            validateUserInput(''); // 空输入
        } catch (error) {
            if (error instanceof ValidationError) {
                console.log(`   验证错误: ${error.message}`);
            } else {
                console.log(`   其他错误: ${error.message}`);
            }
        }

        // 4. Promise错误处理
        console.log('\n4. Promise错误处理:');
        asyncOperation()
            .then(result => console.log(`   异步操作成功: ${result}`))
            .catch(error => console.log(`   异步操作失败: ${error.message}`));

        // 5. async/await错误处理
        console.log('\n5. async/await错误处理:');
        this.handleAsyncErrors();

        console.log('');
    }

    /**
     * 控制跳转语句演示
     */
    demonstrateControlFlowJumps() {
        console.log('⏭️ 控制跳转语句演示:');
        console.log('-'.repeat(30));

        // 1. break语句
        console.log('1. break语句:');
        console.log('   寻找第一个偶数:');
        const numbers = [1, 3, 5, 8, 9, 12];
        for (const num of numbers) {
            if (num % 2 === 0) {
                console.log(`     找到第一个偶数: ${num}`);
                break;
            }
        }

        // 2. continue语句
        console.log('\n2. continue语句:');
        console.log('   跳过奇数，只处理偶数:');
        for (const num of numbers) {
            if (num % 2 !== 0) {
                continue;
            }
            console.log(`     处理偶数: ${num}`);
        }

        // 3. 嵌套循环和标签
        console.log('\n3. 嵌套循环和标签:');
        outer: for (let i = 1; i <= 3; i++) {
            console.log(`   外层循环 i=${i}:`);
            for (let j = 1; j <= 3; j++) {
                if (i === 2 && j === 2) {
                    console.log(`     在(${i},${j})处跳出外层循环`);
                    break outer;
                }
                console.log(`     内层循环 j=${j}`);
            }
        }

        console.log('');
    }

    /**
     * 实际应用场景演示
     */
    demonstrateRealWorldScenarios() {
        console.log('🌍 实际应用场景演示:');
        console.log('-'.repeat(30));

        // 1. 数据验证场景
        console.log('1. 数据验证场景:');
        const userData = {
            name: '张三',
            email: 'zhangsan@example.com',
            age: 25,
            hobbies: ['读书', '游泳', '编程']
        };

        const validationErrors = this.validateUserData(userData);
        if (validationErrors.length > 0) {
            console.log('   验证失败:');
            validationErrors.forEach(error => console.log(`     - ${error}`));
        } else {
            console.log('   数据验证通过');
        }

        // 2. 文件处理场景
        console.log('\n2. 文件处理场景:');
        const fileSizes = [1024, 2048, 512, 4096, 100];
        this.processFiles(fileSizes);

        // 3. API请求处理场景
        console.log('\n3. API请求处理场景:');
        const apiResponses = [
            { status: 200, data: { id: 1, name: '用户1' } },
            { status: 404, error: '用户不存在' },
            { status: 500, error: '服务器错误' },
            { status: 200, data: { id: 2, name: '用户2' } }
        ];

        this.handleApiResponses(apiResponses);

        console.log('');
    }

    // 辅助方法
    async handleAsyncErrors() {
        try {
            const result = await this.asyncRiskyOperation();
            console.log(`   异步操作结果: ${result}`);
        } catch (error) {
            console.log(`   捕获异步错误: ${error.message}`);
        }
    }

    validateUserData(data) {
        const errors = [];
        
        if (!data.name || data.name.length < 2) {
            errors.push('姓名至少需要2个字符');
        }
        
        if (!data.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
            errors.push('邮箱格式不正确');
        }
        
        if (data.age < 0 || data.age > 150) {
            errors.push('年龄必须在0-150之间');
        }
        
        if (!Array.isArray(data.hobbies) || data.hobbies.length === 0) {
            errors.push('至少需要一个爱好');
        }
        
        return errors;
    }

    processFiles(fileSizes) {
        console.log('   处理文件:');
        fileSizes.forEach((size, index) => {
            if (size > 3000) {
                console.log(`     文件${index + 1} (${size}KB): 文件过大，跳过处理`);
                return;
            }
            if (size < 100) {
                console.log(`     文件${index + 1} (${size}KB): 文件过小，可能是空文件`);
                return;
            }
            console.log(`     文件${index + 1} (${size}KB): 处理成功`);
        });
    }

    handleApiResponses(responses) {
        console.log('   处理API响应:');
        responses.forEach((response, index) => {
            switch (response.status) {
                case 200:
                    console.log(`     请求${index + 1}: 成功 - ${response.data.name}`);
                    break;
                case 404:
                    console.log(`     请求${index + 1}: 未找到 - ${response.error}`);
                    break;
                case 500:
                    console.log(`     请求${index + 1}: 服务器错误 - ${response.error}`);
                    break;
                default:
                    console.log(`     请求${index + 1}: 未知状态 ${response.status}`);
            }
        });
    }

    // 运行所有演示
    runAllDemos() {
        try {
            this.demonstrateConditionalStatements();
            this.demonstrateLoopStatements();
            this.demonstrateAdvancedIteration();
            this.demonstrateErrorHandling();
            this.demonstrateControlFlowJumps();
            this.demonstrateRealWorldScenarios();
            
            console.log('🎉 所有控制流演示完成!');
            console.log('='.repeat(50));
            
        } catch (error) {
            console.error('❌ 演示过程中出现错误:', error);
        }
    }
}

// 辅助函数
function riskyOperation(a, b) {
    if (b === 0) {
        throw new Error('除数不能为零');
    }
    return a / b;
}

function asyncOperation() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            // 模拟50%成功率
            if (Math.random() > 0.5) {
                resolve('操作成功');
            } else {
                reject(new Error('操作失败'));
            }
        }, 1000);
    });
}

class ValidationError extends Error {
    constructor(message) {
        super(message);
        this.name = 'ValidationError';
    }
}

function validateUserInput(input) {
    if (!input || input.trim() === '') {
        throw new ValidationError('输入不能为空');
    }
    if (input.length < 3) {
        throw new ValidationError('输入长度至少为3个字符');
    }
    return true;
}

ControlFlowDemo.prototype.asyncRiskyOperation = async function() {
    await new Promise(resolve => setTimeout(resolve, 500));
    if (Math.random() > 0.7) {
        throw new Error('异步操作随机失败');
    }
    return '异步操作成功';
};

// 主执行函数
function main() {
    const demo = new ControlFlowDemo();
    demo.runAllDemos();
}

// 如果直接运行此文件，则执行主函数
if (require.main === module) {
    main();
}

// 导出类供其他模块使用
module.exports = ControlFlowDemo;