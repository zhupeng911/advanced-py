from sqlalchemy import Column, Integer, String, Float, DateTime, func

from core.config.pg_config import Base


# shop表：继承自 Base，表示这个类是一个 ORM 模型类
class Shop(Base):
    __tablename__ = "shop"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    counter = Column(Integer, nullable=False, default=0)
    price = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, server_default=func.now())
