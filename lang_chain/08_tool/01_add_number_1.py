from langchain_core.tools import tool


@tool
def add_number(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b


result = add_number.invoke({"a": 1, "b": 2})
print(result)
