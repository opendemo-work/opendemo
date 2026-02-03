#!/usr/bin/env node
/**
 * Node.js控制流测试文件
 * 验证条件语句、循环语句、异常处理等控制结构的正确性
 */

const ControlFlowDemo = require('./control_flow_demo');

// 简单的断言函数
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

function runTests() {
    console.log('🧪 开始运行控制流测试...\n');

    try {
        // 测试1: 条件语句
        console.log('1. 测试条件语句...');
        
        // if-else测试
        const score = 85;
        let grade;
        if (score >= 90) {
            grade = '优秀';
        } else if (score >= 80) {
            grade = '良好';
        } else if (score >= 60) {
            grade = '及格';
        } else {
            grade = '不及格';
        }
        assert(grade === '良好', '分数等级判断应该正确');
        
        // 三元运算符测试
        const age = 20;
        const status = age >= 18 ? '成年人' : '未成年人';
        assert(status === '成年人', '三元运算符判断应该正确');
        
        // switch语句测试
        const day = 3;
        let dayName;
        switch (day) {
            case 1: dayName = '星期一'; break;
            case 2: dayName = '星期二'; break;
            case 3: dayName = '星期三'; break;
            default: dayName = '其他';
        }
        assert(dayName === '星期三', 'switch语句应该正确匹配');
        
        console.log('   ✓ 条件语句测试通过\n');

        // 测试2: 循环语句
        console.log('2. 测试循环语句...');
        
        // for循环测试
        const numbers = [1, 2, 3, 4, 5];
        let sum = 0;
        for (let i = 0; i < numbers.length; i++) {
            sum += numbers[i];
        }
        assert(sum === 15, 'for循环数组求和应该正确');
        
        // for...of循环测试
        const fruits = ['苹果', '香蕉', '橙子'];
        const fruitList = [];
        for (const fruit of fruits) {
            fruitList.push(fruit);
        }
        assertDeepEqual(fruitList, fruits, 'for...of循环应该正确遍历');
        
        // while循环测试
        let count = 0;
        let result = 1;
        while (count < 4) {
            count++;
            result *= 2;
        }
        assert(result === 16, 'while循环计算应该正确');
        
        console.log('   ✓ 循环语句测试通过\n');

        // 测试3: 数组方法
        console.log('3. 测试数组方法...');
        
        const testData = [1, 2, 3, 4, 5];
        
        // map测试
        const doubled = testData.map(x => x * 2);
        assertDeepEqual(doubled, [2, 4, 6, 8, 10], 'map方法应该正确转换');
        
        // filter测试
        const evens = testData.filter(x => x % 2 === 0);
        assertDeepEqual(evens, [2, 4], 'filter方法应该正确筛选');
        
        // reduce测试
        const total = testData.reduce((sum, x) => sum + x, 0);
        assert(total === 15, 'reduce方法求和应该正确');
        
        // find测试
        const found = testData.find(x => x > 3);
        assert(found === 4, 'find方法应该找到第一个匹配项');
        
        console.log('   ✓ 数组方法测试通过\n');

        // 测试4: 异常处理
        console.log('4. 测试异常处理...');
        
        // try-catch测试
        let errorThrown = false;
        try {
            throw new Error('测试错误');
        } catch (error) {
            errorThrown = true;
            assert(error.message === '测试错误', '应该捕获到正确的错误消息');
        }
        assert(errorThrown, '应该触发错误处理');
        
        // 自定义错误测试
        class CustomError extends Error {
            constructor(message) {
                super(message);
                this.name = 'CustomError';
            }
        }
        
        let customErrorCaught = false;
        try {
            throw new CustomError('自定义错误');
        } catch (error) {
            if (error instanceof CustomError) {
                customErrorCaught = true;
                assert(error.name === 'CustomError', '应该识别自定义错误类型');
            }
        }
        assert(customErrorCaught, '应该捕获自定义错误');
        
        console.log('   ✓ 异常处理测试通过\n');

        // 测试5: 控制跳转
        console.log('5. 测试控制跳转...');
        
        // break测试
        const breakTest = [1, 2, 3, 4, 5];
        let breakResult = [];
        for (const item of breakTest) {
            if (item === 4) break;
            breakResult.push(item);
        }
        assertDeepEqual(breakResult, [1, 2, 3], 'break语句应该正确跳出循环');
        
        // continue测试
        const continueTest = [1, 2, 3, 4, 5];
        let continueResult = [];
        for (const item of continueTest) {
            if (item % 2 === 0) continue;
            continueResult.push(item);
        }
        assertDeepEqual(continueResult, [1, 3, 5], 'continue语句应该正确跳过迭代');
        
        console.log('   ✓ 控制跳转测试通过\n');

        // 测试6: 实际应用场景
        console.log('6. 测试实际应用场景...');
        
        // 数据验证测试
        function validateEmail(email) {
            return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        }
        
        assert(validateEmail('user@example.com') === true, '有效邮箱应该验证通过');
        assert(validateEmail('invalid.email') === false, '无效邮箱应该验证失败');
        
        // 数组处理测试
        const scores = [85, 92, 78, 96, 88];
        const passedStudents = scores.filter(score => score >= 80);
        const average = scores.reduce((sum, score) => sum + score, 0) / scores.length;
        
        assert(passedStudents.length === 4, '应该有4个及格学生');
        assert(Math.abs(average - 87.8) < 0.1, '平均分计算应该正确');
        
        console.log('   ✓ 实际应用场景测试通过\n');

        console.log('🎉 所有测试通过! Node.js控制流功能正常');
        
    } catch (error) {
        console.error('❌ 测试失败:', error.message);
        process.exit(1);
    }
}

// 运行测试
if (require.main === module) {
    runTests();
}

module.exports = { runTests };