#!/usr/bin/env node
/**
 * Node.js变量和数据类型基础演示程序
 * 展示var、let、const声明方式及JavaScript各种数据类型的特性和使用
 */

// 导入必要的模块
const util = require('util');

// 配置控制台输出样式
console.log('\n🚀 Node.js变量和数据类型基础演示\n');
console.log('=' .repeat(50));

class VariablesTypesDemo {
    constructor() {
        console.log('初始化变量和数据类型演示环境...\n');
    }

    /**
     * 变量声明方式演示
     */
    demonstrateVariableDeclarations() {
        console.log('📋 变量声明方式演示:');
        console.log('-'.repeat(30));

        // 1. var声明（函数作用域）
        console.log('1. var声明 (函数作用域):');
        var varVariable = '我是var变量';
        console.log(`   varVariable = "${varVariable}"`);
        console.log(`   typeof varVariable = ${typeof varVariable}\n`);

        // 2. let声明（块级作用域）
        console.log('2. let声明 (块级作用域):');
        let letVariable = '我是let变量';
        console.log(`   letVariable = "${letVariable}"`);
        console.log(`   typeof letVariable = ${typeof letVariable}\n`);

        // 3. const声明（常量）
        console.log('3. const声明 (常量):');
        const constVariable = '我是const常量';
        console.log(`   constVariable = "${constVariable}"`);
        console.log(`   typeof constVariable = ${typeof constVariable}\n`);

        // 4. 作用域差异演示
        console.log('4. 作用域差异演示:');
        this.scopeDifferenceDemo();

        // 5. 变量提升演示
        console.log('5. 变量提升演示:');
        this.hoistingDemo();
    }

    /**
     * 作用域差异演示
     */
    scopeDifferenceDemo() {
        console.log('   函数作用域 vs 块级作用域:');

        // var的函数作用域
        function varScopeTest() {
            if (true) {
                var functionScoped = 'var在函数内可见';
            }
            console.log(`     var变量: ${functionScoped}`); // 可以访问
        }
        varScopeTest();

        // let的块级作用域
        try {
            if (true) {
                let blockScoped = 'let仅在块内可见';
            }
            // console.log(blockScoped); // 这里会报错
        } catch (error) {
            console.log(`     let变量: 访问时报错 - ${error.message}`);
        }

        console.log('');
    }

    /**
     * 变量提升演示
     */
    hoistingDemo() {
        console.log('   变量提升行为:');

        // var提升 - 声明提升但赋值不提升
        console.log(`     var变量提升: ${typeof hoistedVar}`); // undefined
        var hoistedVar = 'var变量';
        console.log(`     var变量赋值后: ${hoistedVar}`);

        // let/const暂时性死区
        try {
            console.log(temporalDeadZoneLet); // ReferenceError
        } catch (error) {
            console.log(`     let暂时性死区: ${error.name}`);
        }
        let temporalDeadZoneLet = 'let变量';

        console.log('');
    }

