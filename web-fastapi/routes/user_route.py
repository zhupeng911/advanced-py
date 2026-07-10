from fastapi import APIRouter, Query, HTTPException, Cookie, Header

from vo.user import UserCreateVo, UserResponse, RegisterVo, SetPasswordVo

# 创建用户模块的分路由
user_route = APIRouter(tags=["用户模块接口"])

# 模拟数据库
fake_db: dict[int, dict] = {}
_id_counter: int = 0


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
        size: int = Query(10, ge=1, le=100, description="每页条数"), ):
    all_users = list(fake_db.values())
    start = (page - 1) * size
    return all_users[start: start + size]


# 3.获取单个用户：自定义返回值
@user_route.get("/{user_id}", response_model=UserResponse, summary="获取单个用户")
def get_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail=f"用户 {user_id} 不存在")
    return fake_db[user_id]


# 4.删除用户
@user_route.delete("/{user_id}", status_code=204, summary="删除用户")
def delete_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail=f"用户 {user_id} 不存在")
    del fake_db[user_id]


# 5.创建用户[POST]：基础Field校验
@user_route.post("/create_user", summary="创建用户", description="创建用户接口", response_model=UserResponse)
def create_user(user: UserCreateVo):
    global _id_counter
    _id_counter += 1
    record = {"id": _id_counter, **user.model_dump()}
    fake_db[_id_counter] = record
    return record


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
