from functools import wraps

from flask import request

from utils.response import error


def validate_json(*required_fields):
    """验证请求 JSON 必填字段"""

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return error("请求必须是 JSON 格式", 400)
            data = request.get_json()
            missing = [field for field in required_fields if field not in data or not data[field]]
            if missing:
                return error(f"缺少必填字段: {', '.join(missing)}", 400)
            return f(*args, **kwargs)

        return wrapper

    return decorator


# 装饰器："包裹"原函数，在原函数执行前后加点额外逻辑
def validate_pagination(f):  # f = 被装饰的函数
    """验证分页参数"""

    # 参数1: *args 接收任意多个位置参数，打包成元组
    # 参数2: **kwargs 接收任意多个关键字参数，打包成字典
    @wraps(f)
    def wrapper(*args, **kwargs):
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        if page < 1:
            return error("page 必须大于等于 1", 400)
        if page_size < 1 or page_size > 100:
            return error("page_size 必须在 1-100 之间", 400)
        kwargs['page'] = page
        kwargs['page_size'] = page_size
        return f(*args, **kwargs)   # 等价 get_users(page=3, page_size=20)

    return wrapper
