"""自定义各类业务异常"""


class BizException(Exception):
    """通用业务异常，可指定状态码和错误码"""

    def __init__(self, message: str, code: int = 400, error_code: int = 1):
        self.message = message
        self.code = code
        self.error_code = error_code


class NotFoundException(BizException):
    """资源不存在异常"""

    def __init__(self, message: str = "资源不存在"):
        super().__init__(message, code=404, error_code=404)


class ForbiddenException(BizException):
    """权限异常"""

    def __init__(self, message: str = "暂无权限"):
        super().__init__(message, code=403, error_code=404)
