"""全局异常处理器"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from exception.exceptions import BizException


def register_exception_handlers(app: FastAPI):
    """将异常处理器注册到 app 实例"""

    @app.exception_handler(BizException)
    async def biz_exception_handler(request, exc: BizException):
        """1. 业务异常 → 统一 JSON 响应"""
        return JSONResponse(
            status_code=exc.code,
            content={"code": exc.error_code, "message": exc.message, "data": None},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc: RequestValidationError):
        """2. 参数校验失败 → 中文友好提示"""
        errors = []
        for err in exc.errors():
            field = " → ".join(str(loc) for loc in err["loc"])
            errors.append(f"字段 [{field}] {err['msg']}")
        return JSONResponse(
            status_code=422,
            content={"code": 422, "message": "参数校验失败: " + "; ".join(errors), "data": None},
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc: Exception):
        """3. 兜底未知异常 → 隐藏内部细节"""
        return JSONResponse(
            status_code=500,
            content={"code": 500, "message": "服务器内部错误，请稍后再试", "data": None},
        )
