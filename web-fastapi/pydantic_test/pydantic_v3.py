import uuid
from enum import Enum
from ipaddress import IPv4Address, IPv6Address
from typing import Annotated, Literal, Optional
from uuid import UUID

from pydantic import (
    AnyHttpUrl,
    AnyUrl,
    BaseModel,
    EmailStr,
    Field,
    SecretStr,
    ValidationError,
)


# ============================================================
# 五、Pydantic 内置扩展类型
# Pydantic 对 Python 标准库和常用类型提供了原生支持
# ============================================================

# ---- 5.1 邮箱校验 EmailStr ----
# pip install pydantic[email] 或 pip install email-validator
class EmailModel(BaseModel):
    email: EmailStr


print("=== 5.1 EmailStr ===")
m = EmailModel(email="test@example.com")
print(f"合法邮箱: {m.email}")
try:
    EmailModel(email="not-an-email")
except ValidationError as e:
    print(f"非法邮箱校验: {e.errors()[0]['msg']}")


# ---- 5.2 URL校验：AnyUrl / AnyHttpUrl ----
class UrlModel(BaseModel):
    homepage: AnyUrl  # 任意 URL scheme（http/https/ftp 等）
    avatar: AnyHttpUrl  # 仅 http/https


print("\n=== 5.2 AnyUrl / AnyHttpUrl ===")
m = UrlModel(homepage="https://example.com/path?q=1", avatar="https://img.com/a.jpg")
print(f"scheme={m.homepage.scheme}, host={m.homepage.host}, path={m.homepage.path}")
try:
    UrlModel(homepage="https://ok.com", avatar="ftp://bad.jpg")  # avatar 必须 http/https
except ValidationError as e:
    print(f"avatar 非 http/https: {e.errors()[0]['msg']}")


# ---- 5.3 UUID ----
class UUIDModel(BaseModel):
    user_id: UUID
    trace_id: UUID = Field(default_factory=uuid.uuid4)


print("\n=== 5.3 UUID ===")
m = UUIDModel(user_id="550e8400-e29b-41d4-a716-446655440000")
print(f"user_id: {m.user_id}, trace_id(自动生成): {m.trace_id}")


# ---- 5.4 IPv4Address / IPv6Address ----
class IPModel(BaseModel):
    ipv4: IPv4Address
    ipv6: Optional[IPv6Address] = None


print("\n=== 5.4 IPv4Address / IPv6Address ===")
m = IPModel(ipv4="192.168.1.1", ipv6="::1")
print(f"ipv4={m.ipv4}, ipv6={m.ipv6}")
try:
    IPModel(ipv4="999.999.999.999")
except ValidationError as e:
    print(f"非法 IP: {e.errors()[0]['msg']}")


# ---- 5.5 SecretStr ----
class CredentialModel(BaseModel):
    username: str
    password: SecretStr


print("\n=== 5.5 SecretStr ===")
m = CredentialModel(username="admin", password="s3cret!")
print(f"打印时自动隐藏: {m.password}")  # SecretStr('**********')
print(f"获取明文: {m.password.get_secret_value()}")


# ============================================================
# 六、约束类型（v2 推荐方式：Annotated + Field）
# v1 的 conint/constr/confloat 已废弃，v2 用 Annotated 组合
# ============================================================

class ConstrainedModel(BaseModel):
    # 数值约束
    age: Annotated[int, Field(gt=0, le=150)]
    score: Annotated[float, Field(ge=0.0, le=100.0, multiple_of=0.5)]

    # 字符串约束
    code: Annotated[str, Field(min_length=3, max_length=10, pattern=r"^[A-Z]{3,10}$")]

    # 列表长度约束
    tags: Annotated[list[str], Field(min_length=1, max_length=5)]


print("\n=== 六、约束类型 ===")
m = ConstrainedModel(age=25, score=88.5, code="PYTHON", tags=["dev", "tutorial"])
print(f"age={m.age}, score={m.score}, code={m.code}, tags={m.tags}")

print("\n--- 校验失败示例 ---")
for bad_data, desc in [
    ({"age": -1, "score": 50.0, "code": "PY", "tags": ["x"]}, "年龄负数"),
    ({"age": 200, "score": 50.0, "code": "PYTHON", "tags": ["x"]}, "年龄超限"),
    ({"age": 25, "score": 50.0, "code": "python", "tags": ["x"]}, "code 非大写"),
    ({"age": 25, "score": 50.0, "code": "PYTHON", "tags": []}, "tags 为空"),
]:
    try:
        ConstrainedModel(**bad_data)
    except ValidationError as e:
        print(f"  {desc} → {e.errors()[0]['msg']}")


# ============================================================
# 七、Literal 与 Enum
# ============================================================

# ---- 7.1 Literal：限定为固定字面值 ----
class OrderModel(BaseModel):
    status: Literal["pending", "shipped", "delivered", "cancelled"]


