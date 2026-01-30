# Node.js 正则表达式（RegExp）文本匹配验证 Demo

## 简介
本项目是一个面向初学者到中级开发者的 Node.js 实例，展示了如何使用 JavaScript 内置的 `RegExp` 对象对常见文本格式（如邮箱、手机号、密码强度）进行验证。通过三个独立示例，帮助理解正则表达式的构造与应用。

## 学习目标
- 掌握 JavaScript 中 RegExp 的基本语法和用法
- 学会编写用于常见场景的正则表达式
- 理解 test() 和 match() 方法的区别与应用场景
- 遵循 Node.js 最佳实践进行模块化编码

## 环境要求
- Node.js 版本：v14.x 或更高（推荐 v16+）
- 操作系统：Windows / macOS / Linux（跨平台兼容）
- 包管理器：npm（随 Node.js 自动安装）

## 安装依赖的详细步骤
该项目不依赖第三方库，仅使用 Node.js 内建功能，无需额外安装依赖。

1. 确保已安装 Node.js：
   ```bash
   node --version
   ```
   预期输出：`v16.x.x` 或类似版本号

2. 克隆或创建项目目录并放入以下文件：
   - `validation-email.js`
   - `validation-phone.js`
   - `validation-password.js`

3. 进入项目目录：
   ```bash
   cd your-project-folder
   ```

## 文件说明
| 文件名 | 功能 |
|--------|------|
| `validation-email.js` | 验证电子邮件地址格式 |
| `validation-phone.js` | 验证中国大陆手机号码 |
| `validation-password.js` | 验证密码强度（至少8位，含大小写字母和数字） |

## 逐步实操指南

### 步骤 1：运行邮箱验证
```bash
node validation-email.js
```
**预期输出**：
```
✅ 'test@example.com' 是合法邮箱
❌ 'invalid-email' 不是合法邮箱
```

### 步骤 2：运行手机号验证
```bash
node validation-phone.js
```
**预期输出**：
```
✅ '13812345678' 是合法手机号
❌ '12345678901' 不是合法手机号
❌ '1381234567' 位数不足，不是合法手机号
```

### 步骤 3：运行密码强度验证
```bash
node validation-password.js
```
**预期输出**：
```
✅ 'Abc12345' 密码强度合格
❌ 'abc123' 太短且缺少大写字母
❌ 'password' 缺少数字和大写字母
```

## 代码解析

### 1. 正则表达式定义方式
```js
const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
```
- `^` 表示字符串开始
- `[a-zA-Z0-9._%+-]+` 匹配用户名部分（允许字母、数字及常见符号）
- `@` 字面量匹配 @ 符号
- `\.` 转义点号
- `{2,}` 表示顶级域名至少两位
- `$` 表示字符串结束

### 2. 使用 .test() 方法
`.test()` 返回布尔值，适合条件判断：
```js
if (regex.test(input)) { ... }
```

### 3. 模块化设计
每个文件独立可执行，便于测试和复用。

## 常见问题解答

**Q: 为什么正则中要用双反斜杠 `\\.`？**
A: 因为在 JavaScript 字符串中，反斜杠需要转义，所以 `\.` 才能表示字面量 `.`。

**Q: 如何调试正则表达式？**
A: 可使用 [regex101.com](https://regex101.com/) 在线工具测试表达式逻辑。

**Q: 是否可以使用 new RegExp() 构造函数？**
A: 可以，但字面量 `/.../` 更简洁高效，推荐用于静态正则。

## 扩展学习建议
- 学习 RegExp 的标志（flags）：`i`（忽略大小写）、`g`（全局匹配）等
- 尝试捕获组（Capturing Groups）提取子字符串
- 结合 Express.js 构建 API 接口进行请求参数校验
- 使用 Joi 或 Yup 等库实现更复杂的表单验证