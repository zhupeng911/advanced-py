from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator


# 数据模型：创建用户Vo
class UserCreateVo(BaseModel):
    """创建用户请求体"""
    name: str = Field(..., min_length=1, max_length=50, description="用户名")
    age: int = Field(..., ge=0, le=150, description="年龄")
    email: Optional[str] = Field(None, pattern=r"^\S+@\S+\.\S+$", description="邮箱")  # 非必填


# 数据模型：用户响应Vo
class UserResponse(BaseModel):
    """用户响应体"""
    id: int
    name: str
    age: int
    email: Optional[str] = None


# 数据模型：注册Vo
class RegisterVo(BaseModel):
    """注册请求体：演示 field_validator"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., min_length=6, max_length=20, description="密码")
    age: int = Field(..., description="年龄")

    @field_validator("username")
    @classmethod
    def username_must_valid(cls, v: str) -> str:
        # 中文名至少2字，英文名至少3字母
        if v.isascii():
            if len(v) < 3:
                raise ValueError("英文用户名至少需要 3 个字符")
        else:
            if len(v) < 2:
                raise ValueError("中文用户名至少需要 2 个字符")
        return v.strip()

    @field_validator("age")
    @classmethod
    def age_must_reasonable(cls, v: int) -> int:
        if v < 0 or v > 150:
            raise ValueError("年龄必须在 0-150 之间")
        return v


# 数据模型：修改密码Vo
class SetPasswordVo(BaseModel):
    """修改密码请求体：演示 model_validator 跨字段校验"""
    password: str = Field(..., min_length=6, max_length=20)
    confirm_password: str = Field(..., min_length=6, max_length=20)

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("两次密码不一致")
        return self
