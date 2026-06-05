# Prompt 01: 项目骨架 + 基本路由 + 数据模型

创建 FastAPI 项目：

app/main.py：
- FastAPI 实例 title="FastAPI Demo API"
- GET / 返回 {"message": "Hello FastAPI!", "docs": "/docs"}

数据模型（Pydantic v2）：
- UserBase(name: str min=3 max=50, email: str pattern=邮箱正则)
- UserCreate(继承 UserBase + password: str min=6)
- User(继承 UserBase + id: int, is_active: bool, created_at)
- ItemBase(name, description, price > 0)
- ItemCreate, Item(id, owner_id, created_at)
- Token(access_token, token_type)

requirements.txt：fastapi, uvicorn, pydantic, python-jose, passlib, python-multipart, pytest, httpx

---
## 背景
- 工具：Cursor Composer（多文件编辑）
- 阶段：第 1-2 轮
- 结果：AI 用了 Field(regex=...) 而非 Pydantic v2 的 Field(pattern=...)
