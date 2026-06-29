import json
from flask import make_response


def success(data=None, message="操作成功", code=200):
    """统一成功响应"""
    response_data = {
        "code": code,
        "message": message,
        "data": data
    }
    response = make_response(json.dumps(response_data, ensure_ascii=False), code)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


def error(message="操作失败", code=400, errors=None):
    """统一错误响应"""
    response_data = {
        "code": code,
        "message": message,
    }
    if errors:
        response_data["errors"] = errors
    response = make_response(json.dumps(response_data, ensure_ascii=False), code)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response
