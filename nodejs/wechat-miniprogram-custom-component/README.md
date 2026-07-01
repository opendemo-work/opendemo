<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 微信小程序自定义组件演示

## 学习目标

1. 掌握 Component 构造器用法
2. 理解插槽 (slot) 机制
3. 学会组件间通信 (behaviors, relations)
4. 实现组件复用和发布

## 环境要求

- 微信开发者工具
- 基础组件知识

## 组件架构

```
Component
├── properties    # 属性 (输入)
├── data          # 内部数据
├── methods       # 方法
├── observers     # 监听器
├── lifetimes     # 生命周期
└── behaviors     # Behavior 复用
```

## 快速开始

### 1. 创建组件

```
components/
└── my-button/
    ├── index.js
    ├── index.json
    ├── index.wxml
    └── index.wxss
```

### 2. 组件定义

```javascript
// components/my-button/index.js
Component({
  // 组件属性
  properties: {
    text: {
      type: String,
      value: '按钮'
    },
    type: {
      type: String,
      value: 'primary'  // primary, warn, ghost
    },
    disabled: {
      type: Boolean,
      value: false
    },
    loading: {
      type: Boolean,
      value: false
    }
  },

  // 内部数据
  data: {
    isPressed: false
  },

  // 组件方法
  methods: {
    handleTap() {
      if (this.properties.disabled || this.properties.loading) return;

      this.triggerEvent('click', { time: Date.now() });
    },

    handleTouchStart() {
      this.setData({ isPressed: true });
    },

    handleTouchEnd() {
      this.setData({ isPressed: false });
    }
  }
});
```

### 3. 组件模板

```html
<!-- components/my-button/index.wxml -->
<button
  class="btn btn-{{type}} {{isPressed ? 'pressed' : ''}}"
  disabled="{{disabled}}"
  loading="{{loading}}"
  bindtap="handleTap"
  bindtouchstart="handleTouchStart"
  bindtouchend="handleTouchEnd"
>
  <slot></slot>
  <text>{{text}}</text>
</button>
```

### 4. 组件样式

```css
/* components/my-button/index.wxss */
.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24rpx 48rpx;
  border-radius: 8rpx;
  font-size: 28rpx;
  transition: all 0.2s;
}

.btn-primary {
  background: #07c160;
  color: white;
}

.btn-warn {
  background: #fa5151;
  color: white;
}

.btn-ghost {
  background: transparent;
  color: #07c160;
  border: 2rpx solid #07c160;
}

.btn.pressed {
  opacity: 0.8;
  transform: scale(0.98);
}

.btn[disabled] {
  opacity: 0.5;
}
```

### 5. 使用组件

```json
{
  "usingComponents": {
    "my-button": "/components/my-button/index"
  }
}
```

```html
<my-button
  text="提交"
  type="primary"
  bindclick="handleSubmit"
/>
```

## 插槽 (Slot)

### 默认插槽

```html
<!-- 组件定义 -->
<view class="card">
  <slot></slot>
</view>

<!-- 使用 -->
<my-card>
  <text>卡片内容</text>
</my-card>
```

### 命名插槽

```html
<!-- 组件定义 -->
<view class="layout">
  <slot name="header"></slot>
  <view class="content">
    <slot name="body"></slot>
  </view>
  <slot name="footer"></slot>
</view>

<!-- 使用 -->
<my-layout>
  <view slot="header">标题</view>
  <view slot="body">内容</view>
  <view slot="footer">底部</view>
</my-layout>
```

## 组件通信

### 1. 属性传递 (父→子)

```javascript
// 父组件
<my-child value="{{parentValue}}" />

// 子组件接收
properties: {
  value: String
}
```

### 2. 事件触发 (子→父)

```javascript
// 子组件
this.triggerEvent('myevent', { data: 'some data' });

// 父组件
<my-child bindmyevent="onChildEvent" />

// 父组件处理
onChildEvent(e) {
  console.log('子组件数据:', e.detail.data);
}
```

### 3. 获取组件实例

```javascript
// 获取组件实例
const child = this.selectComponent('#myChild');
child.getData();

// 触发方法
child.someMethod();
```

## Behavior 复用

```javascript
// behaviors/form-item.js
module.exports = Behavior({
  properties: {
    label: String,
    value: String,
    error: String
  },

  data: {
    focused: false
  },

  methods: {
    onFocus() {
      this.setData({ focused: true });
    },

    onBlur() {
      this.setData({ focused: false });
    }
  }
});
```

```javascript
// 组件使用 Behavior
Component({
  behaviors: [require('../behaviors/form-item.js')],

  // 组件属性和方法会合并
});
```

## 组件生命周期

```javascript
Component({
  // 组件所在页面的生命周期
  pageLifetimes: {
    show() {},    // 页面显示
    hide() {},    // 页面隐藏
    resize() {}   // 页面尺寸变化
  },

  // 组件生命周期
  lifetimes: {
    created() {},     // 创建
    attached() {},    // 挂载
    ready() {},       // 渲染完成
    detached() {},    // 卸载
    error() {}        // 错误
  }
});
```

## 常见问题

### Q1: 如何让组件样式隔离？

在 `component.wxss` 中使用 `:host` 选择器：

```css
:host {
  display: block;
}
```

### Q2: 如何实现虚拟列表？

使用 `scroll-view` 和动态渲染：

```html
<scroll-view scroll-y bindscrolltolower="loadMore">
  <block wx:for="{{visibleList}}" wx:key="id">
    <list-item item="{{item}}" />
  </block>
</scroll-view>
```

---

**技术栈**: 微信小程序 | Component | Behavior | WXML | WXSS

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
