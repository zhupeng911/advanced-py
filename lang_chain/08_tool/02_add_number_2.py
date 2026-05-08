from langchain_core.tools import tool
from pydantic import BaseModel, Field


# Pydantic = "类型注解 + 自动校验 + 类型转换"，让Python在运行也能享受静态类型的安全感
# class User(BaseModel):
#     no: StrictInt  # 严格整数类型，拒绝自动类型转换
#     id: int
#     name: str
#     age: int = 0
#
#
# try:
#     u = User(no=1, id=1, name="张三")
#     # u = User(no="1", id=1, name="张三") # Input should be a valid integer [type=int_type, input_value='1', input_type=str]
#     print(u)
# except Exception as e:
#     print(e)

class FieldInfo(BaseModel):
    a: int = Field(description="字段a")
    b: int = Field(description="字段b")


@tool(args_schema=FieldInfo)
def add_number(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b


result = add_number.invoke({"a": 1, "b": 2})
print(result)