    /**
     * 基本数据类型演示
     */
    demonstratePrimitiveTypes() {
        console.log('🔢 基本数据类型演示:');
        console.log('-'.repeat(30));

        // 1. Number类型
        console.log('1. Number类型:');
        const integer = 42;
        const float = 3.14159;
        const scientific = 1.23e5;
        const infinity = Infinity;
        const nan = NaN;

        console.log(`   整数: ${integer} (typeof: ${typeof integer})`);
        console.log(`   浮点数: ${float} (typeof: ${typeof float})`);
        console.log(`   科学计数法: ${scientific} (typeof: ${typeof scientific})`);
        console.log(`   无穷大: ${infinity} (typeof: ${typeof infinity})`);
        console.log(`   非数字: ${nan} (typeof: ${typeof nan})`);
        console.log(`   NaN === NaN: ${nan === nan}`); // false
        console.log('');

        // 2. String类型
        console.log('2. String类型:');
        const singleQuote = '单引号字符串';
        const doubleQuote = "双引号字符串";
        const templateLiteral = `模板字符串可以嵌入变量: ${integer}`;
        const multiline = `多行
字符串
演示`;

        console.log(`   单引号: ${singleQuote}`);
        console.log(`   双引号: ${doubleQuote}`);
        console.log(`   模板字面量: ${templateLiteral}`);
        console.log(`   多行字符串: ${multiline.trim()}`);
        console.log(`   字符串长度: ${singleQuote.length}`);
        console.log('');

        // 3. Boolean类型
        console.log('3. Boolean类型:');
        const trueValue = true;
        const falseValue = false;
        const truthyValues = [1, 'hello', [], {}, -1];
        const falsyValues = [0, '', null, undefined, NaN, false];

        console.log(`   显式布尔值: ${trueValue}, ${falseValue}`);
        console.log('   真值(truthy)示例:', truthyValues.map(v => `${v}(${!!v})`));
        console.log('   假值(falsy)示例:', falsyValues.map(v => `${v}(${!!v})`));
        console.log('');

        // 4. Undefined类型
        console.log('4. Undefined类型:');
        let undefinedVar;
        const explicitUndefined = undefined;

        console.log(`   未初始化变量: ${undefinedVar} (typeof: ${typeof undefinedVar})`);
        console.log(`   显式undefined: ${explicitUndefined} (typeof: ${typeof explicitUndefined})`);
        console.log('');

        // 5. Null类型
        console.log('5. Null类型:');
        const nullValue = null;
        console.log(`   null值: ${nullValue} (typeof: ${typeof nullValue})`);
        console.log(`   null == undefined: ${null == undefined}`); // true
        console.log(`   null === undefined: ${null === undefined}`); // false
        console.log('');

        // 6. Symbol类型 (ES6)
        console.log('6. Symbol类型 (ES6):');
        const symbol1 = Symbol('描述1');
        const symbol2 = Symbol('描述1');
        const symbol3 = Symbol.for('全局符号');

        console.log(`   Symbol创建: ${symbol1.toString()}`);
        console.log(`   相同描述的Symbol相等吗: ${symbol1 === symbol2}`); // false
        console.log(`   全局Symbol: ${Symbol.for('全局符号') === symbol3}`); // true
        console.log('');

        // 7. BigInt类型 (ES2020)
        console.log('7. BigInt类型 (ES2020):');
        const bigInt1 = 123456789012345678901234567890n;
        const bigInt2 = BigInt('123456789012345678901234567890');

        console.log(`   BigInt字面量: ${bigInt1}`);
        console.log(`   BigInt构造函数: ${bigInt2}`);
        console.log(`   typeof bigInt1: ${typeof bigInt1}`);
        console.log('');
    }

    /**
     * 引用数据类型演示
     */
    demonstrateReferenceTypes() {
        console.log('📦 引用数据类型演示:');
        console.log('-'.repeat(30));

        // 1. Object类型
        console.log('1. Object类型:');
        const person = {
            name: '张三',
            age: 25,
            skills: ['JavaScript', 'Node.js'],
            address: {
                city: '北京',
                district: '朝阳区'
            },
            greet() {
                return `你好，我是${this.name}`;
            }
        };

        console.log('   对象内容:');
        console.log(util.inspect(person, { depth: null, colors: true }));
        console.log(`   方法调用: ${person.greet()}`);
        console.log(`   属性访问: ${person.name}, ${person['age']}`);
        console.log('');

        // 2. Array类型
        console.log('2. Array类型:');
        const fruits = ['苹果', '香蕉', '橙子'];
        const mixedArray = [1, '字符串', true, null, { key: 'value' }];

        console.log(`   水果数组: [${fruits.join(', ')}]`);
        console.log(`   混合数组: ${util.inspect(mixedArray)}`);
        console.log(`   数组长度: ${fruits.length}`);
        console.log(`   第一个元素: ${fruits[0]}`);
        console.log(`   最后一个元素: ${fruits[fruits.length - 1]}`);
        console.log('');

        // 3. Function类型
        console.log('3. Function类型:');
        
        // 函数声明
        function declaredFunction(a, b) {
            return a + b;
        }

        // 函数表达式
        const expressionFunction = function(x) {
            return x * 2;
        };

        // 箭头函数
        const arrowFunction = (name) => `Hello, ${name}!`;

        console.log(`   函数声明: ${declaredFunction(3, 4)}`);
        console.log(`   函数表达式: ${expressionFunction(5)}`);
        console.log(`   箭头函数: ${arrowFunction('World')}`);
        console.log('');

        // 4. Date类型
        console.log('4. Date类型:');
        const now = new Date();
        const specificDate = new Date('2024-01-15T10:30:00');
        const timestamp = new Date(1705311000000);

        console.log(`   当前时间: ${now.toLocaleString()}`);
        console.log(`   指定日期: ${specificDate.toLocaleString()}`);
        console.log(`   时间戳创建: ${timestamp.toLocaleString()}`);
        console.log(`   年份: ${now.getFullYear()}`);
        console.log(`   月份: ${now.getMonth() + 1}`); // 月份从0开始
        console.log('');

        // 5. RegExp类型
        console.log('5. RegExp类型:');
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const phoneRegex = /^1[3-9]\d{9}$/;

        const testEmails = ['user@example.com', 'invalid.email', 'test@domain'];
        const testPhones = ['13812345678', '12345678901', 'invalid'];

        console.log('   邮箱验证:');
        testEmails.forEach(email => {
            console.log(`     ${email}: ${emailRegex.test(email)}`);
        });

        console.log('   手机号验证:');
        testPhones.forEach(phone => {
            console.log(`     ${phone}: ${phoneRegex.test(phone)}`);
        });
        console.log('');
    }

