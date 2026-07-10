from fastapi import APIRouter, Depends, HTTPException, Query, Cookie, Header
from sqlalchemy.orm import Session

from depends.depends import get_db
from core.service import user_service
from vo.user import UserCreateVo, UserResponse, RegisterVo, SetPasswordVo

# 创建用户模块的分路由
user_route = APIRouter(tags=["用户模块接口"])


# 1.从 Cookie / Header 获取参数
@user_route.get("/cookie-header", summary="从 Cookie / Header 获取参数")
def validate_cookie_header(
        session_id: str | None = Cookie(None, description="会话ID"),
        x_request_id: str | None = Header(None, description="请求追踪ID"),
        user_agent: str = Header(..., description="User-Agent"),
):
    """从 Cookie 和 Header 中提取参数，部分可选、部分必填"""
    return {
        "session_id": session_id,
        "x_request_id": x_request_id,
        "user_agent": user_agent,
    }


# 2. 分页获取用户：自定义返回值
@user_route.get("/userPage", response_model=list[UserResponse], summary="获取用户列表")
def list_users(
        page: int = Query(1, ge=1, description="页码"),
        size: int = Query(10, ge=1, le=100, description="每页条数"),
        db: Session = Depends(get_db),
):
    offset = (page - 1) * size
    return user_service.get_users_page(db, offset, size)


# 3.获取单个用户：自定义返回值
@user_route.get("/{user_id}", response_model=UserResponse, summary="获取单个用户")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"用户 {user_id} 不存在")
    return user


# 4.删除用户
@user_route.delete("/{user_id}", status_code=204, summary="删除用户")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if not user_service.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail=f"用户 {user_id} 不存在")


# 5.创建用户[POST]：基础Field校验
@user_route.post("/create_user", summary="创建用户", description="创建用户接口", response_model=UserResponse)
def create_user(user: UserCreateVo, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)


# 6.用户注册[POST]：自定义字段校验
@user_route.post("/register", summary="注册用户", description="field_validator：自定义字段校验")
def register_user(user: RegisterVo):
    """Pydantic field_validator：用户名中英文区分、年龄合理性"""
    return {"username": user.username, "age": user.age}


# 7.密码修改[POST]：自定义字段校验
@user_route.post("/set_password", summary="修改密码", description="model_validator：跨字段校验")
def set_password(body: SetPasswordVo):
    """Pydantic model_validator：确认密码一致性检验"""
    return {"msg": "密码验证通过"}
