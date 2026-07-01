<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 微信小程序登录与 JWT 鉴权演示

## 学习目标

1. 掌握微信小程序登录流程
2. 理解 JWT Token 鉴权机制
3. 学会状态管理和持久化
4. 实现登录拦截和自动登录

## 环境要求

- 微信开发者工具
- Node.js 16+ (后端环境)
- 已申请 AppID

## 登录流程

```
┌─────────┐                      ┌─────────┐                     ┌─────────┐
│小程序端 │                      │后端服务 │                     │微信服务器 │
└────┬────┘                      └────┬────┘                     └────┬────┘
     │                                │                               │
     │ 1. wx.login() 获取 code        │                               │
     │───────────────────────────────> │                               │
     │                                │ 2. code + appId + secret       │
     │                                │───────────────────────────────>│
     │                                │                               │
     │                                │ 3. openid + session_key        │
     │                                │<───────────────────────────────│
     │                                │                               │
     │                                │ 4. 生成 JWT 返回               │
     │ 5. 返回 JWT + 用户信息          │                               │
     │<───────────────────────────────│                               │
     │                                │                               │
     │ 6. 存储 token                  │                               │
```

## 快速开始

### 后端服务

```bash
cd wechat-miniprogram-login/server
npm install
node server.js
```

### 小程序端

1. 打开微信开发者工具
2. 导入 `code` 目录
3. 配置服务器域名 (需在 MP 后台设置)
4. 编译运行

## 核心代码解析

### 前端 - 登录流程 (pages/login/login.js)

```javascript
Page({
  data: {
    canIUse: wx.canIUse('button.open-type.getUserProfile')
  },

  // 微信登录
  async handleWxLogin() {
    // 1. 获取 code
    const { code } = await wx.login();

    // 2. 发送到后端获取 token
    const res = await wx.request({
      url: 'https://api.example.com/wx/login',
      method: 'POST',
      data: { code }
    });

    if (res.data.token) {
      // 3. 存储 token
      wx.setStorageSync('token', res.data.token);
      wx.setStorageSync('userInfo', res.data.userInfo);

      // 4. 跳转首页
      wx.switchTab({ url: '/pages/index/index' });
    }
  },

  // 获取用户信息
  async handleGetUserInfo(e) {
    if (!e.detail.userInfo) return;

    const { avatarUrl, nickName } = e.detail.userInfo;

    // 存储用户信息
    wx.setStorageSync('userInfo', { avatarUrl, nickName });

    // 继续登录流程
    this.handleWxLogin();
  }
});
```

### 后端 - JWT 生成 (server/app.js)

```javascript
const express = require('express');
const jwt = require('jsonwebtoken');
const axios = require('axios');
const app = express();

const WX_APPID = 'your-appid';
const WX_SECRET = 'your-secret';
const JWT_SECRET = 'your-jwt-secret';

app.post('/wx/login', async (req, res) => {
  const { code } = req.body;

  try {
    // 1. 用 code 换取 openid
    const wxRes = await axios.get(
      `https://api.weixin.qq.com/sns/jscode2session`, {
        params: {
          appid: WX_APPID,
          secret: WX_SECRET,
          js_code: code,
          grant_type: 'authorization_code'
        }
      }
    );

    const { openid, session_key } = wxRes.data;

    // 2. 生成 JWT
    const token = jwt.sign(
      { openid, exp: Math.floor(Date.now() / 1000) + 7200 },
      JWT_SECRET
    );

    // 3. 返回给前端
    res.json({
      code: 0,
      token,
      userInfo: { openid }
    });

  } catch (e) {
    res.json({ code: -1, msg: '登录失败' });
  }
});

// JWT 中间件
const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({ code: -1, msg: '未登录' });
  }

  try {
    req.user = jwt.verify(token, JWT_SECRET);
    next();
  } catch (e) {
    res.status(401).json({ code: -1, msg: 'token 失效' });
  }
};

// 受保护的接口
app.get('/api/user/info', authMiddleware, (req, res) => {
  res.json({
    code: 0,
    data: { openid: req.user.openid, vip: true }
  });
});
```

## 状态管理

### App 全局状态 (app.js)

```javascript
App({
  globalData: {
    token: '',
    userInfo: null
  },

  onLaunch() {
    // 检查登录状态
    this.checkLoginStatus();
  },

  checkLoginStatus() {
    const token = wx.getStorageSync('token');
    const userInfo = wx.getStorageSync('userInfo');

    if (token && userInfo) {
      this.globalData.token = token;
      this.globalData.userInfo = userInfo;
    }
  }
});
```

### 登录拦截器

```javascript
const checkLogin = () => {
  const token = wx.getStorageSync('token');
  if (!token) {
    wx.showModal({
      title: '请先登录',
      content: '是否跳转到登录页？',
      success: (res) => {
        if (res.confirm) {
          wx.navigateTo({ url: '/pages/login/login' });
        }
      }
    });
    return false;
  }
  return true;
};
```

## 常见问题

### Q1: 如何处理 token 过期？

```javascript
// 请求拦截器
const request = (options) => {
  return wx.request({
    ...options,
    fail: (err) => {
      if (err.statusCode === 401) {
        // 清除 token，重新登录
        wx.removeStorageSync('token');
        wx.navigateTo({ url: '/pages/login/login' });
      }
    }
  });
};
```

### Q2: 如何实现自动登录？

```javascript
// app.js
onLaunch() {
  const token = wx.getStorageSync('token');
  if (!token) {
    // 静默登录
    wx.login({ success: (res) => this.autoLogin(res.code) });
  }
}
```

---

**技术栈**: 微信小程序 | JWT | Node.js/Express | 微信登录

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
