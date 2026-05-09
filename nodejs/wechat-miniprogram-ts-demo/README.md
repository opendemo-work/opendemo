# 微信小程序 TypeScript 开发演示

## 学习目标

1. 掌握 TypeScript 配置
2. 理解类型定义和使用
3. 学会泛型和接口
4. 实现模块化和类型安全

## 环境要求

- 微信开发者工具 (支持 TypeScript)
- Node.js 16+

## 配置 TypeScript

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "strict": true,
    "moduleResolution": "node",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "noEmit": true,
    "lib": ["ES2020", "DOM"]
  },
  "include": ["**/*.ts"],
  "exclude": ["node_modules"]
}
```

## 类型基础

### 基础类型

```typescript
// 基础类型
const name: string = '张三';
const age: number = 28;
const active: boolean = true;
const nums: number[] = [1, 2, 3];
const tuple: [string, number] = ['name', 123];
```

### 接口定义

```typescript
// 定义用户接口
interface User {
  id: string;
  nickName: string;
  avatarUrl?: string;  // 可选属性
  readonly createdAt: Date;  // 只读属性
}

// 接口实现
class UserClass implements User {
  id: string;
  nickName: string;
  avatarUrl?: string;
  readonly createdAt: Date;

  constructor(data: Partial<User>) {
    this.id = data.id || generateId();
    this.nickName = data.nickName || '';
    this.avatarUrl = data.avatarUrl;
    this.createdAt = new Date();
  }
}
```

### 类型别名

```typescript
// 基本类型别名
type ID = string | number;

// 联合类型
type Status = 'pending' | 'processing' | 'success' | 'failed';

// 函数类型
type RequestCallback = (success: boolean, data?: any) => void;

// 泛型类型
type Result<T> = {
  code: number;
  message: string;
  data: T | null;
};
```

### 泛型

```typescript
// 泛型函数
function parseJSON<T>(json: string): T | null {
  try {
    return JSON.parse(json) as T;
  } catch {
    return null;
  }
}

// 泛型接口
interface APIResponse<T> {
  code: number;
  data: T;
  message: string;
}

// 泛型约束
interface HasId {
  id: string;
}

function findById<T extends HasId>(items: T[], id: string): T | undefined {
  return items.find(item => item.id === id);
}
```

## 实际应用

### API 请求封装

```typescript
// types/api.ts

interface RequestOptions<T = any> {
  url: string;
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  data?: T;
  header?: Record<string, string>;
}

interface ResponseData<T = any> {
  code: number;
  data: T;
  message: string;
}

type RequestPromise<T = any> = Promise<ResponseData<T>>;

// 请求封装
function request<T = any>(options: RequestOptions): RequestPromise<T> {
  return new Promise((resolve, reject) => {
    const app = getApp<App>();

    wx.showLoading({ title: '加载中...' });

    wx.request({
      url: app.globalData.apiBase + options.url,
      method: options.method || 'GET',
      data: options.data,
      header: {
        'Content-Type': 'application/json',
        'Authorization': wx.getStorageSync('token') || '',
        ...options.header
      },
      success: (res) => {
        const { statusCode, data } = res;
        if (statusCode === 200) {
          resolve(data as ResponseData<T>);
        } else {
          reject(new Error(`请求失败: ${statusCode}`));
        }
      },
      fail: reject,
      complete: () => wx.hideLoading()
    });
  });
}

// 导出类型和函数
export { request, RequestOptions, ResponseData };
export type { APIResponse };
```

### 页面定义

```typescript
// pages/user/user.ts

import { request, ResponseData } from '../../types/api';

// 数据模型
interface UserInfo {
  id: string;
  nickName: string;
  avatarUrl: string;
  phone: string;
  createdAt: Date;
}

// Page 实例类型
interface IPageData {
  userInfo: UserInfo | null;
  loading: boolean;
}

interface IPageMethod {
  fetchUserInfo(): Promise<void>;
  updateUserInfo(data: Partial<UserInfo>): Promise<void>;
}

// 页面逻辑
Page<IData, IMethod>({
  data: <IPageData>{
    userInfo: null,
    loading: false
  },

  onLoad() {
    this.fetchUserInfo();
  },

  async fetchUserInfo() {
    this.setData({ loading: true });

    try {
      const res = await request<UserInfo>({
        url: '/api/user/info'
      });

      if (res.code === 0 && res.data) {
        this.setData({ userInfo: res.data });
      }
    } catch (e) {
      console.error('获取用户信息失败', e);
    } finally {
      this.setData({ loading: false });
    }
  },

  async updateUserInfo(data: Partial<UserInfo>) {
    const res = await request<UserInfo>({
      url: '/api/user/update',
      method: 'POST',
      data
    });

    if (res.code === 0) {
      wx.showToast({ title: '更新成功' });
      this.fetchUserInfo();
    }
  }
});
```

### 云函数定义

```typescript
// cloudfunctions/user/index.ts

const cloud = require('wx-server-sdk');

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });

const db = cloud.database();

interface User {
  openid: string;
  nickName: string;
  avatarUrl: string;
  createdAt: Date;
}

exports.main = async (event: { action: string; data?: any }, context: any) => {
  const { action, data } = event;

  switch (action) {
    case 'getUser':
      return await getUser(data.openid);

    case 'updateUser':
      return await updateUser(data.openid, data.updates);

    case 'createUser':
      return await createUser(data.userInfo);

    default:
      return { success: false, error: 'Unknown action' };
  }
};

async function getUser(openid: string) {
  const { data } = await db.collection('users').where({ openid }).get();
  return { success: true, data: data[0] };
}

async function updateUser(openid: string, updates: Partial<User>) {
  const result = await db.collection('users')
    .where({ openid })
    .update({ data: { ...updates, updatedAt: db.serverDate() } });

  return { success: true, updated: result.updated };
}

async function createUser(userInfo: Omit<User, 'createdAt'>) {
  const result = await db.collection('users')
    .add({ data: { ...userInfo, createdAt: db.serverDate() } });

  return { success: true, id: result._id };
}
```

## 常见问题

### Q1: 如何处理 nullable 类型？

```typescript
// 使用可选链和空值合并
const name = user?.nickName ?? '匿名';

// 类型守卫
function isUser(obj: any): obj is User {
  return obj && typeof obj.id === 'string';
}

// 类型断言
const user = maybeUser as User;
```

### Q2: 如何定义微信小程序特有的类型？

创建 `src/types/wx.d.ts`:

```typescript
declare module 'wx' {
  interface Wx {
    login(options: LoginOptions): void;
    getUserProfile(options: GetUserProfileOptions): void;
    request(options: RequestOptions): void;
    // ... 更多定义
  }
}

const wx: Wx;
export default wx;
```

---

**技术栈**: 微信小程序 | TypeScript | 类型安全

**版本**: 1.0.0