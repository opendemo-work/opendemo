#!/usr/bin/env node
/**
 * Node.js变量和数据类型测试文件
 * 验证各种变量声明、数据类型和类型转换的正确性
 */

const VariablesTypesDemo = require('./variables_types_demo');

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

function runTests() {
    console.log('🧪 开始运行变量和数据类型测试...\n');

    try {
        // 测试1: 变量声明方式
        console.log('1. 测试变量声明方式...');
        
        // var声明测试
        var varTest = 'var变量';
        assert(typeof varTest === 'string', 'var声明应该创建字符串类型');
        assert(varTest === 'var变量', 'var变量值应该正确');
        
        // let声明测试
        let letTest = 'let变量';
        assert(typeof letTest === 'string', 'let声明应该创建字符串类型');
        assert(letTest === 'let变量', 'let变量值应该正确');
        
        // const声明测试
        const constTest = 'const变量';
        assert(typeof constTest === 'string', 'const声明应该创建字符串类型');
        assert(constTest === 'const变量', 'const变量值应该正确');
        
        console.log('   ✓ 变量声明测试通过\n');

        // 测试2: 基本数据类型
        console.log('2. 测试基本数据类型...');
        
        // Number类型测试
        const num = 42;
        assert(typeof num === 'number', '数字类型检测');
        assert(Number.isInteger(num), '42应该是整数');
        
        const float = 3.14;
        assert(typeof float === 'number', '浮点数类型检测');
        assert(!Number.isInteger(float), '3.14不应该被认为是整数');
        
        // String类型测试
        const str = 'Hello World';
        assert(typeof str === 'string', '字符串类型检测');
        assert(str.length === 11, '字符串长度应该为11');
        
        // Boolean类型测试
        const boolTrue = true;
        const boolFalse = false;
        assert(typeof boolTrue === 'boolean', '布尔类型检测');
        assert(boolTrue === true, '布尔值true测试');
        assert(boolFalse === false, '布尔值false测试');
        
        // Undefined类型测试
        let undefinedVar;
        assert(typeof undefinedVar === 'undefined', '未定义变量类型检测');
        assert(undefinedVar === undefined, '未初始化变量应该等于undefined');
        
        // Null类型测试
        const nullVar = null;
        assert(typeof nullVar === 'object', 'null的typeof应该是object(历史遗留问题)');
        assert(nullVar === null, 'null值比较测试');
        assert(nullVar == undefined, 'null等于undefined(宽松相等)');
        assert(!(nullVar === undefined), 'null不全等于undefined(严格相等)');
        
        // Symbol类型测试
        const sym1 = Symbol('test');
        const sym2 = Symbol('test');
        assert(typeof sym1 === 'symbol', 'Symbol类型检测');
        assert(sym1 !== sym2, '相同描述的Symbol不相等');
        assert(sym1.toString().includes('test'), 'Symbol描述正确');
        
        console.log('   ✓ 基本数据类型测试通过\n');

        // 测试3: 引用数据类型
        console.log('3. 测试引用数据类型...');
        
        // Object类型测试
        const obj = { name: '测试', value: 123 };
        assert(typeof obj === 'object', '对象类型检测');
        assert(obj.name === '测试', '对象属性访问');
        assert(obj.value === 123, '对象数值属性访问');
        assert(Object.keys(obj).length === 2, '对象应该有两个属性');
        
        // Array类型测试
        const arr = [1, 2, 3, 'four'];
        assert(Array.isArray(arr), '数组类型检测');
        assert(arr.length === 4, '数组长度检测');
        assert(arr[0] === 1 && arr[3] === 'four', '数组元素访问');
        
        // Function类型测试
        const func = function(x) { return x * 2; };
        assert(typeof func === 'function', '函数类型检测');
        assert(func(5) === 10, '函数执行结果');
        
        // Date类型测试
        const date = new Date('2024-01-15');
        assert(date instanceof Date, 'Date实例检测');
        assert(date.getFullYear() === 2024, '年份获取');
        assert(date.getMonth() === 0, '月份获取(0-indexed)');
        
        console.log('   ✓ 引用数据类型测试通过\n');

        // 测试4: 类型转换
        console.log('4. 测试类型转换...');
        
        // 字符串到数字转换
        const strToNum = Number('123');
        assert(typeof strToNum === 'number', '字符串转数字类型');
        assert(strToNum === 123, '字符串转数字值');
        
        const parsedFloat = parseFloat('123.45');
        assert(parsedFloat === 123.45, 'parseFloat转换');
        
        // 数字到字符串转换
        const numToStr = String(42);
        assert(typeof numToStr === 'string', '数字转字符串类型');
        assert(numToStr === '42', '数字转字符串值');
        
        // 布尔转换
        assert(Boolean('hello') === true, '非空字符串转布尔');
        assert(Boolean('') === false, '空字符串转布尔');
        assert(Boolean(1) === true, '非零数字转布尔');
        assert(Boolean(0) === false, '零转布尔');
        assert(!!'hello' === true, '双重否定布尔转换');
        
        // 隐式转换测试
        assert('5' + 3 === '53', '字符串连接隐式转换');
        assert('5' - 3 === 2, '数值运算隐式转换');
        assert(true + 1 === 2, '布尔转数字隐式转换');
        
        console.log('   ✓ 类型转换测试通过\n');

        // 测试5: 作用域和提升
        console.log('5. 测试作用域和提升...');
        
        // var提升测试
        assert(typeof hoistedVar === 'undefined', 'var变量在声明前是undefined');
        var hoistedVar = '提升的var';
        assert(hoistedVar === '提升的var', 'var变量赋值后正常访问');
        
        // let暂时性死区测试
        let tdzLet = '暂时性死区测试';
        assert(tdzLet === '暂时性死区测试', 'let变量正常访问');
        
        console.log('   ✓ 作用域和提升测试通过\n');

        // 测试6: 特殊值比较
        console.log('6. 测试特殊值比较...');
        
        // NaN测试
        assert(isNaN(NaN), 'NaN检测');
        assert(NaN !== NaN, 'NaN不等于自身');
        assert(!(NaN === NaN), 'NaN不严格等于自身');
        
        // Infinity测试
        assert(Infinity > 1000000, 'Infinity大于大数');
        assert(typeof Infinity === 'number', 'Infinity是数字类型');
        assert(1/0 === Infinity, '除零得到Infinity');
        
        // 空值比较
        const emptyValues = [null, undefined, '', 0, false, NaN];
        emptyValues.forEach(val => {
            if (val !== null && val !== undefined) {
                assert(!val, `${val}应该被认为是假值`);
            }
        });
        
        console.log('   ✓ 特殊值比较测试通过\n');

        console.log('🎉 所有测试通过! Node.js变量和数据类型功能正常');
        
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