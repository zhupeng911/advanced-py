import datetime
from typing import Annotated, Generic, List, Literal, Optional, TypeVar, Union

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    Discriminator,
    Field,
    PrivateAttr,
    Tag,
    ValidationError,
    computed_field,
    field_validator,
    model_validator,
)


# ============================================================
# 十、field_validator 高级用法：mode 参数
# ============================================================

# ---- 10.1 mode="before"：字段校验前对原始值做预处理 ----
class UserProfile(BaseModel):
    phone: str

    @field_validator("phone", mode="before")
    @classmethod
    def normalize_phone(cls, v: str) -> str:
        """字段校验前：清洗手机号（去空格、去横线）"""
        if isinstance(v, str):
            v = v.replace(" ", "").replace("-", "")
        return v  # 返回清洗后的值，交给下一步类型校验

    @field_validator("phone")
    @classmethod
    def validate_phone_pattern(cls, v: str) -> str:
        """字段校验后：验证手机号格式"""
        if not (v.isdigit() and len(v) == 11):
            raise ValueError("手机号必须是11位数字")
        return v


print("=== 十、field_validator mode 参数 ===")
print("--- 10.1 mode='before' ---")
m = UserProfile(phone="138-1234-5678")
print(f"自动清洗后: {m.phone}")

try:
    UserProfile(phone="123")
except ValidationError as e:
    print(f"校验失败: {e.errors()[0]['msg']}")

# ---- 10.2 mode="after"：字段校验后进行二次判断 ----
class PaymentCheck(BaseModel):
    amount: float

    @field_validator("amount", mode="after")
    @classmethod
    def check_amount_reasonable(cls, v: float) -> float:
        """类型转换已完成，v 已经是 float"""
        if v > 100000:
            raise ValueError("单笔金额不得超过 100000")
        if v <= 0:
            raise ValueError("金额必须大于 0")
        return v


print("\n--- 10.2 mode='after' ---")
try:
    PaymentCheck(amount=200000)
except ValidationError as e:
    print(f"超额拦截: {e.errors()[0]['msg']}")

# ---- mode 总结 ----
# before → 字段类型校验前，拿到原始值，可做清洗/转换
# after  → 字段类型校验后，拿到已转换的正确类型，可做附加判断
# 默认(不传mode) → 等同于 after，在类型转换后执行


# ============================================================
# 十一、Annotated + 函数式校验器
# v2 推荐方式：将校验逻辑提取为可复用的函数
# ============================================================

def strip_whitespace(v: str) -> str:
    """BeforeValidator 函数：去除首尾空格"""
    return v.strip()


def must_be_alphanumeric(v: str) -> str:
    """AfterValidator 函数：必须字母数字"""
    if not v.replace("-", "").replace("_", "").isalnum():
        raise ValueError("只能包含字母、数字、-、_")
    return v


def must_be_positive(v: float) -> float:
    """AfterValidator 函数"""
    if v <= 0:
        raise ValueError("必须大于 0")
    return v


print("\n=== 十一、Annotated + 函数式校验器 ===")

# ---- 11.1 单个校验器 ----
class ProductV2(BaseModel):
    sku: Annotated[str, AfterValidator(must_be_alphanumeric)]
    price: Annotated[float, AfterValidator(must_be_positive)]


m = ProductV2(sku="ITEM-001", price=99.9)
print(f"sku={m.sku}, price={m.price}")

# ---- 11.2 链式组合：Before + After ----
class SanitizedProduct(BaseModel):
    name: Annotated[
        str,
        BeforeValidator(strip_whitespace),  # 先执行：去空格
        AfterValidator(must_be_alphanumeric),  # 再执行：格式校验
    ]


print("\n--- 11.2 链式组合 ---")
m = SanitizedProduct(name="  Clean_Name  ")
print(f"trim 后: '{m.name}'")

try:
    SanitizedProduct(name="  $$$bad  ")
except ValidationError as e:
    print(f"AfterValidator 拦截: {e.errors()[0]['msg']}")

# ---- 11.3 复用校验函数到多处 ----
class OrderItemV2(BaseModel):
    product_sku: Annotated[str, AfterValidator(must_be_alphanumeric)]
    warehouse_code: Annotated[str, AfterValidator(must_be_alphanumeric)]  # 同一个函数复用


# ============================================================
# 十二、Discriminated Union（判别联合类型）
# 根据某个字段的值自动匹配合适的子模型
# ============================================================

print("\n=== 十二、Discriminated Union ===")


class CatData(BaseModel):
    pet_type: Literal["cat"]
    meow_volume: int  # 猫叫音量


class DogData(BaseModel):
    pet_type: Literal["dog"]
    bark_loudness: int  # 犬吠响度


class Owner(BaseModel):
    name: str
    # 关键：根据 pet_type 字段自动判别是 CatData 还是 DogData
    pet: Annotated[
        Union[Annotated[CatData, Tag("cat")], Annotated[DogData, Tag("dog")]],
        Discriminator("pet_type"),
    ]


owner_with_cat_data = {"name": "Alice", "pet": {"pet_type": "cat", "meow_volume": 80}}
owner_with_dog_data = {"name": "Bob", "pet": {"pet_type": "dog", "bark_loudness": 99}}

owner_cat = Owner(**owner_with_cat_data)
owner_dog = Owner(**owner_with_dog_data)

