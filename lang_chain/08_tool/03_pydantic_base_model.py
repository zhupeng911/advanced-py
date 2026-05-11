from pydantic import BaseModel, Field, StrictInt, field_validator


# Pydantic = "类型注解 + 自动校验 + 类型转换"，
# 核心是将“不确定”的外部数据转化为“确定”的 Python 对象，让Python在运行也能享受静态类型的安全感
# 案例1：BaseModel 它不仅检查类型，还会尝试强制转换
class User(BaseModel):
    no: StrictInt  # 严格整数类型，拒绝自动类型转换
    id: int  # 必须是整数，或能转为整数的字符串
    username: str  # 字符串
    is_active: bool  # 布尔值


user_1 = User(no=1, id="123", username="johndoe", is_active=True)  # id="123" 自动转换为 id=123
user_2 = User(no=2, id=123, username="johndoe", is_active=True)


# 案例2:使用 Field 可以为字段添加校验规则
class Product(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0, description="价格必须大于0")
    tags: list[str] = Field(default_factory=list)


# 触发校验失败
try:
    # p = Product(name="A", price=-10)
    p = Product(name="AA", price=10, tags=["tag1", "tag2"])
except Exception as e:
    print(e)  # 会报错：name 太短，price 必须 > 0


# 案例3:嵌套模型与复杂结构，处理复杂的 JSON 结构
class Address(BaseModel):
    city: str
    zip_code: str


class Employee(BaseModel):
    name: str
    address: Address  # 嵌套模型
    skills: list[str]


data = {
    "name": "Alice",
    "address": {"city": "Shanghai", "zip_code": "200000"},
    "skills": ["Java", "Python"]
}

emp = Employee(**data)
print(emp.name)  # 输出: Alice
print(emp.address)  # 输出: city='Shanghai', zip_code='200000'
print(emp.skills)  # 输出: ['Java', 'Python']


# 案例4：自定义校验器（高级）
class Signup(BaseModel):
    password: str
    confirm_password: str

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if v != info.data.get("password"):
            raise ValueError("两次密码输入不一致")
        return v
