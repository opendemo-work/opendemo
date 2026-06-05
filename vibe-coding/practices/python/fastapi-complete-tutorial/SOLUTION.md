# 解决过程：FastAPI 完整实战

## 使用的工具：Cursor Composer（多文件编辑）

---

### 第 1 轮：项目骨架 + 基本路由

**Prompt：**
> 创建 FastAPI 项目：
> - app/main.py 作为主文件
> - requirements.txt 包含 fastapi, uvicorn, pydantic, python-jose, passlib, python-multipart, pytest, httpx
> - 基本路由：GET / 返回 {"message": "Hello FastAPI!", "docs": "/docs"}
> - FastAPI 实例配置 title="FastAPI Demo API"

**AI 生成：** 正确的项目结构和基本路由。

---

### 第 2 轮：数据模型 + 用户系统

**Prompt：**
> 添加以下 Pydantic 模型和用户系统：
> - UserBase(name: str min=3 max=50, email: str pattern=邮箱正则)
> - UserCreate(继承 UserBase + password: str min=6)
> - User(继承 UserBase + id: int, is_active: bool=True, created_at)
> - Token(access_token: str, token_type: str)
> - fake_users_db 字典，预置 admin 用户（密码 admin123，bcrypt 哈希）
> - POST /users/ 创建用户
> - GET /users/me 获取当前用户

**AI 生成：** 模型定义正确。

**问题：** AI 用了 `email: str = Field(..., regex=...)` — Pydantic v2 中应该用 `pattern=`。

**修复：** "这是 Pydantic v2，把 regex= 改成 pattern="。

---

### 第 3 轮：JWT 认证

**Prompt：**
> 添加 JWT 认证：
> - SECRET_KEY = "your-secret-key-here", ALGORITHM = "HS256"
> - OAuth2PasswordBearer(tokenUrl="token")
> - create_access_token 函数（30 分钟过期）
> - authenticate_user 验证用户名密码
> - get_current_user 依赖：解码 token 获取用户
> - POST /token 登录接口

**AI 生成：** 认证逻辑正确。

**问题：** `datetime.utcnow()` 在 Python 3.12 中已被弃用。

**修复：** 保持兼容性，暂不修改（教程级代码可接受）。

---

### 第 4 轮：物品 CRUD

**Prompt：**
> 添加物品的完整 CRUD：
> - ItemBase(name, description, price)
> - ItemCreate, Item(id, owner_id, created_at)
> - GET /items/ 分页（skip/limit），需要认证
> - POST /items/ 创建，需要认证
> - GET /items/{item_id} 获取单个
> - PUT /items/{item_id} 更新
> - DELETE /items/{item_id} 删除
> - fake_items_db 列表存储

**AI 生成：** CRUD 完整。

**问题：** `item.dict()` 在 Pydantic v2 中应使用 `item.model_dump()`。

**修复：** "改用 model_dump()"。

---

### 第 5 轮：验证

```bash
uvicorn app.main:app --reload
# 访问 http://localhost:8000/docs 查看 Swagger UI
# 测试完整流程：登录 → 创建物品 → 查询物品 → 删除
```

**结果：** 全部通过 ✅

---

## 总结

| 维度 | 值 |
|------|-----|
| 总轮次 | 5 轮 |
| 实际用时 | ~30 分钟 |
| AI 犯错次数 | 2（Pydantic v2 API 变化） |
| 人工干预 | regex→pattern, dict()→model_dump() |

### 关键技巧
- **Pydantic v2 有很多 API 变化** — AI 经常生成 v1 的代码，需要注意
- **Cursor Composer 适合多文件项目** — 一次 prompt 可以同时修改 main.py 和 requirements.txt
- **FastAPI 自动文档** — 写完直接访问 /docs 测试，比 curl 更直观

### 常见坑
- `Field(regex=...)` → v2 改为 `Field(pattern=...)`
- `model.dict()` → v2 改为 `model.model_dump()`
- `from_attributes=True` — v2 的 ORM 模式配置，替代 v1 的 `orm_mode`
- OAuth2PasswordRequestForm 需要 `python-multipart` 依赖 — 缺少会报 422
