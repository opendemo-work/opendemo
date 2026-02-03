# Node.js控制流基础

## 🎯 案例概述

这是一个全面展示Node.js控制流结构的示例，涵盖条件语句、循环语句、异常处理、控制跳转等JavaScript控制结构的使用方法和最佳实践。

## 📚 学习目标

通过本示例你将掌握：
- if、switch等条件语句的使用技巧
- for、while等循环语句的应用场景
- 数组高级迭代方法（map、filter、reduce等）
- try-catch异常处理机制
- break、continue等控制跳转语句
- 实际开发中的控制流应用模式

## 🔧 核心知识点

### 1. 条件语句
- **if...else**: 基本条件判断
- **switch**: 多分支选择结构
- **三元运算符**: 简洁的条件表达式
- **逻辑运算符短路**: && 和 || 的求值特性

### 2. 循环语句
- **for循环**: 传统的计数循环
- **for...of**: ES6迭代协议循环
- **for...in**: 对象属性遍历
- **while循环**: 条件驱动循环
- **do...while**: 至少执行一次的循环

### 3. 异常处理
- **try...catch**: 基本异常捕获
- **finally**: 清理资源块
- **自定义错误**: 扩展Error类
- **Promise错误处理**: 异步操作异常处理

### 4. 控制跳转
- **break**: 跳出循环或switch
- **continue**: 跳过当前迭代
- **标签**: 嵌套循环控制

## 🚀 运行示例

```bash
# 安装依赖（本示例无外部依赖）
npm install

# 运行主程序
npm start
# 或者
node control_flow_demo.js

# 运行测试
npm test
# 或者
node test_control_flow.js
```

## 📖 代码详解

### 主要类结构

```javascript
class ControlFlowDemo {
    demonstrateConditionalStatements()   // 条件语句演示
    demonstrateLoopStatements()          // 循环语句演示
    demonstrateAdvancedIteration()       // 高级迭代方法演示
    demonstrateErrorHandling()           // 异常处理演示
    demonstrateControlFlowJumps()        // 控制跳转演示
    demonstrateRealWorldScenarios()      // 实际应用场景演示
}
```

### 关键技术点演示

#### 1. 条件语句示例
```javascript
// 多层if-else
if (score >= 90) {
    grade = '优秀';
} else if (score >= 80) {
    grade = '良好';
} else if (score >= 60) {
    grade = '及格';
} else {
    grade = '不及格';
}

// switch语句
switch (day) {
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
        console.log('工作日');
        break;
    case 6:
    case 7:
        console.log('周末');
        break;
    default:
        console.log('无效日期');
}

// 三元运算符
const status = age >= 18 ? '成年人' : '未成年人';
const access = user && user.isActive ? '允许访问' : '拒绝访问';
```

#### 2. 循环语句示例
```javascript
// 传统for循环
for (let i = 0; i < array.length; i++) {
    console.log(array[i]);
}

// for...of循环 (推荐)
for (const item of array) {
    console.log(item);
}

// for...in循环 (对象属性)
for (const key in object) {
    if (object.hasOwnProperty(key)) {
        console.log(`${key}: ${object[key]}`);
    }
}

// while循环
let i = 0;
while (i < 5) {
    console.log(i++);
}

// do...while循环
do {
    console.log('至少执行一次');
} while (false);
```

#### 3. 数组高级方法
```javascript
const numbers = [1, 2, 3, 4, 5];

// map - 转换
const doubled = numbers.map(x => x * 2);

// filter - 筛选
const evens = numbers.filter(x => x % 2 === 0);

// reduce - 聚合
const sum = numbers.reduce((acc, x) => acc + x, 0);

// find - 查找
const firstEven = numbers.find(x => x % 2 === 0);

// some/every - 条件判断
const hasEven = numbers.some(x => x % 2 === 0);
const allPositive = numbers.every(x => x > 0);
```

#### 4. 异常处理示例
```javascript
// 基本try-catch
try {
    const result = riskyOperation();
    console.log(result);
} catch (error) {
    console.error('操作失败:', error.message);
} finally {
    cleanupResources();
}

// 自定义错误
class ValidationError extends Error {
    constructor(field, message) {
        super(message);
        this.field = field;
        this.name = 'ValidationError';
    }
}

// 异步错误处理
async function asyncOperation() {
    try {
        const result = await fetchData();
        return result;
    } catch (error) {
        throw new Error(`数据获取失败: ${error.message}`);
    }
}
```

