# TypedDict 是 Python typing 模块提供的一个类，旨在为 字典（dict） 提供结构化的类型检查。
# 与 Pydantic 不同，TypedDict 在运行时不会进行数据校验或转换，它仅在开发阶段（IDE 或 mypy）提供静态类型提示，且性能开销几乎为零，非常适合追求极致性能且数据源可信的场景。
from typing import TypedDict


# 案例1：TypedDict 定义了字典应该包含哪些键，以及这些键对应的值是什么类型
class User(TypedDict):
    id: int
    username: str
    is_active: bool


# 正确使用
user: User = {"id": 1, "username": "gemini", "is_active": True}


# 静态检查错误示例（IDE 会标红）
# user_error: User = {"id": "1", "username": 123} # 类型不匹配


# 案例2：默认情况下，TypedDict=True 要求所有键必须存在。如果你希望某些键是可选的，可以使用 total=False
class ConnectionConfig(TypedDict, total=False):
    host: str
    port: int
    timeout: int


# 只提供 host 也是合法的
config: ConnectionConfig = {"host": "localhost"}

# 案例3：精细化控制 Required 与 NotRequired
from typing import TypedDict, Required, NotRequired


class Movie(TypedDict):
    title: str  # 必选
    year: Required[int]  # 显式必选
    rating: NotRequired[float]  # 可选字段


movie_1 = Movie(title="Gemini", year=2023)
movie_2 = Movie(title="Gemini", year=2023, rating=5.0)


# 案例4：嵌套结构与复杂应用
class Stats(TypedDict):
    views: int
    likes: int


class Article(TypedDict):
    title: str
    author: str
    metadata: Stats  # 嵌套 TypedDict


blog_post: Article = {
    "title": "TypedDict 详解",
    "author": "AI Assistant",
    "metadata": {"views": 100, "likes": 50}
}
print(blog_post)

# 特性           TypedDict                     Pydantic (BaseModel)
# 运行时校验      无（仅静态检查）                   严格校验
# 类型转换        无                              自动转换
# 性能           极快（就是原生 dict）              稍慢（有实例化和校验开销）
# 访问方式        obj[""key""]                    obj.key
# 主要用途        静态类型提示、旧代码兼容,           API 输入验证、复杂逻辑、结构化输出

# 用 TypedDict：当你需要高性能、或者数据结构简单且你完全信任数据来源时（如内部函数传递配置）。
# 用 Pydantic：当你处理来自用户输入、外部 API 请求、或者需要 LLM 生成结构化 JSON 时。
