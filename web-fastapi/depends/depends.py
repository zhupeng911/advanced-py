"""FastAPI 依赖注入（Depends）演示

三种典型用法：
  1. 通用参数提取 — 分页参数复用，多个路由共享同一个参数定义
  2. 子依赖 — 依赖内部调用另一依赖，形成依赖链
  3. 认证模拟 — 从 Header 提取 token、注入当前用户
"""

from fastapi import Depends, Header, HTTPException, Query

from core.config.pg_config import SessionLocal


def get_db():
    """数据库会话依赖：路由用完自动关闭"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# 1. 通用参数提取：分页参数
#    多个路由都能直接 Depends(pagination_params) 拿到 (page, size)
#    避免在每个函数里重复写 Query(...) 参数
# ---------------------------------------------------------------------------


async def pagination_params(
        page: int = Query(1, ge=1, description="页码"),
        size: int = Query(10, ge=1, le=100, description="每页条数"),
) -> dict:
    """把 page / size 封装成一个公共依赖，一处定义、多处复用"""
    return {"page": page, "size": size, "offset": (page - 1) * size}


# ---------------------------------------------------------------------------
# 2. 子依赖：token 解析 → 认证校验
#    verify_token 被 get_current_user 调用，演示依赖嵌套
# ---------------------------------------------------------------------------


async def verify_token(authorization: str = Header(..., description="认证 Token")):
    """最底层依赖：从 Header 拿 token 并简单校验"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token 格式错误，应为 Bearer xxx")
    token = authorization[len("Bearer "):]
    # 模拟校验：有效 token 为 "123456"
    if token != "123456":
        raise HTTPException(status_code=401, detail="Token 无效或已过期")
    return token


async def get_current_user(token: str = Depends(verify_token)):
    """中间层依赖：调用 verify_token 拿到 token 后，查"数据库"得到用户信息"""
    # 模拟数据库查询
    return {"user_id": 1, "username": "admin", "role": "superuser"}
