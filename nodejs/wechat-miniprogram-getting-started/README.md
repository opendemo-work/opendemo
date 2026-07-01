<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 微信小程序入门演示

## 学习目标

1. 理解微信小程序项目结构
2. 掌握小程序生命周期函数
3. 学会使用 WXML、WXSS、JS 三件套
4. 配置小程序 AppID 和调试

## 环境要求

- 微信开发者工具 (最新版本)
- Node.js 18+
- 微信小程序 AppID (个人可申请测试号)

## 项目结构

```
wechat-miniprogram-getting-started/
├── code/                      # 主要代码
│   ├── app.js                # 应用入口
│   ├── app.json             # 应用配置
│   ├── app.wxss             # 全局样式
│   ├── pages/               # 页面目录
│   │   ├── index/           # 首页
│   │   │   ├── index.js
│   │   │   ├── index.wxml
│   │   │   └── index.wxss
│   │   └── logs/            # 日志页
│   └── utils/               # 工具函数
│       └── request.js
├── components/              # 自定义组件
├── cloudfunctions/          # 云函数
├── cloud/                   # 云开发资源
└── README.md
```

## 快速开始

### 1. 创建项目

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 克隆本项目后
cd wechat-miniprogram-getting-started/code

# 安装依赖 (如需要 npm 包)
npm install
```

### 2. 打开项目

1. 打开微信开发者工具
2. 点击 "导入项目"
3. 选择 `code` 目录
4. 填写 AppID (测试号或正式 AppID)

### 3. 运行预览

点击 "编译" → "预览" → 扫码查看效果

## 核心概念详解

### 小程序生命周期

```javascript
// app.js
App({
  onLaunch() {
    // 小程序启动时执行
    console.log('小程序启动了');
  },

  onShow() {
    // 小程序显示时执行 (切入前台)
  },

  onHide() {
    // 小程序隐藏时执行 (切入后台)
  }
});
```

### 页面生命周期

```javascript
// pages/index/index.js
Page({
  data: {
    // 页面数据 (响应式)
    message: 'Hello OpenDemo',
    count: 0
  },

  onLoad(options) {
    // 页面加载时执行
    // options: 路由参数
  },

  onShow() {
    // 页面显示时执行
  },

  onReady() {
    // 页面初次渲染完成
  },

  onHide() {
    // 页面隐藏时执行
  },

  onUnload() {
    // 页面卸载时执行
  },

  // 自定义方法
  handleTap() {
    this.setData({ count: this.data.count + 1 });
  }
});
```

### WXML 模板

```html
<!-- pages/index/index.wxml -->
<view class="container">
  <text class="title">{{message}}</text>

  <button bindtap="handleTap">点击次数: {{count}}</button>

  <block wx:for="{{list}}" wx:key="id">
    <view class="item">{{item.name}}</view>
  </block>
</view>
```

### WXSS 样式

```css
/* pages/index/index.wxss */
.container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

button {
  margin-top: 20px;
  background-color: #07c160;
  color: white;
  width: 200px;
}

.item {
  padding: 10px;
  border-bottom: 1px solid #eee;
}
```

## 代码解析

### app.js - 应用入口

```javascript
// 小程序入口文件
App({
  globalData: {
    // 全局数据
    userInfo: null,
    apiBase: 'https://api.example.com'
  },

  onLaunch() {
    // 检查登录状态
    this.checkLogin();

    // 获取系统信息
    const systemInfo = wx.getSystemInfoSync();
    console.log('系统信息:', systemInfo);
  },

  checkLogin() {
    const token = wx.getStorageSync('token');
    if (!token) {
      // 跳转到登录页
      // wx.navigateTo({ url: '/pages/login/login' });
    }
  }
});
```

### app.json - 应用配置

```json
{
  "pages": [
    "pages/index/index",
    "pages/logs/logs"
  ],
  "window": {
    "backgroundTextStyle": "light",
    "navigationBarBackgroundColor": "#07c160",
    "navigationBarTitleText": "OpenDemo",
    "navigationBarTextStyle": "white"
  },
  "tabBar": {
    "color": "#999",
    "selectedColor": "#07c160",
    "list": [
      { "pagePath": "pages/index/index", "text": "首页" },
      { "pagePath": "pages/logs/logs", "text": "日志" }
    ]
  },
  "style": "v2",
  "sitemapLocation": "sitemap.json"
}
```

### utils/request.js - 网络请求封装

```javascript
/**
 * 请求封装
 */
