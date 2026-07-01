<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 微信小程序云数据库演示

## 学习目标

1. 掌握云数据库 CRUD 操作
2. 理解数据库集合和记录概念
3. 学会使用云函数操作数据库
4. 实现数据的实时同步

## 环境要求

- 微信开发者工具 (启用云开发)
- 小程序已开通云开发能力

## 云数据库优势

```
传统方式                          云开发方式
┌─────────────┐                   ┌─────────────┐
│  自建数据库 │                   │  云数据库   │
│  需要服务端 │                   │  无需服务端 │
│  API 调用  │                   │  端直接操作 │
│  运维成本高 │                   │  自动扩容   │
└─────────────┘                   └─────────────┘
```

## 快速开始

### 1. 启用云开发

1. 打开微信开发者工具
2. 右键项目 → "更多工具" → "启用云开发"
3. 创建云环境

### 2. 创建集合

```javascript
// 初始化云数据库
const db = wx.cloud.database();

// 创建集合
db.createCollection('todos').then(res => {
  console.log('集合创建成功');
});
```

### 3. 定义数据结构

```javascript
// collection: users
{
  "_id": "xxxxx",
  "nickName": "张三",
  "avatarUrl": "https://...",
  "phone": "13800138000",
  "createdAt": Date("2026-05-09"),
  "updatedAt": Date("2026-05-09")
}
```

## CRUD 操作

### 创建记录 (C)

```javascript
const db = wx.cloud.database();

// 添加单条记录
const result = await db.collection('todos').add({
  data: {
    title: '学习微信小程序',
    completed: false,
    priority: 1,
    tags: ['前端', '微信'],
    createdAt: db.serverDate()
  }
});

console.log('记录 ID:', result._id);
```

### 查询记录 (R)

```javascript
// 查询所有记录
const { data } = await db.collection('todos').get();

// 条件查询
const { data } = await db.collection('todos')
  .where({ completed: false })
  .orderBy('createdAt', 'desc')
  .get();

// 分页查询
const { data } = await db.collection('todos')
  .skip(10)
  .limit(10)
  .get();

// 查询单条
const one = await db.collection('todos').doc('id').get();
```

### 更新记录 (U)

```javascript
// 更新单条
await db.collection('todos').doc('id').update({
  data: {
    completed: true,
    updatedAt: db.serverDate()
  }
});

// 批量更新
await db.collection('todos')
  .where({ completed: true })
  .update({
    data: { status: 'archived' }
  });
```

### 删除记录 (D)

```javascript
// 删除单条
await db.collection('todos').doc('id').remove();

// 批量删除
await db.collection('todos')
  .where({ completed: true, status: 'archived' })
  .remove();
```

## 云函数操作数据库

### 云函数示例 (cloudfunctions/crud/index.js)

```javascript
// 云函数入口文件
const cloud = require('wx-server-sdk');

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });

const db = cloud.database();

// 批量插入
exports.main = async (event, context) => {
  const { todos } = event;

  try {
    // 批量插入
    const result = await db.collection('todos').add({
      data: todos.map(t => ({
        ...t,
        createdAt: db.serverDate()
      }))
    });

    return { success: true, ids: result._id };
  } catch (e) {
    return { success: false, error: e.message };
  }
};
```

### 小程序调用云函数

```javascript
// 调用云函数
const result = await wx.cloud.callFunction({
  name: 'crud',
  data: {
    todos: [
      { title: '任务1', completed: false },
      { title: '任务2', completed: true }
    ]
  }
});

if (result.result.success) {
  console.log('批量插入成功');
}
```

## 实战案例 - 备忘录

### 页面结构 (pages/memo/memo.js)

```javascript
Page({
  data: {
    todos: [],
    inputValue: ''
  },

  onLoad() {
    this.fetchTodos();
  },

  // 获取待办列表
  async fetchTodos() {
    wx.showLoading({ title: '加载中...' });

    const { data } = await db.collection('todos')
      .orderBy('createdAt', 'desc')
      .get();

    this.setData({ todos: data });
    wx.hideLoading();
  },

  // 添加待办
  async addTodo() {
    const title = this.data.inputValue.trim();
    if (!title) return;

    await db.collection('todos').add({
      data: {
        title,
        completed: false,
        createdAt: db.serverDate()
      }
    });

    this.setData({ inputValue: '' });
    this.fetchTodos();
  },

  // 切换状态
  async toggleTodo(e) {
    const id = e.currentTarget.dataset.id;
    const todo = this.data.todos.find(t => t._id === id);

    await db.collection('todos').doc(id).update({
      data: { completed: !todo.completed }
    });

    this.fetchTodos();
  },

  // 删除待办
  async removeTodo(e) {
    const id = e.currentTarget.dataset.id;

    await db.collection('todos').doc(id).remove();
    this.fetchTodos();
  }
});
```

## 常见问题

### Q1: 如何实现实时更新？

使用 `database.observe` 监听数据变化：

```javascript
db.collection('todos')
  .where({ completed: false })
  .watch({
    onChange: (snapshot) => {
      this.setData({ todos: snapshot.docChanges });
    },
    onError: (err) => {
      console.error('监听失败', err);
    }
  });
```

### Q2: 如何保证数据安全？

1. 在云控制台设置集合权限
2. 使用云函数进行敏感操作
3. 避免前端直接操作敏感数据

---

**技术栈**: 微信小程序 | 云开发 | 云数据库 | 云函数

**版本**: 1.0.0
## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

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

```bash
# 请根据实际案例替换
./scripts/demo.sh
```
