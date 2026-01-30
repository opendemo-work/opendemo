# Jest Mock模拟单元测试Demo

## 简介
本项目是一个完整的Jest Mock模拟演示，展示了在Node.js环境中如何使用Jest进行函数模拟、模块模拟和异步API模拟。通过三个具体场景帮助开发者掌握Mock的核心用法。

## 学习目标
- 理解Jest中mock的概念和用途
- 掌握函数级别的模拟（function mocking）
- 学会模拟外部模块依赖
- 掌握异步函数的模拟测试
- 熟悉Jest提供的mock工具方法

## 环境要求
- Node.js 14.x 或更高版本
- npm 6.x 或更高版本
- 操作系统：Windows / Linux / macOS（跨平台兼容）

## 安装依赖的详细步骤

```bash
# 1. 克隆项目或创建项目目录
mkdir jest-mock-demo && cd jest-mock-demo

# 2. 初始化npm项目
npm init -y

# 3. 安装Jest作为开发依赖
npm install --save-dev jest@^29.0.0

# 4. 将package.json中的test脚本改为使用Jest
# 添加或修改scripts字段：
# "scripts": { "test": "jest" }
```

## 文件说明
- `math.js`：包含待测试的数学计算函数
- `apiClient.js`：模拟外部API客户端
- `userService.js`：使用API客户端的业务逻辑层
- `math.test.js`：测试math.js中的函数，演示函数mock
- `userService.test.js`：测试userService.js，演示模块mock和异步mock

## 逐步实操指南

### 步骤1：创建源代码文件
```bash
mkdir src tests
```

将math.js和apiClient.js内容复制到src/目录下，将userService.js也放入src/目录。

### 步骤2：创建测试文件
将math.test.js和userService.test.js内容复制到tests/目录下。

### 步骤3：配置package.json
确保package.json包含以下脚本：
```json
"scripts": {
  "test": "jest",
  "test:watch": "jest --watch"
}
```

### 步骤4：运行测试
```bash
# 运行所有测试
npm test

# 预期输出：
# PASS  tests/math.test.js
# PASS  tests/userService.test.js
# 
# Test Suites: 2 passed, 2 total
# Tests:       5 passed, 5 total
```

## 代码解析

### math.test.js 关键点
- 使用`jest.fn()`创建模拟函数
- 使用`.mockReturnValue()`定义返回值
- 验证模拟函数被调用的情况（次数、参数）

### userService.test.js 关键点
- 使用`jest.mock('../src/apiClient')`自动模拟整个模块
- 模拟异步函数返回Promise
- 使用`expect.assertions()`确保异步断言被执行

## 预期输出示例
```
PASS  tests/math.test.js
PASS  tests/userService.test.js

Test Suites: 2 passed, 2 total
Tests:       5 passed, 5 total
Snapshots:   0 total
Time:        0.567 s, estimated 1 s
Ran all test suites.
```

## 常见问题解答

**Q: 运行测试时报错“jest不是内部或外部命令”？**
A: 请确认已全局安装jest或使用npx：`npx jest`

**Q: 如何调试Jest测试？**
A: 可以在VS Code中配置launch.json，或使用`console.log`+`npx jest --silent=false`

**Q: mock函数没有被调用怎么办？**
A: 检查是否正确地将mock函数传入了被测函数，或是否需要使用`jest.mock()`自动模拟

## 扩展学习建议
- 学习Jest的`mockImplementation`和`mockImplementationOnce`
- 探索自动mock与手动mock的区别
- 了解`__mocks__`目录的使用
- 学习如何模拟定时器（setTimeout等）
- 实践快照测试（Snapshot Testing）