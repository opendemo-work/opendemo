"""
FastAPI 完整示例应用

包含:
- RESTful API
- 请求/响应模型
- 依赖注入
- 认证授权
- 数据库操作
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# FastAPI应用实例
app = FastAPI(
    title="FastAPI Demo API",
    description="FastAPI完整演示项目",
    version="1.0.0"
)

# 安全相关
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 数据模型
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class User(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        from_attributes = True

class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    
class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# 模拟数据库
fake_users_db = {
    "admin": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": pwd_context.hash("admin123"),
        "is_active": True
    }
}

fake_items_db = []
item_id_counter = 1

# 辅助函数
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str):
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return User(**{k: v for k, v in user_dict.items() if k != "hashed_password"})
    return None

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

# API路由
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """用户登录获取访问令牌"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/", tags=["根"])
async def root():
    """根路径"""
    return {"message": "Hello FastAPI!", "docs": "/docs"}

@app.get("/users/me", response_model=User, tags=["用户"])
async def read_users_me(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user

@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED, tags=["用户"])
async def create_user(user: UserCreate):
    """创建新用户"""
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    new_user = {
        "id": len(fake_users_db) + 1,
        "username": user.username,
        "email": user.email,
        "hashed_password": get_password_hash(user.password),
        "is_active": True
    }
    fake_users_db[user.username] = new_user
    
    return User(**{k: v for k, v in new_user.items() if k != "hashed_password"})

@app.get("/items/", response_model=List[Item], tags=["物品"])
async def read_items(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user)
):
    """获取物品列表"""
    return fake_items_db[skip : skip + limit]

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["物品"])
async def create_item(
    item: ItemCreate,
    current_user: User = Depends(get_current_user)
):
    """创建新物品"""
    global item_id_counter
    new_item = {
        "id": item_id_counter,
        **item.dict(),
        "owner_id": current_user.id,
        "created_at": datetime.now()
    }
    fake_items_db.append(new_item)
    item_id_counter += 1
    return Item(**new_item)

@app.get("/items/{item_id}", response_model=Item, tags=["物品"])
async def read_item(
    item_id: int,
    current_user: User = Depends(get_current_user)
):
    """获取单个物品"""
    for item in fake_items_db:
        if item["id"] == item_id:
            return Item(**item)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found"
    )

@app.put("/items/{item_id}", response_model=Item, tags=["物品"])
async def update_item(
    item_id: int,
    item_update: ItemCreate,
    current_user: User = Depends(get_current_user)
):
    """更新物品"""
    for i, item in enumerate(fake_items_db):
        if item["id"] == item_id:
            fake_items_db[i].update(item_update.dict())
            return Item(**fake_items_db[i])
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found"
    )

@app.delete("/items/{item_id}", tags=["物品"])
async def delete_item(
    item_id: int,
    current_user: User = Depends(get_current_user)
):
    """删除物品"""
    for i, item in enumerate(fake_items_db):
        if item["id"] == item_id:
            deleted = fake_items_db.pop(i)
            return {"message": "Item deleted", "item": deleted}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
