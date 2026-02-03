# NodeJS单元测试与覆盖率实战Demo

## 简介
本项目是一个完整的Node.js示例，演示如何使用Jest和Mocha/Chai进行单元测试，并通过`nyc`生成测试覆盖率报告。涵盖同步函数、异步操作的测试场景，以及跨平台运行方式。

## 学习目标
- 掌握使用Jest编写单元测试
- 学会使用Mocha + Chai进行BDD风格测试
- 理解如何生成和解读测试覆盖率报告
- 实践行业标准的测试目录结构与配置

## 环境要求
- Node.js 16.x 或更高版本（LTS推荐）
- npm 8+（随Node.js自动安装）
- 操作系统：Windows、macOS、Linux 均支持

## 安装依赖的详细步骤

1. 克隆或创建项目目录后，打开终端进入项目根目录
2. 执行以下命令安装所需依赖：

```bash
npm init -y
npm install --save-dev jest mocha chai nyc
```

## 文件说明
- `src/calculator.js`：被测的业务逻辑模块（计算器功能）
- `test/jest.test.js`：使用Jest编写的测试文件
- `test/mocha.test.js`：使用Mocha + Chai编写的测试文件
- `package.json`：已包含测试脚本配置

## 逐步实操指南

### 步骤1：运行Jest测试
```bash
npx jest
```
**预期输出**：
> PASS  test/jest.test.js
> ✓ 加法函数应正确相加 (5ms)
> ✓ 异步获取数据应返回正确结果 (10ms)

### 步骤2：运行Mocha测试
```bash
npx mocha test/mocha.test.js
```
**预期输出**：
> 
>   ✔ 加法函数应正确相加
>   ✔ 异步操作应成功解析
> 
>   2 passing (8ms)

### 步骤3：生成测试覆盖率报告（使用nyc + Mocha）
```bash
npx nyc --reporter=html --reporter=text npx mocha test/mocha.test.js
```
或使用预设脚本：
```bash
npm run coverage
```
**预期输出**：
- 控制台显示文本覆盖率统计
- 生成 `/coverage/index.html` 可视化报告

## 代码解析

### calculator.js
实现了简单的同步加法和异步数据获取函数，用于测试演示。

### jest.test.js
使用Jest的`test()`和`expect()`断言语法，测试同步与异步函数，展示了`.resolves`匹配器用法。

### mocha.test.js
使用Mocha的`describe`/`it`结构和Chai的`expect`断言库，体现BDD风格测试写法。

## 预期输出示例
```
PASS  test/jest.test.js
✓ 加法函数应正确相加 (5ms)
✓ 异步获取数据应返回正确结果 (10ms)

Test Suites: 1 passed, 1 total
Tests:       2 passed, 2 total
```

## 常见问题解答

**Q：运行nyc时报错找不到mocha？**
A：确保`nyc`和`mocha`都已通过`--save-dev`安装，并使用`npx`调用。

**Q：覆盖率报告未包含某文件？**
A：检查源文件是否被正确引用，且路径在`nyc`可扫描范围内。

**Q：Jest提示Cannot find module？**
A：确认文件路径大小写正确，Node.js默认区分路径大小写（Linux/macOS）。

## 扩展学习建议
- 尝试为复杂对象或API接口编写模拟测试（mock/fake）
- 集成到CI/CD流程中（如GitHub Actions）
- 学习使用Sinon进行更高级的Spy/Stubs/Mocks
- 探索Puppeteer进行端到端测试