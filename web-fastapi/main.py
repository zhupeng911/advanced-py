"""
FastAPI 简单案例：用户管理 API

运行方式：
    pip install fastapi uvicorn
    python main.py
    访问 http://127.0.0.1:8000/docs 查看 Swagger 文档
"""

from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="用户管理 API", version="1.0.0")

# ============================================================
# 1. 数据模型
# ============================================================

class UserCreate(BaseModel):
    """创建用户的请求体"""
    name: str = Field(..., min_length=1, max_length=50, description="用户名")
    age: int = Field(..., ge=0, le=150, description="年龄")
    email: Optional[str] = Field(None, pattern=r"^\S+@\S+\.\S+$", description="邮箱")

class UserUpdate(BaseModel):
    """更新用户的请求体（所有字段可选）"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    age: Optional[int] = Field(None, ge=0, le=150)
    email: Optional[str] = Field(None, pattern=r"^\S+@\S+\.\S+$")

class UserResponse(BaseModel):
    """用户响应体"""
    id: int
    name: str
    age: int
    email: Optional[str] = None

# ============================================================
# 2. 模拟数据库
# ============================================================

fake_db: dict[int, dict] = {}
_id_counter: int = 0

# ============================================================
# 3. API 端点
# ============================================================

@app.get("/", summary="根路径")
def root():
    return {"message": "欢迎使用用户管理 API", "docs": "/docs"}


@app.post("/users", response_model=UserResponse, status_code=201, summary="创建用户")
def create_user(user: UserCreate):
    global _id_counter
    _id_counter += 1
    record = {"id": _id_counter, **user.model_dump()}
    fake_db[_id_counter] = record
    return record


@app.get("/users", response_model=list[UserResponse], summary="获取用户列表")
def list_users(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页条数"),
):
    all_users = list(fake_db.values())
    start = (page - 1) * size
    return all_users[start : start + size]


@app.get("/users/{user_id}", response_model=UserResponse, summary="获取单个用户")
def get_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail=f"用户 {user_id} 不存在")
    return fake_db[user_id]


@app.put("/users/{user_id}", response_model=UserResponse, summary="更新用户")
def update_user(user_id: int, user: UserUpdate):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail=f"用户 {user_id} 不存在")
    # 只更新传入的字段
    update_data = user.model_dump(exclude_unset=True)
    fake_db[user_id].update(update_data)
    return fake_db[user_id]


@app.delete("/users/{user_id}", status_code=204, summary="删除用户")
def delete_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail=f"用户 {user_id} 不存在")
    del fake_db[user_id]


# ============================================================
# 4. 启动
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
