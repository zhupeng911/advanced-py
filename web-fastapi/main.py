from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 导入所有 model，确保 Base.metadata 能发现所有表
import core.po.user  # noqa
from core.config.pg_config import create_database, db_engine, Base
from depends.depends_route import depends_route
from exception.exception_handlers import register_exception_handlers
from exception.exception_route import exception_route
from middleware.middlewares import TimingMiddleware
from core.routes.shop_route import shop_route
from core.routes.user_route import user_route

"""
FastAPI 案例集合

覆盖内容：
  - 路由注册、路径/查询/Cookie/Header 参数
  - Pydantic 校验（field_validator / model_validator）
  - 自定义异常 + 全局异常处理器
  - 依赖注入（Depends）：分页复用、认证链、子依赖
  - 中间件：CORS 跨域、请求耗时统计

运行方式：
    pip install fastapi uvicorn
    python main.py
    访问 http://127.0.0.1:8000/docs 查看 Swagger 文档
"""


# 0.启动时自动建库 + 建表
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    Base.metadata.create_all(bind=db_engine)
    yield


# 1.创建FastAPI应用实例
app = FastAPI(lifespan=lifespan)

# 2. 路由注册
app.include_router(shop_route, prefix="/shop", tags=["购物车模块接口"])
app.include_router(user_route, prefix="/user", tags=["用户模块接口"])
app.include_router(exception_route, prefix="/exception", tags=["异常抛出演示"])
app.include_router(depends_route, prefix="/depends", tags=["依赖注入演示"])

# 3.异常处理注册
register_exception_handlers(app)

# 4.中间件注册：自定义请求耗时中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TimingMiddleware)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
