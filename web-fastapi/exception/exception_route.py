"""异常抛出示例路由"""

from fastapi import APIRouter

from exception.exceptions import BizException, NotFoundException, ForbiddenException

exception_route = APIRouter(tags=["异常抛出演示"])


# 1. 业务异常
@exception_route.get("/biz", summary="通用业务异常")
def trigger_biz():
    raise BizException("用户余额不足，无法下单", code=400, error_code=1001)


# 2. 资源不存在
@exception_route.get("/not-found", summary="资源不存在异常")
def trigger_not_found():
    raise NotFoundException(f"订单 {999} 不存在")


# 3. 权限异常
@exception_route.get("/forbidden", summary="权限不足异常")
def trigger_forbidden():
    raise ForbiddenException("仅管理员可执行此操作")


# 4. 未捕获异常（兜底）
@exception_route.get("/unhandled", summary="未捕获异常（兜底 500）")
def trigger_unhandled():
    1 / 0