    /**
     * 类型检测和转换演示
     */
    demonstrateTypeCheckingConversion() {
        console.log('🔍 类型检测和转换演示:');
        console.log('-'.repeat(30));

        // 1. 类型检测方法
        console.log('1. 类型检测方法:');
        const testValues = [
            42, 'hello', true, null, undefined,
            {}, [], function(){}, Symbol('test')
        ];

        console.log('   typeof操作符:');
        testValues.forEach(value => {
            console.log(`     ${util.inspect(value)}: ${typeof value}`);
        });

        console.log('\n   instanceof操作符:');
        console.log(`   [] instanceof Array: ${[] instanceof Array}`);
        console.log(`   {} instanceof Object: ${({}) instanceof Object}`);
        console.log(`   new Date() instanceof Date: ${new Date() instanceof Date}`);

        console.log('\n   Array.isArray():');
        console.log(`   Array.isArray([]): ${Array.isArray([])}`);
        console.log(`   Array.isArray({}): ${Array.isArray({})}`);

        // 2. 类型转换演示
        console.log('\n2. 类型转换演示:');
        
        // 隐式转换
        console.log('   隐式转换:');
        console.log(`     "5" + 3 = ${"5" + 3} (字符串连接)`);
        console.log(`     "5" - 3 = ${"5" - 3} (数值运算)`);
        console.log(`     true + 1 = ${true + 1}`);
        console.log(`     false + 1 = ${false + 1}`);

        // 显式转换
        console.log('\n   显式转换:');
        const stringValue = "123.45";
        console.log(`     String to Number: Number("${stringValue}") = ${Number(stringValue)}`);
        console.log(`     Parse Float: parseFloat("${stringValue}") = ${parseFloat(stringValue)}`);
        console.log(`     Parse Int: parseInt("${stringValue}") = ${parseInt(stringValue)}`);

        const numericValue = 42;
        console.log(`     Number to String: String(${numericValue}) = "${String(numericValue)}"`);
        console.log(`     Number to String: ${numericValue}.toString() = "${numericValue.toString()}"`);

        const booleanValue = "hello";
        console.log(`     To Boolean: Boolean("${booleanValue}") = ${Boolean(booleanValue)}`);
        console.log(`     To Boolean: !!("${booleanValue}") = ${!!booleanValue}`);
        console.log('');
    }

    /**
     * 内存管理和性能考虑
     */
    demonstrateMemoryManagement() {
        console.log('💾 内存管理和性能考虑:');
        console.log('-'.repeat(30));

        // 1. 变量内存分配
        console.log('1. 变量内存分配:');
        const primitiveSize = '基本类型存储值本身';
        const referenceSize = '引用类型存储内存地址';

        console.log(`   基本类型: ${primitiveSize}`);
        console.log(`   引用类型: ${referenceSize}`);

        // 2. 垃圾回收演示
        console.log('\n2. 垃圾回收影响:');
        let largeObject = { data: new Array(1000000).fill('x') };
        console.log(`   创建大对象，内存占用增加`);
        
        largeObject = null; // 断开引用
        console.log(`   断开引用后，对象可被垃圾回收`);
        console.log(`   手动触发垃圾回收: global.gc && global.gc()`);

        // 3. 性能优化建议
        console.log('\n3. 性能优化建议:');
        console.log('   • 优先使用const，其次是let，避免var');
        console.log('   • 合理使用局部变量而非全局变量');
        console.log('   • 避免频繁创建临时对象');
        console.log('   • 及时清理不需要的引用');
        console.log('');
    }

    /**
     * 运行所有演示
     */
    runAllDemos() {
        try {
            this.demonstrateVariableDeclarations();
            this.demonstratePrimitiveTypes();
            this.demonstrateReferenceTypes();
            this.demonstrateTypeCheckingConversion();
            this.demonstrateMemoryManagement();
            
            console.log('🎉 所有演示完成!');
            console.log('='.repeat(50));
            
        } catch (error) {
            console.error('❌ 演示过程中出现错误:', error);
        }
    }
}

// 主执行函数
function main() {
    const demo = new VariablesTypesDemo();
    demo.runAllDemos();
}

// 如果直接运行此文件，则执行主函数
if (require.main === module) {
    main();
}

// 导出类供其他模块使用
module.exports = VariablesTypesDemo;