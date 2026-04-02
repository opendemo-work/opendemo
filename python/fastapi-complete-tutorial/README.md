# FastAPI Complete Tutorial

FastAPI完整实战教程，包含RESTful API、认证授权、数据库操作等核心功能。

## 什么是FastAPI

FastAPI是一个现代、高性能的Python Web框架，特点：
- **高性能**：基于Starlette和Pydantic，性能接近Node.js和Go
- **快速开发**：自动API文档，类型提示自动验证
- **现代标准**：基于Python 3.8+类型提示、OpenAPI、JSON Schema

## 与Flask/Django对比

| 特性 | FastAPI | Flask | Django |
|------|---------|-------|--------|
| 性能 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 开发效率 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 学习曲线 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| 自动文档 | ✅ | ❌ | ❌ |
| 类型验证 | ✅ 原生 | ❌ | ❌ |
| 异步支持 | ✅ 原生 | ⚠️ 扩展 | ⚠️ 3.1+ |

## 技术栈

- Python 3.8+
- FastAPI 0.104+
- Pydantic v2
- SQLAlchemy 2.0
- JWT认证

## 项目结构

```
fastapi-complete-tutorial/
├── app/
│   ├── __init__.py
│   └── main.py              # 主应用
├── tests/
│   └── test_main.py         # 测试
├── alembic/                 # 数据库迁移
├── requirements.txt         # 依赖
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
# 开发模式
uvicorn app.main:app --reload

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. 访问API文档

```
自动生成的API文档:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json
```

## 核心功能演示

### 1. 基本路由

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

### 2. 请求/响应模型

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### 3. 依赖注入

```python
from fastapi import Depends

async def common_parameters(q: str = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
```

### 4. 认证授权

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

## 测试API

### 1. 获取Token

```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### 2. 创建用户

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "secret123"
  }'
```

### 3. 创建物品（需认证）

```bash
curl -X POST "http://localhost:8000/items/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone",
    "price": 999.99,
    "description": "Apple iPhone"
  }'
```

### 4. 获取物品列表

```bash
curl "http://localhost:8000/items/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 运行测试

```bash
# 运行所有测试
pytest

# 运行并显示详细输出
pytest -v

# 覆盖率报告
pytest --cov=app --cov-report=html
```

## 核心特性详解

### 自动数据验证

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    # 自动验证邮箱格式
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    # 自动验证年龄范围
    age: int = Field(..., ge=0, le=150)
    # 自动验证字符串长度
    name: str = Field(..., min_length=2, max_length=50)
```

### 异步支持

```python
# FastAPI原生支持async/await
@app.get("/async-endpoint")
async def async_endpoint():
    # 可以await异步操作
    data = await fetch_data_from_database()
    return data
```

### 后台任务

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # 发送邮件逻辑
    pass

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email, "Hello!")
    return {"message": "Notification sent in the background"}
```

## 生产部署

### 使用Gunicorn

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 学习要点

1. Python类型提示在FastAPI中的应用
2. Pydantic模型验证原理
3. 依赖注入系统的设计
4. 异步编程与协程
5. JWT认证流程
6. API版本控制策略

## 参考

- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [Pydantic文档](https://docs.pydantic.dev/)
- [Starlette文档](https://www.starlette.io/)
