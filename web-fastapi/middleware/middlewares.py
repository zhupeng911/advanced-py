"""FastAPI 中间件演示

自定义中间件请求耗时统计，自动写入 Response Header
"""

import time

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


class TimingMiddleware(BaseHTTPMiddleware):
    """记录每个请求处理耗时，注入 X-Process-Time 响应头"""

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - start
        response.headers["X-Process-Time"] = f"{elapsed:.4f}s"
        return response
