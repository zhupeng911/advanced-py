from langchain_core.tools import tool
from pydantic import BaseModel, Field


# Pydantic = "类型注解 + 自动校验 + 类型转换"，让Python在运行也能享受静态类型的安全感
# 案例1：BaseModel 检查入参合法性
class FieldInfo(BaseModel):
    # name: str = Field(min_length=2, max_length=50)
    # price: float = Field(gt=0, description="价格必须大于0")
    # tags: list[str] = Field(default_factory=list)
    a: int = Field(description="字段a", min_length=1, max_length=10)
    b: int = Field(description="字段b", min_length=1, max_length=10)


@tool("add_number", description="Add two numbers together", args_schema=FieldInfo, return_direct=True)
def add_number(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b


result = add_number.invoke({"a": 1, "b": 2})
print(result)
