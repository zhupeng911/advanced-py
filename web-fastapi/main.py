from fastapi import FastAPI

from exception.exception_handlers import register_exception_handlers
from routes.exception_route import exception_route
from routes.shop_route import shop
from routes.user_route import user

"""
FastAPI 简单案例

运行方式：
    pip install fastapi uvicorn
    python main.py
    访问 http://127.0.0.1:8000/docs 查看 Swagger 文档
"""

# 创建FastAPI应用实例
app = FastAPI()

# 路由注册
app.include_router(shop, prefix="/shop", tags=["购物车模块接口"])
app.include_router(user, prefix="/user", tags=["用户模块接口"])
app.include_router(exception_route, prefix="/exception", tags=["异常抛出演示"])

# 注册全局异常处理器
register_exception_handlers(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
