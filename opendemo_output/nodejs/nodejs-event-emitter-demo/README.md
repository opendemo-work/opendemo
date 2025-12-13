# Node.js事件发射器实战演示

## 简介
本演示项目展示了Node.js中`EventEmitter`类的核心用法，涵盖自定义事件、异步通信和错误处理等常见场景。通过三个递进式示例帮助开发者掌握事件驱动编程模式。

## 学习目标
- 理解EventEmitter的基本工作原理
- 掌握事件绑定与触发的实践技巧
- 学会使用once方法处理一次性事件
- 实践错误传播机制

## 环境要求
- Node.js >= 14.0.0
- npm（随Node.js自动安装）
- 任意操作系统（Windows/Linux/Mac）

## 安装依赖步骤
```bash
# 克隆项目或创建新目录
mkdir event-demo && cd event-demo

# 将本项目文件保存到当前目录
# 包括 emitter-basic.js, emitter-async.js, package.json

# 安装依赖（本项目无外部依赖，仅需初始化）
npm init -y
```

## 文件说明
- `emitter-basic.js`: 基础事件监听与发射示例
- `emitter-async.js`: 异步操作中的事件通信示例
- `package.json`: 项目依赖声明文件

## 逐步实操指南

### 第一步：运行基础事件示例
```bash
node emitter-basic.js
```
**预期输出**：
```
用户已登录：Alice
欢迎消息已发送
一次性通知已触发
错误被捕获：数据加载失败
```

### 第二步：运行异步事件示例
```bash
node emitter-async.js
```
**预期输出**：
```
开始获取用户数据...
缓存命中：user_123
数据验证通过：{ id: 'user_123', name: 'Alice' }
最终接收到的数据：{ id: 'user_123', name: 'Alice' }
```

## 代码解析

### emitter-basic.js 关键段
```javascript
// 使用原生events模块
const EventEmitter = require('events');

// 继承EventEmitter实现自定义事件类
class LoginEmitter extends EventEmitter {}
```
这是创建可发射事件对象的标准方式。

```javascript
// once用于注册只执行一次的监听器
loginEmitter.once('notification', () => {
  console.log('一次性通知已触发');
});
```
`once`确保事件处理器只会被调用一次，常用于初始化完成等场景。

### emitter-async.js 关键段
```javascript
setTimeout(() => {
  if (Math.random() < 0.3) {
    emitter.emit('error', new Error('网络请求超时'));
  } else {
    emitter.emit('data', { id: 'user_123', name: 'Alice' });
  }
}, 1000);
```
在异步回调中发射事件，模拟真实API请求行为。

## 预期输出示例
完整输出见“逐步实操指南”部分。

## 常见问题解答

**Q: 如何移除事件监听器？**
A: 使用`removeListener(event, listener)`方法，注意必须传入原始函数引用。

**Q: 可以监听所有事件吗？**
A: 不推荐，但可通过特殊事件`newListener`监控新的监听器注册。

**Q: EventEmitter有内存泄漏风险吗？**
A: 是的，默认最大监听器数量为10，超过会警告。可用`emitter.setMaxListeners(n)`调整。

## 扩展学习建议
- 阅读Node.js官方文档中events模块章节
- 学习Stream API（基于EventEmitter构建）
- 探索第三方库如`mitt`了解轻量级替代方案
- 实践将EventEmitter与Promise结合使用