const request = (options) => {
  return new Promise((resolve, reject) => {
    const app = getApp();

    wx.showLoading({ title: options.loading || '加载中...' });

    wx.request({
      url: app.globalData.apiBase + options.url,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'Content-Type': 'application/json',
        'Authorization': wx.getStorageSync('token') || ''
      },
      success: (res) => {
        if (res.data.code === 0) {
          resolve(res.data.data);
        } else {
          wx.showToast({ title: res.data.msg, icon: 'none' });
          reject(res.data);
        }
      },
      fail: (err) => {
        wx.showToast({ title: '网络请求失败', icon: 'none' });
        reject(err);
      },
      complete: () => {
        wx.hideLoading();
      }
    });
  });
};

module.exports = { request };
```

### pages/index/index.js - 首页逻辑

```javascript
const { request } = require('../../utils/request');

Page({
  data: {
    message: '欢迎来到 OpenDemo',
    count: 0,
    list: [
      { id: 1, name: '微信小程序入门' },
      { id: 2, name: '云开发实战' },
      { id: 3, name: '登录与鉴权' }
    ],
    userInfo: null
  },

  onLoad() {
    // 页面加载时获取数据
    this.fetchData();
  },

  onShow() {
    // 每次显示时检查登录
    const userInfo = wx.getStorageSync('userInfo');
    if (userInfo) {
      this.setData({ userInfo });
    }
  },

  handleTap() {
    this.setData({
      count: this.data.count + 1
    });
  },

  async fetchData() {
    try {
      // 模拟获取数据
      // const data = await request({ url: '/api/list' });
      // this.setData({ list: data });
    } catch (e) {
      console.error('获取数据失败', e);
    }
  },

  goToDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
    });
  }
});
```

### pages/index/index.wxml - 首页模板

```html
<view class="container">
  <!-- 头部欢迎 -->
  <view class="header">
    <text class="title">{{message}}</text>
    <text class="subtitle" wx:if="{{userInfo}}">
      欢迎, {{userInfo.nickName}}
    </text>
  </view>

  <!-- 点击计数 -->
  <view class="counter">
    <button type="primary" bindtap="handleTap">
      点击次数: {{count}}
    </button>
  </view>

  <!-- 列表展示 -->
  <view class="list">
    <text class="section-title">学习路线</text>
    <view
      class="list-item"
      wx:for="{{list}}"
      wx:key="id"
      bindtap="goToDetail"
      data-id="{{item.id}}"
    >
      <text class="item-name">{{item.name}}</text>
      <text class="item-arrow">></text>
    </view>
  </view>

  <!-- 底部信息 -->
  <view class="footer">
    <text class="footer-text">OpenDemo 微信小程序入门教程</text>
  </view>
</view>
```

### pages/index/index.wxss - 首页样式

```css
.container {
  padding: 30rpx;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.header {
  text-align: center;
  padding: 40rpx 0;
  background: linear-gradient(#07c160, #039c4d);
  border-radius: 20rpx;
  margin-bottom: 30rpx;
}

.title {
  display: block;
  font-size: 40rpx;
  font-weight: bold;
  color: white;
}

.subtitle {
  display: block;
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.9);
  margin-top: 10rpx;
}

.counter {
  text-align: center;
  margin-bottom: 30rpx;
}

.list {
  background: white;
  border-radius: 20rpx;
  padding: 20rpx;
}

.section-title {
  display: block;
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  padding-bottom: 20rpx;
  border-bottom: 1px solid #eee;
  margin-bottom: 20rpx;
}

.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30rpx 0;
  border-bottom: 1px solid #f5f5f5;
}

.list-item:last-child {
  border-bottom: none;
}

.item-name {
  font-size: 30rpx;
  color: #333;
}

.item-arrow {
  color: #999;
  font-size: 28rpx;
}

.footer {
  text-align: center;
  padding: 40rpx 0;
}

.footer-text {
  font-size: 24rpx;
  color: #999;
}
```

## 常见问题

### Q1: 如何申请测试 AppID？

1. 访问 [微信公众平台](https://mp.weixin.qq.com/)
2. 注册小程序账号
3. 进入 "开发管理" → "开发设置"
4. 获取 AppID (测试号也可使用)

### Q2: 真机调试无法请求本地接口？

开发工具默认支持 localhost，但真机需要：
- 使用内网穿透工具 (如 ngrok)
- 配置 HTTPS 域名
- 小程序后台添加合法域名

### Q3: 如何提高小程序性能？

1. 减少 setData 频率和数据量
2. 使用分包加载
3. 合理使用组件
4. 开启骨骼屏功能

## 扩展学习

- [微信小程序官方文档](https://developers.weixin.qq.com/miniprogram/dev/framework/)
- [小程序云开发指南](https://developers.weixin.qq.com/miniprogram/dev/wxcloud/)
- [Vant Weapp 组件库](https://youzan.github.io/vant-weapp/)

---

**技术栈**: 微信小程序 | WXML | WXSS | JavaScript | 云开发

**维护者**: OpenDemo Team

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
