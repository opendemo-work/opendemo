<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 微信小程序 UI 组件库演示 (Vant Weapp)

## 学习目标

1. 掌握 Vant Weapp 组件库安装
2. 学会使用常用组件
3. 实现表单验证
4. 主题定制

## 环境要求

- 微信开发者工具
- npm 支持

## 安装 Vant Weapp

### 方式一: npm 安装

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 在项目目录执行
npm init -y
npm install vant-weapp -S
```

构建: 菜单 → 工具 → 构建 npm

### 方式二: 直接下载

从 [GitHub](https://github.com/youzan/vant-weapp) 下载源码，复制到项目

## 常用组件

### Button 按钮

```html
<van-button type="primary" size="large">主要按钮</van-button>
<van-button type="warning">警告按钮</van-button>
<van-button type="info">信息按钮</van-button>
<van-button type="default">默认按钮</van-button>
<van-button loading="{{loading}}" disabled="{{disabled}}">
  加载中
</van-button>
```

### Cell 单元格

```html
<van-cell-group>
  <van-cell title="标题" value="内容" />
  <van-cell
    title="带图标"
    value="内容"
    icon="{{info}}"
    is-link
  />
  <van-cell
    title="圆角"
    value="内容"
    border="{{false}}"
    radius
  />
</van-cell-group>
```

### Field 输入框

```html
<van-field
  value="{{ username }}"
  label="用户名"
  placeholder="请输入用户名"
  error="{{ usernameError }}"
  bind:change="onUsernameChange"
/>

<van-field
  value="{{ password }}"
  type="password"
  label="密码"
  placeholder="请输入密码"
  error="{{ passwordError }}"
  bind:change="onPasswordChange"
/>
```

### Toast 轻提示

```javascript
// 成功提示
wx.vant.showToast({
  message: '操作成功',
  type: 'success'
});

// 失败提示
wx.vant.showFailToast({
  message: '操作失败'
});

// 加载提示
wx.vant.showLoadingToast({
  message: '加载中...',
  forbidClick: true
});
```

### Dialog 对话框

```javascript
// 确认对话框
wx.vant.showDialog.confirm({
  title: '确认删除',
  message: '确定要删除这条记录吗？',
  async confirm() {
    await deleteItem();
    wx.vant.showToast({ message: '删除成功' });
  }
});
```

### 表单提交示例

```javascript
Page({
  data: {
    form: {
      username: '',
      password: '',
      phone: '',
      code: ''
    },
    errors: {}
  },

  // 表单验证
  validate() {
    const { username, password, phone, code } = this.data.form;
    const errors = {};

    if (!username) {
      errors.username = '请输入用户名';
    }

    if (!password || password.length < 6) {
      errors.password = '密码至少6位';
    }

    if (!/^1\d{10}$/.test(phone)) {
      errors.phone = '手机号格式不正确';
    }

    if (!code) {
      errors.code = '请输入验证码';
    }

    this.setData({ errors: Object.keys(errors).length ? errors : {} });
    return Object.keys(errors).length === 0;
  },

  // 提交表单
  async handleSubmit() {
    if (!this.validate()) return;

    wx.vant.showLoadingToast({ message: '提交中...' });

    try {
      await request('/api/submit', this.data.form);
      wx.vant.showSuccessToast('提交成功');
    } catch (e) {
      wx.vant.showFailToast('提交失败');
    }
  }
});
```

```html
<van-form bind:submit="handleSubmit">
  <van-cell-group>
    <van-field
      value="{{ form.username }}"
      label="用户名"
      placeholder="请输入用户名"
      error="{{ errors.username }}"
    />
    <van-field
      value="{{ form.password }}"
      type="password"
      label="密码"
      placeholder="请输入密码"
      error="{{ errors.password }}"
    />
    <van-field
      value="{{ form.phone }}"
      label="手机号"
      type="number"
      placeholder="请输入手机号"
      error="{{ errors.phone }}"
    />
    <van-field
      value="{{ form.code }}"
      center
      clearable
      label="验证码"
      placeholder="请输入验证码"
      use-button-slot
      error="{{ errors.code }}"
    >
      <van-button
        slot="button"
        size="small"
        type="primary"
        bind:click="sendCode"
      >
        发送验证码
      </van-button>
    </van-field>
  </van-cell-group>

  <view class="submit-btn">
    <van-button type="primary" size="large" round block submit>
      提交
    </van-button>
  </view>
</van-form>
```

## 主题定制

```json
// app.json
{
  "usingComponents": {
    "van-button": "path/vant-weapp/button/index",
    "van-field": "path/vant-weapp/field/index"
  },
  "theme": {
    "primary-color": "#07c160",
    "danger-color": "#ee0a24"
  }
}
```

## 常见问题

### Q1: 组件样式不生效？

检查 `app.wxss` 是否有全局样式覆盖，组件样式使用 `:host` 隔离。

### Q2: 如何自定义主题？

在 `app.wxss` 中覆盖 CSS 变量：

```css
page {
  --primary-color: #07c160;
  --button-primary-border-color: #059b4e;
}
```

---

**技术栈**: 微信小程序 | Vant Weapp | 表单验证

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