## 🧪 测试覆盖

测试文件 `test_control_flow.js` 包含以下测试：

✅ 条件语句测试  
✅ 循环语句测试  
✅ 数组方法测试  
✅ 异常处理测试  
✅ 控制跳转测试  
✅ 实际应用场景测试  

## 🎯 实际应用场景

### 1. 数据验证场景
```javascript
function validateUserData(user) {
    const errors = [];
    
    // 条件验证
    if (!user.name || user.name.length < 2) {
        errors.push('姓名至少2个字符');
    }
    
    // 正则验证
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(user.email)) {
        errors.push('邮箱格式不正确');
    }
    
    // 范围验证
    if (user.age < 0 || user.age > 150) {
        errors.push('年龄范围0-150');
    }
    
    return errors;
}
```

### 2. 文件处理场景
```javascript
function processFiles(fileList) {
    for (const file of fileList) {
        try {
            if (file.size > MAX_FILE_SIZE) {
                console.log(`文件${file.name}过大，跳过处理`);
                continue;
            }
            
            if (file.type !== SUPPORTED_TYPE) {
                throw new Error(`不支持的文件类型: ${file.type}`);
            }
            
            await processFile(file);
            console.log(`文件${file.name}处理完成`);
            
        } catch (error) {
            console.error(`处理文件${file.name}时出错:`, error.message);
        }
    }
}
```

### 3. API响应处理
```javascript
async function handleApiResponse(response) {
    switch (response.status) {
        case 200:
            return response.data;
        case 401:
            throw new Error('未授权访问');
        case 404:
            throw new Error('资源不存在');
        case 500:
            throw new Error('服务器内部错误');
        default:
            throw new Error(`未知状态码: ${response.status}`);
    }
}
```

## ⚡ 最佳实践建议

### 1. 条件语句优化
- 优先使用卫语句(guard clauses)提前返回
- 复杂条件考虑提取为函数
- 合理使用三元运算符保持代码简洁

### 2. 循环使用建议
- 优先使用for...of而非传统for循环
- 避免在循环中进行重复计算
- 合理使用break和continue提高效率

### 3. 错误处理原则
- 具体错误具体处理
- 提供有意义的错误信息
- 及时清理资源避免内存泄漏

### 4. 性能考虑
- 减少嵌套层级
- 避免不必要的循环
- 合理使用缓存机制

## 🔍 常见问题和解决方案

### 1. 循环中的闭包问题
```javascript
// 问题：所有回调函数都引用同一个变量
for (var i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 100); // 输出: 3, 3, 3
}

// 解决：使用let或者立即执行函数
for (let i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 100); // 输出: 0, 1, 2
}
```

### 2. 异步操作的错误处理
```javascript
// 问题：Promise错误可能未被捕获
promise.then(result => {
    // 处理结果
}); // 错误可能丢失

// 解决：始终添加catch处理器
promise
    .then(result => { /* 处理结果 */ })
    .catch(error => { /* 处理错误 */ });
```

### 3. switch语句的fall-through
```javascript
// 问题：忘记break导致意外执行
switch (value) {
    case 1:
        console.log('one');
    case 2:  // 会继续执行!
        console.log('two');
        break;
}

// 解决：明确添加break或使用注释说明故意fall-through
switch (value) {
    case 1:
    case 2:
        console.log('one or two');
        break;
    default:
        console.log('other');
}
```

## 📚 扩展学习资源

### 官方文档
- [MDN JavaScript控制流](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Control_flow_and_error_handling)
- [Node.js错误处理](https://nodejs.org/api/errors.html)

### 推荐书籍
- 《JavaScript语言精粹》
- 《Effective JavaScript》
- 《Node.js实战》

### 相关链接
- JavaScript异步编程指南
- Node.js最佳实践

## 🔄 版本历史

- v1.0.0 (2024-01-15): 初始版本，包含完整的控制流演示

---
**注意**: 熟练掌握JavaScript控制流是编写高质量Node.js应用程序的基础，合理的控制结构能够显著提升代码的可读性和维护性。