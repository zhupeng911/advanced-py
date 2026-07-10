from sqlalchemy import Column, Integer, String, DateTime, func

from core.config.pg_config import Base


# user表：继承自 Base，表示这个类是一个 ORM 模型类
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String(100), nullable=True)
    password_hash = Column(String(128), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
