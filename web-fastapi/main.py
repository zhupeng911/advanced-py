from fastapi import FastAPI

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

# 路由分发：将购物车模块的分路由加载到主应用中
app.include_router(shop, prefix="/shop", tags=["购物车模块接口"])
app.include_router(user, prefix="/user", tags=["用户模块接口"])

if __name__ == "__main__":
    # 启动方式1:
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
