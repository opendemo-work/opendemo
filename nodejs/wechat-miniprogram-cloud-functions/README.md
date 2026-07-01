<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 微信小程序云函数演示

## 学习目标

1. 掌握云函数编写和部署
2. 理解云函数与云数据库的配合
3. 学会文件上传和触发器配置
4. 实现定时任务和 HTTP 触发

## 环境要求

- 微信开发者工具 (启用云开发)
- 云环境已创建

## 云函数架构

```
┌──────────────┐
│  小程序端    │
│  wx.cloud    │
│  .callFunc() │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   云函数     │
│  wx-server  │
│    -sdk     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  云数据库    │
│  云存储      │
│  外部 API    │
└──────────────┘
```

## 快速开始

### 1. 创建云函数

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 在 cloudfunctions 目录右键
# "新建 Node.js 云函数"
# 命名为 getUserInfo
```

### 2. 编写云函数

```javascript
// cloudfunctions/getUserInfo/index.js
const cloud = require('wx-server-sdk');

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });

const db = cloud.database();

exports.main = async (event, context) => {
  const { userId } = event;

  try {
    // 查询用户信息
    const { data } = await db.collection('users')
      .doc(userId)
      .get();

    return {
      success: true,
      data: data[0]
    };
  } catch (e) {
    return {
      success: false,
      error: e.message
    };
  }
};
```

### 3. 部署云函数

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 右键云函数目录
# "上传并部署"
```

### 4. 小程序端调用

```javascript
// 调用云函数
const result = await wx.cloud.callFunction({
  name: 'getUserInfo',
  data: { userId: 'xxxxx' }
});

if (result.result.success) {
  console.log('用户信息:', result.result.data);
}
```

## 云函数进阶

### 文件上传云存储

```javascript
// cloudfunctions/uploadFile/index.js
const cloud = require('wx-server-sdk');
const fs = require('fs');

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });

exports.main = async (event, context) => {
  const { fileContent, fileName } = event;

  try {
    // 上传到云存储
    const uploadResult = await cloud.uploadFile({
      cloudPath: `uploads/${Date.now()}_${fileName}`,
      fileContent: Buffer.from(fileContent, 'base64')
    });

    return {
      success: true,
      fileID: uploadResult.fileID
    };
  } catch (e) {
    return { success: false, error: e.message };
  }
};
```

### 发送 HTTP 请求

```javascript
// 云函数中调用外部 API
const https = require('https');

exports.main = async (event, context) => {
  return new Promise((resolve, reject) => {
    https.get('https://api.example.com/data', (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve({ success: true, data: JSON.parse(data) });
        } catch (e) {
          resolve({ success: true, data });
        }
      });
    }).on('error', (e) => {
      resolve({ success: false, error: e.message });
    });
  });
};
```

### 定时触发器

在 `config.json` 中配置：

```json
{
  "triggers": [
    {
      "name": "myTrigger",
      "type": "timer",
      "config": "0 0 2 * * * *"  // 每天凌晨 2 点执行
    }
  ]
}
```

```javascript
// cloudfunctions/dailyTask/index.js
const cloud = require('wx-server-sdk');

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });

const db = cloud.database();

// 定时清理过期数据
exports.main = async (event, context) => {
  if (event.triggerName !== 'myTrigger') {
    return { success: false, msg: '非定时触发' };
  }

  const now = new Date();
  const thirtyDaysAgo = new Date(now - 30 * 24 * 60 * 60 * 1000);

  try {
    // 删除 30 天前的过期记录
    const result = await db.collection('cache')
      .where({
        expireAt: db.command.lt(thirtyDaysAgo)
      })
      .remove();

    return {
      success: true,
      deleted: result.deleted
    };
  } catch (e) {
    return { success: false, error: e.message };
  }
};
```

### HTTP 触发云函数

```javascript
// 导出 HTTP 触发入口
exports.main = async (event, context) => {
  const httpMethod = event.httpMethod;
  const path = event.path;
  const queryString = event.queryString;

  if (path === '/api/health') {
    return { statusCode: 200, body: 'OK' };
  }

  return { statusCode: 404, body: 'Not Found' };
};
```

## 错误处理

```javascript
exports.main = async (event, context) => {
  try {
    // 业务逻辑
    const result = await someOperation();
    return { success: true, data: result };

  } catch (e) {
    // 记录错误日志
    console.error('云函数错误:', e);

    // 返回友好错误
    return {
      success: false,
      error: e.message || '服务器内部错误',
      code: e.code || 'INTERNAL_ERROR'
    };
  }
};
```

## 常见问题

### Q1: 云函数超时怎么办？

默认超时 20 秒，可通过控制台调整到 60 秒。对于耗时操作：
- 使用异步队列处理
- 分批处理数据
- 启用并发调用

### Q2: 如何调试云函数？

```javascript
// 启用调试模式
cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV,
  traceUser: true
});

// 本地日志输出
console.log('event:', event);
console.log('context:', context);
```

---

**技术栈**: 微信小程序 | 云函数 | Node.js | 云存储

**版本**: 1.0.0
## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/demo.sh
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际案例替换
./scripts/demo.sh
```
