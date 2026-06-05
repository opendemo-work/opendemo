# 挑战：FastAPI 完整实战

## 难度：intermediate | 预计用时：45 分钟 | 推荐工具：Cursor Composer / Claude Code

## 目标

用 FastAPI 构建一个完整的 REST API 应用，包含：

1. **用户认证** — OAuth2 + JWT token 登录
2. **用户 CRUD** — 创建用户、获取当前用户信息
3. **物品 CRUD** — 创建、查询、更新、删除物品（需要认证）
4. **数据验证** — Pydantic 模型自动验证请求参数
5. **自动文档** — Swagger UI + ReDoc

## 约束

- Python 3.8+，FastAPI 0.104+，Pydantic v2
- 使用 `fake_users_db` 字典模拟数据库（不需要真实数据库）
- JWT 密钥硬编码 `"your-secret-key-here"`
- 密码用 bcrypt 哈希存储
- 所有 API 响应使用 Pydantic 模型
- 预置 admin 用户（密码 `admin123`）

## API 规格

| 方法 | 路径 | 认证 | 功能 |
|------|------|------|------|
| POST | `/token` | 否 | 登录获取 JWT |
| GET | `/` | 否 | 欢迎消息 |
| GET | `/users/me` | 是 | 当前用户信息 |
| POST | `/users/` | 否 | 创建新用户 |
| GET | `/items/` | 是 | 物品列表（分页 skip/limit） |
| POST | `/items/` | 是 | 创建物品 |
| GET | `/items/{id}` | 是 | 获取单个物品 |
| PUT | `/items/{id}` | 是 | 更新物品 |
| DELETE | `/items/{id}` | 是 | 删除物品 |

## 验证

```bash
# 启动
uvicorn app.main:app --reload

# 1. 登录
curl -X POST "http://localhost:8000/token" \
  -d "username=admin&password=admin123"
# 返回 {"access_token": "eyJ...", "token_type": "bearer"}

# 2. 创建物品
curl -X POST "http://localhost:8000/items/" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "iPhone", "price": 999.99, "description": "Apple iPhone"}'
# 返回 201

# 3. 获取物品列表
curl "http://localhost:8000/items/?skip=0&limit=10" \
  -H "Authorization: Bearer <TOKEN>"

# 4. 自动文档
# 浏览器打开 http://localhost:8000/docs
```

## 提示（卡住时再看）

<details>
<summary>提示 1：推荐分步实现</summary>

第一步：只实现基本路由（GET /、数据模型定义）
第二步：添加用户认证（OAuth2PasswordBearer + JWT）
第三步：添加物品 CRUD
第四步：添加 Pydantic 验证和错误处理

</details>

<details>
<summary>提示 2：关键依赖</summary>

requirements.txt: fastapi, uvicorn, pydantic, python-jose[cryptography], passlib[bcrypt], python-multipart

</details>

<details>
<summary>提示 3：关键 Prompt</summary>

"用 FastAPI 创建一个 REST API，包含 JWT 认证和用户/物品 CRUD。用户用 fake_users_db 字典存储，密码用 bcrypt 哈希。物品需要认证才能操作。Pydantic 模型做请求验证。预置 admin 用户。"

</details>

## 对应原 Demo

完成后对比参考实现：`python/fastapi-complete-tutorial/`
