# Prompt 02: JWT 认证 + CRUD + 验证

添加 JWT 认证系统：
- SECRET_KEY = "your-secret-key-here", ALGORITHM = "HS256"
- OAuth2PasswordBearer(tokenUrl="token")
- create_access_token（30 分钟过期）
- authenticate_user 验证用户名密码
- get_current_user 依赖：解码 token
- POST /token 登录接口

添加物品完整 CRUD（全部需要认证）：
- GET /items/ 分页、POST /items/、GET /items/{id}、PUT /items/{id}、DELETE /items/{id}
- fake_users_db 和 fake_items_db 字典/列表存储
- 预置 admin 用户（密码 admin123，bcrypt 哈希）

验证：uvicorn app.main:app --reload，访问 /docs 测试完整流程。

---
## 背景
- 工具：Cursor Composer
- 阶段：第 3-5 轮
- 结果：model.dict() 需改为 Pydantic v2 的 model_dump()
