"""依赖注入演示路由

展示 Depends 的三种用法：
  - 分页参数复用
  - 认证校验
  - 两者组合使用
"""

from fastapi import APIRouter, Depends

from depends.depends import get_current_user, pagination_params

depends_route = APIRouter(tags=["依赖注入演示"])


# 1. 使用分页依赖（无需重复写 page/size 的 Query）
@depends_route.get("/list", summary="分页查询演示")
async def demo_pagination(pager: dict = Depends(pagination_params)):
    """page / size 从依赖注入，路由函数不再需要声明这两个参数"""
    return {"msg": "分页参数", "pager": pager}


# 2. 使用认证依赖（需要有效 token 才能访问）
@depends_route.get("/me", summary="认证校验演示")
async def demo_auth(current_user: dict = Depends(get_current_user)):
    """依赖链：Bearer 123456 → verify_token → get_current_user → current_user"""
    return {"msg": "当前登录用户", "user": current_user}


# 3. 组合依赖（分页 + 认证同时使用）
@depends_route.get("/secure-list", summary="分页 + 认证组合")
async def demo_combined(
        pager: dict = Depends(pagination_params),
        current_user: dict = Depends(get_current_user),
):
    """两个依赖同时注入，实现受保护的分页查询"""
    return {
        "msg": "受保护的分页查询",
        "user": current_user["username"],
        "pager": pager,
        "data": [{"id": 1, "name": "item-1"}, {"id": 2, "name": "item-2"}],
    }
