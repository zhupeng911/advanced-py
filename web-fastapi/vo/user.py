from typing import Optional

from pydantic import BaseModel, Field


# 数据模型：创建用户Vo
class UserCreateVo(BaseModel):
    """创建用户请求体"""
    name: str = Field(..., min_length=1, max_length=50, description="用户名")
    age: int = Field(..., ge=0, le=150, description="年龄")
    email: Optional[str] = Field(None, pattern=r"^\S+@\S+\.\S+$", description="邮箱") # 非必填

# 数据模型：用户响应Vo
class UserResponse(BaseModel):
    """用户响应体"""
    id: int
    name: str
    age: int
    email: Optional[str] = None