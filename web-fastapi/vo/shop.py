from pydantic import BaseModel, Field


# 数据模型：创建购物车Vo
class ShopCreateVo(BaseModel):
    """创建购物车请求体"""
    name: str = Field(..., min_length=1, max_length=100, description="购物车名称")
    counter: int = Field(..., ge=0, le=10, description="数量")
    price: float = Field(..., ge=0, description="价格")