print("\n=== 七、Literal 与 Enum ===")
print("--- 7.1 Literal ---")
m = OrderModel(status="shipped")
print(f"status={m.status}")
try:
    OrderModel(status="unknown")
except ValidationError as e:
    print(f"非法字面值: {e.errors()[0]['msg']}")


# ---- 7.2 Enum：用类组织枚举值 ----
class RoleEnum(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class UserRoleModel(BaseModel):
    name: str
    role: RoleEnum


print("\n--- 7.2 Enum ---")
m = UserRoleModel(name="张三", role=RoleEnum.EDITOR)
print(f"role={m.role}, value={m.role.value}")
try:
    UserRoleModel(name="张三", role="superadmin")  # 不在枚举中
except ValidationError as e:
    print(f"非法枚举值: {e.errors()[0]['msg']}")

# ============================================================
# 八、model_config 常用配置
# ============================================================

print("\n=== 八、model_config ===")


# ---- 8.1 extra：控制多余字段 ----
class StrictUser(BaseModel):
    model_config = {"extra": "forbid"}  # 禁止传入未定义的字段
    name: str
    age: int


print("--- 8.1 extra='forbid' ---")
m = StrictUser(name="李四", age=30)
print(f"正常: name={m.name}, age={m.age}")
try:
    StrictUser(name="李四", age=30, hobby="coding")  # hobby 未定义
except ValidationError as e:
    print(f"多余字段被拦截: {e.errors()[0]['msg']}")


# extra 的三种取值：
# - "ignore": 忽略多余字段（默认）
# - "forbid":  禁止多余字段，抛出错误
# - "allow":   接受多余字段，保留在 model_extra 中


class IgnoreExtra(BaseModel):
    model_config = {"extra": "ignore"}
    name: str


m = IgnoreExtra(name="王五", hobby="coding")
print(f"extra='ignore': name={m.name}, hobby 被丢弃无提示")


# ---- 8.2 frozen：不可变模型 ----
class Config(BaseModel):
    model_config = {"frozen": True}
    api_key: str
    timeout: int = 30


print("\n--- 8.2 frozen=True ---")
m = Config(api_key="sk-abc123")
print(f"api_key={m.api_key}")
try:
    m.api_key = "new-key"  # frozen 后禁止修改
except Exception as e:
    print(f"frozen 禁止修改: {type(e).__name__}")


# ---- 8.3 from_attributes：从 ORM 对象创建 ----
# 允许 model_validate(obj) 从任意有属性的对象读取字段


class ORMUser(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    name: str


class FakeORM:
    """模拟 SQLAlchemy ORM 对象"""

    def __init__(self):
        self.id = 1
        self.name = "orm_user"


print("\n--- 8.3 from_attributes=True ---")
orm_obj = FakeORM()
m = ORMUser.model_validate(orm_obj)
print(f"从 ORM 对象创建: id={m.id}, name={m.name}")


# ---- 8.4 validate_assignment：赋值时也校验 ----
class SafeUser(BaseModel):
    model_config = {"validate_assignment": True}
    name: str
    age: Annotated[int, Field(ge=0, le=150)]


print("\n--- 8.4 validate_assignment=True ---")
m = SafeUser(name="test", age=25)
print(f"初始: age={m.age}")
try:
    m.age = -1  # 赋值时也会触发校验
except ValidationError as e:
    print(f"赋值时校验拦截: {e.errors()[0]['msg']}")


# ---- 8.5 populate_by_name：同时支持原始字段名和别名输入 ----
class AliasModel(BaseModel):
    model_config = {"populate_by_name": True}
    user_name: str = Field(alias="userName")


print("\n--- 8.5 populate_by_name=True ---")
# 可以用原始字段名 user_name 或别名 userName 传入
m1 = AliasModel(userName="alias_input")
m2 = AliasModel(user_name="original_input")
print(f"别名输入: {m1.user_name}, 原名输入: {m2.user_name}")


# ---- 8.6 综合配置 ----
class FullConfigModel(BaseModel):
    model_config = {
        "extra": "forbid",
        "frozen": False,
        "from_attributes": True,
        "validate_assignment": True,
        "populate_by_name": True,
        "str_strip_whitespace": True,  # 自动去除 str 首尾空格
    }
    username: str
    email: EmailStr
    age: Annotated[int, Field(ge=0, le=150)]


print("\n--- 8.6 综合配置 ---")
m = FullConfigModel(username="  spaced_user  ", email="test@example.com", age=18)
print(f"str_strip_whitespace 自动 trim: username='{m.username}'")


# ============================================================
# 九、validate_default：验证默认值是否符合约束
# ============================================================

class ConfigWithDefaultCheck(BaseModel):
    model_config = {"validate_default": True}
    port: Annotated[int, Field(gt=0, lt=65536)] = 8080  # 默认值符合约束，OK


print("\n=== 九、validate_default ===")
m = ConfigWithDefaultCheck()
print(f"port 默认值通过校验: {m.port}")

if __name__ == "__main__":
    print("\n>>> 01_pydantic_v3.py 全部示例运行完毕")
