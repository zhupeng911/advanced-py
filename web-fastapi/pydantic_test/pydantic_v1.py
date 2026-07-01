from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel, Field


# 一、 基础核心：声明模型与自动类型转换
class User(BaseModel):
    id: int  # 必填，且必须能隐式转换为int
    username: str  # 必填，字符串
    email: Optional[str] = None  # 可选，默认为None
    signup_ts: Optional[datetime] = None  # 可选，自动解析 ISO 格式的日期时间字符串， 默认为None
    tags: List[str] = []  # 可选，默认为空列表


# 1.案例1: 创建用户
user_data_1 = {
    "id": 123,  # "id": "123"也可以，自动变成 int
    "username": "johndoe",
    "email": "johndoe@example.com",
    "signup_ts": "2019-06-01 12:22:33",
    "tags": ["admin", "user"],
}
# ** 字典自动解包，等价于  User(name="张三", age=25, email="zhang@example.com")
user_1 = User(**user_data_1)
print(f'user_1.id: {user_1.id}')
print(f'type(user_1.id): {type(user_1.id)}')
print(f'user_1.email: {user_1.email}')
print(f'user_1.signup_ts: {user_1.signup_ts}')

# 2.案例2: 创建用户，无id，报错
user_data_2 = {
    "username": "johndoe",
    "email": "johndoe@example.com",
    "signup_ts": "2019-06-01 12:22:33",
    "tags": ["admin", "user"],
}
# user_2 = User(**user_data_2)
# print(f'user_2.id: {user_2.id}')


# 3.案例3: 创建用户，无tags，报错
user_data_3 = {
    "id": 123,
    "username": "johndoe",
    "email": "johndoe@example.com",
    "signup_ts": "2019-06-01 12:22:33"
}
user_3 = User(**user_data_3)
print(f'user_3.tags: {user_3.tags}')


# 二、 进阶校验：Field 的高级用法
class Product(BaseModel):
    # 1. 字符串长度限制与正则表达式
    sku: str = Field(min_length=6, max_length=12, pattern=r"^[A-Z0-9]+$")

    # 2. 列表长度限制
    labels: List[str] = Field(default=[], min_length=0, max_length=5, description="商品标签，最多5个")

    # 3. 数值范围限制与描述
    price: float = Field(gt=0, le=99999.9, description="商品单价，必须大于0且小于十万")

    # 4. 数值倍数约束
    quantity: int = Field(default=1, ge=0, le=9999, multiple_of=1, description="库存数量，必须是非负整数")

    # 5. 枚举值限制与 Schema 示例
    currency: str = Field(default="CNY", pattern=r"^(CNY|USD|EUR)$", examples=["CNY", "USD"],
                          description="货币代码，仅支持 CNY/USD/EUR")

    # 6.default与default_factory
    # default:   固定值，类定义时就确定了，不能改变
    # default_factory：调用时才生成，每次创建实例时才执行
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间，调用时才生成")

    # 7. 其他
    # 7.1 字段别名：允许前端传入 "productName" 或 "product_name"，但在 Python 内部一律用 product_name 访问
    product_name: str = Field(validation_alias="productName")

    # 7.2 序列化控制：转为 JSON/字典时自动隐藏敏感隐私字段
    secret_code: str = Field(exclude=True)

    # 7.3 严格模式
    discount: float = Field(default=0.0, ge=0, le=1, strict=True, description="折扣率 0~1，拒绝字符串自动转换")
