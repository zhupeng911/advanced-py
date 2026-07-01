from datetime import date
from typing import List

from pydantic import BaseModel, field_validator, model_validator


# 三、 动态逻辑校验：@field_validator 与 @model_validator
# 当静态的 Field 无法解决复杂的跨字段联动校验时，就需要用到 Pydantic 强大的装饰器验证器。
# 1. 针对单个字段的验证 (@field_validator)
class RegisterRequest(BaseModel):
    username: str
    password: str

    @field_validator("password")
    @classmethod  # 必须指定为类方法： field_validator 在实例 __init__ 之前运行，此时还没有 self，所以只能是类方法
    def validate_password(cls, password: str):
        if len(password) < 8:
            raise ValueError("密码长度不能小于8")
        if not any(char.isdigit() for char in password):
            raise ValueError("密码必须包含数字")
        return password


# 2. 针对整个模型的跨字段联动验证 (@model_validator)
# model_validator 有三种 mode：before / after / wrap，各有不同的应用场景

# ---- mode="before": 在字段校验之前运行，拿到的是原始字典 ----
# 适用场景：数据清洗、字段改名、对原始数据进行预处理
class SignupRequest(BaseModel):
    email: str
    password: str
    password_confirm: str

    @model_validator(mode="before")
    @classmethod
    def preprocess_data(cls, data: dict) -> dict:
        # data 是原始 dict，字段还没做类型校验
        # 场景1：去掉首尾空格、统一小写
        if isinstance(data.get("email"), str):
            data["email"] = data["email"].strip().lower()
        # 场景2：前端多传了一个字段，合并进 password 中
        if "password_raw" in data:
            data["password"] = data.pop("password_raw")
        return data  # 返回 dict，交给下一步做字段校验


# ---- mode="after": 字段校验完成后运行，拿到的是实例对象 ----
# 适用场景：跨字段校验（密码一致性、日期大小、状态机合法性）
class Event(BaseModel):
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def check_date_range(self) -> "Event":
        # self 已经是完整实例，字段已完成类型转换
        if self.start_date > self.end_date:
            raise ValueError("结束时间不能早于开始时间")
        return self  # 返回实例对象


# ---- mode="wrap": 完全接管校验流程 ----
# 适用场景：需要在默认校验前后都插入逻辑（如日志、自定义转换 + 校验）
class Payment(BaseModel):
    amount: float
    currency: str

    @model_validator(mode="wrap")
    @classmethod
    def validate_payment(cls, data: dict, handler):
        # 进入 handler 之前：可以做前置处理
        print(f"[wrap-before] 原始数据: {data}")

        # handler(data) 会执行 Pydantic 默认的校验流程（字段校验 + 类型转换）
        validated: "Payment" = handler(data)

        # handler 返回之后：可以做后置校验或修正
        print(f"[wrap-after] 校验后: amount={validated.amount}, currency={validated.currency}")

        if validated.currency == "USD" and validated.amount > 10000:
            raise ValueError("美元支付单笔不能超过 10000")
        return validated


# ---- 各个 mode 的执行时序对比 ----
# 原始数据 → before(原始dict) → 字段校验 → after(实例) → 最终实例
#                          ←──── wrap(完全包裹) ────→
# wrap 的 handler 就是中间的"字段校验"环节


# 案例演示
print("\n=== before 案例: 数据预处理 ===")
req1 = SignupRequest(email=" USER@Example.com ", password="12345678", password_confirm="12345678")
print(f"email 自动 trim + 小写: {req1.email}")

print("\n=== after 案例: 跨字段校验 ===")
try:
    Event(start_date="2026-06-30", end_date="2026-06-29")
except ValueError as e:
    print(f"日期校验失败: {e}")

print("\n=== wrap 案例: 前后拦截 ===")
try:
    Payment(amount=15000, currency="USD")
except ValueError as e:
    print(f"支付校验失败: {e}")

Payment(amount=100, currency="CNY")  # 正常通过


# 四、 模型嵌套与复杂数据结构
# Pydantic 天生支持完美的树状嵌套结构，这是它能够精准解析复杂企业级微服务 JSON 的底气所在：
class OrderItem(BaseModel):
    item_id: int
    quantity: int
    price: float


class Order(BaseModel):
    order_id: str
    customer_id: int
    # 嵌套其他 Pydantic 模型作为列表元素
    items: List[OrderItem]


# 完美解析多层嵌套的复杂 JSON 字典
order_data = {
    "order_id": "ORD-2026-999",
    "customer_id": 8888,
    "items": [
        {"item_id": 101, "quantity": 2, "price": 45.0},
        {"item_id": 102, "quantity": 1, "price": 120.0}
    ]
}

order = Order(**order_data)
print(order.items[0].price)  # 输出: 45.0