print(f"Alice 的宠物是 Cat: 音量={owner_cat.pet.meow_volume}")
print(f"Bob 的宠物是 Dog: 响度={owner_dog.pet.bark_loudness}")
# 注意：owner_cat.pet 的类型是 CatData，有 meow_volume 属性，没有 bark_loudness

# 非法 pet_type 会被拦截
try:
    Owner(**{"name": "Eve", "pet": {"pet_type": "fish", "whatever": 1}})
except ValidationError as e:
    print(f"非法 pet_type 被拦截: {e.errors()[0]['msg']}")


# ============================================================
# 十三、@computed_field：计算字段
# 不存储数据，每次访问动态计算
# ============================================================

print("\n=== 十三、@computed_field ===")


class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:
        """面积 = 宽 × 高，每次取值时动态计算"""
        return self.width * self.height

    @computed_field(alias="perimeterValue")
    @property
    def perimeter(self) -> float:
        """周长，支持 alias 控制序列化字段名"""
        return 2 * (self.width + self.height)


rect = Rectangle(width=10, height=20)
print(f"area={rect.area}, perimeter={rect.perimeter}")
print(f"序列化(原名): {rect.model_dump()}")
print(f"序列化(别名): {rect.model_dump(by_alias=True)}")  # perimeter → perimeterValue

# 修改 width 后，computed_field 自动反映最新值
rect.width = 15
print(f"width 修改后 area={rect.area}")


# ============================================================
# 十四、PrivateAttr：私有属性
# 不参与校验、不参与序列化、仅运行时内部使用
# ============================================================

print("\n=== 十四、PrivateAttr ===")


class Counter(BaseModel):
    name: str
    _access_count: int = PrivateAttr(default=0)  # 私有属性
    _created_at: datetime.datetime = PrivateAttr(default_factory=datetime.datetime.now)

    def access(self) -> str:
        self._access_count += 1
        return f"{self.name} 第 {self._access_count} 次访问，创建于 {self._created_at}"

    def model_dump(self, **kwargs):
        # 默认序列化不包含 _private_attr
        d = super().model_dump(**kwargs)
        return d


c = Counter(name="计数器A")
print(c.access())
print(c.access())
dumped = c.model_dump()
print(f"序列化结果（不含私有属性）: {dumped}")
# 注意：构造时传入 _access_count=999 会被忽略（不是模型字段）


# ============================================================
# 十五、递归模型：模型自引用
# 适用场景：树形结构、嵌套评论、组织架构
# ============================================================

print("\n=== 十五、递归模型 ===")


class Category(BaseModel):
    name: str
    children: Optional[List["Category"]] = None  # 自引用


# 手动重建模型以解决前向引用
Category.model_rebuild()

category_data = {
    "name": "电子产品",
    "children": [
        {"name": "手机", "children": [{"name": "iPhone"}, {"name": "Android"}]},
        {"name": "电脑", "children": [{"name": "笔记本"}, {"name": "台式机"}]},
    ],
}

root = Category(**category_data)
print(f"根分类: {root.name}")
print(f"  子分类: {[c.name for c in root.children]}")
print(f"    手机的子孙: {[c.name for c in root.children[0].children]}")


# ============================================================
# 十六、泛型模型（Generic BaseModel）
# 适用场景：统一的分页响应结构、通用 API 包裹层
# ============================================================

print("\n=== 十六、泛型模型 ===")

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int

    @computed_field
    @property
    def total_pages(self) -> int:
        """自动计算总页数"""
        import math
        return max(1, math.ceil(self.total / self.page_size))


class UserItem(BaseModel):
    id: int
    name: str
    email: str


class ProductItem(BaseModel):
    sku: str
    price: float


# 泛型实例化：分页用户列表
users_page = PaginatedResponse[UserItem](
    items=[UserItem(id=1, name="Alice", email="alice@example.com")],
    total=1,
    page=1,
    page_size=10,
)
print(f"用户分页: items={len(users_page.items)}, total_pages={users_page.total_pages}")

# 同样结构用于商品分页
products_page = PaginatedResponse[ProductItem](
    items=[ProductItem(sku="A001", price=19.9), ProductItem(sku="A002", price=29.9)],
    total=2,
    page=1,
    page_size=10,
)
print(f"商品分页: items={len(products_page.items)}, total_pages={products_page.total_pages}")


# ============================================================
# 十七、create_model：动态创建模型
# ============================================================

print("\n=== 十七、create_model ===")

from pydantic import create_model

# 运行时动态创建一个模型类，适用于：
# - 根据配置文件动态生成 API 入参模型
# - ORM 字段动态映射
# - 插件系统
DynamicForm = create_model(
    "DynamicForm",
    field_a=(int, Field(gt=0)),
    field_b=(str, "default_value"),  # 带默认值
    __config__={"extra": "forbid"},
)

form = DynamicForm(field_a=42, field_b="hello")
print(f"动态模型: field_a={form.field_a}, field_b={form.field_b}")
print(f"模型名: {DynamicForm.__name__}")

# 验证也生效
try:
    DynamicForm(field_a=-1)
except ValidationError as e:
    print(f"动态模型校验: {e.errors()[0]['msg']}")


if __name__ == "__main__":
    print("\n>>> 01_pydantic_v4.py 全部示例运行完毕")
