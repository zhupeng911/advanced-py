from fastapi import APIRouter, Query, HTTPException

from vo.user import UserCreateVo, UserResponse

# 创建用户模块的分路由
user = APIRouter(tags=["用户模块接口"])

# 模拟数据库
fake_db: dict[int, dict] = {}
_id_counter: int = 0


# 1. 创建用户
@user.post("/create_user", summary="创建用户", description="创建用户接口", response_model=UserResponse)
def create_user(user: UserCreateVo):
    global _id_counter
    _id_counter += 1
    record = {"id": _id_counter, **user.model_dump()}
    fake_db[_id_counter] = record
    return record


# 2. 分页获取用户
@user.get("/userPage", response_model=list[UserResponse], summary="获取用户列表")
def list_users(
        page: int = Query(1, ge=1, description="页码"),
        size: int = Query(10, ge=1, le=100, description="每页条数"), ):
    all_users = list(fake_db.values())
    start = (page - 1) * size
    return all_users[start: start + size]


# 3.获取单个用户
@user.get("/{user_id}", response_model=UserResponse, summary="获取单个用户")
def get_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail=f"用户 {user_id} 不存在")
    return fake_db[user_id]


# 4.删除用户
@user.delete("/{user_id}", status_code=204, summary="删除用户")
def delete_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail=f"用户 {user_id} 不存在")
    del fake_db[user_id]
