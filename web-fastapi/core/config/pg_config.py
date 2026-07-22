import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1.加载环境变量 .env文件
load_dotenv()


# 2.配置数据库连接信息
class PGConfig:
    # PostgreSQL
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME", "py_testdb")
    DB_USER = os.getenv("DB_USER", "zhupeng")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "zhupeng123")
    DB_MIN_CONN = int(os.getenv("DB_MIN_CONN", 2))
    DB_MAX_CONN = int(os.getenv("DB_MAX_CONN", 10))

    @staticmethod
    def get_database_url() -> str:
        return (
            f"postgresql+psycopg://{PGConfig.DB_USER}:{PGConfig.DB_PASSWORD}@{PGConfig.DB_HOST}:{PGConfig.DB_PORT}/{PGConfig.DB_NAME}"
        )


# 3.创建数据库连接池：维护一组到 PostgreSQL 的长连接（连接池），全局复用
DbEngine = create_engine(
    PGConfig.get_database_url(),
    pool_size=PGConfig.DB_MIN_CONN,
    max_overflow=PGConfig.DB_MAX_CONN - PGConfig.DB_MIN_CONN,
)

# 4.创建数据库会话：增删改查的全部改动先在 session 里攒着，commit()一次性写入数据库
SessionLocal = sessionmaker(bind=DbEngine, autocommit=False, autoflush=False)

# 5.创建数据库模型基类：自动把你的 class Shop 映射成 shops 表。create_all() 就是拿着所有继承它的类去数据库里自动建表
Base = declarative_base()
