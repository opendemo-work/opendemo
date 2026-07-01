<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 微信小程序支付集成演示

## 学习目标

1. 掌握微信支付整体流程
2. 理解统一下单 API
3. 学会支付回调处理
4. 实现订单查询和管理

## 环境要求

- 已认证的小程序账号
- 已开通微信支付
- 后端服务 (需 HTTPS + 域名备案)

## 支付流程

```
┌─────────┐                     ┌─────────────┐                     ┌─────────────┐
│小程序端 │                      │后端服务      │                      │微信支付服务器│
└────┬────┘                      └──────┬──────┘                     └──────┬──────┘
     │                                │                               │
     │ 1. 发起支付请求                │                               │
     │──────────────────────────────>│                               │
     │                                │ 2. 统一下单 API                │
     │                                │──────────────────────────────>│
     │                                │                               │ 3. 返回 prepay_id
     │                                │<──────────────────────────────│
     │ 4. 返回支付参数                 │                               │
     │<──────────────────────────────│                               │
     │                                │                               │
     │ 5. wx.requestPayment()        │                               │
     │──────────────────────────────>│                               │
     │                                │ 6. 异步回调通知                 │
     │                                │<──────────────────────────────│
```

## 快速开始

### 后端服务 (server/)

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd server
npm install
# 配置 .env 文件
node app.js
```

### 小程序端

配置合法域名:
- 后端 API 域名需在 MP 后台配置

## 核心代码

### 后端 - 统一下单 (server/routes/pay.js)

```javascript
const express = require('express');
const router = express.Router();
const wxPay = require('wechat-pay');
const crypto = require('crypto');

const wxPayConfig = {
  mchid: 'YOUR_MCHID',
  partnerKey: 'YOUR_PARTNER_KEY',
  appid: 'YOUR_APPID',
  notifyUrl: 'https://yourdomain.com/pay/notify'
};

// 初始化支付
const pay = wxPay.init(wxPayConfig);

// 统一下单
router.post('/createOrder', async (req, res) => {
  const { orderId, totalFee, openid } = req.body;

  // 生成签名
  const timeStamp = Math.floor(Date.now() / 1000).toString();
  const nonceStr = crypto.randomBytes(16).toString('hex');

  const params = {
    body: 'OpenDemo 商品',
    attach: JSON.stringify({ orderId }),
    out_trade_no: orderId,
    total_fee: totalFee,      // 单位: 分
    spbill_create_ip: req.ip,
    openid: openid,
    trade_type: 'JSAPI'
  };

  try {
    const result = await pay.unifiedOrder(params);

    // 返回支付参数
    const paySign = crypto.createHash('md5')
      .update([wxPayConfig.appid, result.prepay_id, timeStamp, nonceStr, wxPayConfig.partnerKey].join('&'))
      .digest('hex');

    res.json({
      code: 0,
      data: {
        timeStamp,
        nonceStr,
        package: `prepay_id=${result.prepay_id}`,
        paySign,
        signType: 'MD5'
      }
    });
  } catch (e) {
    res.json({ code: -1, msg: '创建订单失败' });
  }
});

// 支付回调
router.post('/notify', (req, res) => {
  const xml = req.body;
  const signature = xml.sign;

  // 验证签名
  if (verifySign(xml)) {
    // 处理支付成功逻辑
    if (xml.result_code === 'SUCCESS') {
      // 更新订单状态
      // 发送通知等
      console.log('支付成功:', xml.out_trade_no);
    }
    res.reply('<xml><return_code><![CDATA[SUCCESS]]></return_code></xml>');
  } else {
    res.reply('<xml><return_code><![CDATA[FAIL]]></return_code></xml>');
  }
});

module.exports = router;
```

### 前端 - 发起支付 (pages/pay/pay.js)

```javascript
Page({
  data: {
    orderInfo: null,
    paying: false
  },

  // 获取订单信息
  async createOrder() {
    const openid = wx.getStorageSync('openid');

    // 1. 创建本地订单
    const orderId = 'ORDER_' + Date.now();

    // 2. 请求后端获取支付参数
    const res = await wx.request({
      url: 'https://api.example.com/pay/createOrder',
      method: 'POST',
      data: {
        orderId,
        totalFee: 1,  // 1分钱
        openid
      }
    });

    if (res.data.code === 0) {
      this.setData({ orderInfo: res.data.data });
    }
  },

  // 调起支付
  async handlePay() {
    if (this.data.paying) return;

    this.setData({ paying: true });

    try {
      await wx.requestPayment({
        timeStamp: this.data.orderInfo.timeStamp,
        nonceStr: this.data.orderInfo.nonceStr,
        package: this.data.orderInfo.package,
        paySign: this.data.orderInfo.paySign,
        signType: 'MD5'
      });

      wx.showToast({ title: '支付成功' });
      this.triggerEvent('paySuccess');

    } catch (e) {
      if (e.errMsg.includes('cancel')) {
        wx.showToast({ title: '用户取消支付', icon: 'none' });
      } else {
        wx.showToast({ title: '支付失败', icon: 'none' });
      }
    } finally {
      this.setData({ paying: false });
    }
  }
});
```

## 订单查询

### 前端 - 查询订单状态

```javascript
async queryOrderStatus(orderId) {
  const res = await wx.request({
    url: 'https://api.example.com/pay/query',
    data: { orderId }
  });

  if (res.data.trade_state === 'SUCCESS') {
    this.setData({ paid: true });
  }
}
```

## 常见问题

### Q1: 支付时提示" 商户需配置退款通知"？

需要在微信商户平台配置退款通知 URL，并启用退款权限。

### Q2: 如何处理重复支付？

在后端使用幂等设计：
- 使用订单号作为唯一索引
- 检查订单状态后再处理
- 使用数据库事务

### Q3: 沙箱环境下如何测试？

使用沙箱密钥测试：
1. 在商户平台开启沙箱模式
2. 获取沙箱密钥替换原密钥

---

**技术栈**: 微信小程序 | 微信支付 | Node.js/Express | 安全

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
