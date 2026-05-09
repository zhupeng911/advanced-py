# 函数：解包、闭包、装饰器
# ---------- 1. 解包 ----------
# 解包（Unpacking）：就是把一个容器（列表、元组、字典等）拆开，把里面的元素单独取出来的过程
# 基本解包：列表/元组
a, b, c = [1, 2, 3]  # a=1, b=2, c=3
e, f = (10, 20)  # a=10, b=20
# 基本解包：交换变量（无需临时变量）
a, b = b, a

# 星号解包：剩余元素
first, *middle, last = [1, 2, 3, 4, 5]  # first=1, middle=[2,3,4], last=5
# 星号解包：头部/尾部拆解
head, *tail = [1, 2, 3, 4, 5]  # head=1, tail=[2,3,4,5]
# 星号解包：忽略元素
g, _, h, _ = [1, 2, 3, 4]  # g=1, h=3

# 字典解包 **：合并字典
d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}
res = {**d1, **d2}  # {'a': 1, 'b': 3, 'c': 4}
# 字典解包 **：函数传参
defaults = {'timeout': 30, 'retry': 3}
options = {'timeout': 60}
config = {**defaults, **options}

# 嵌套解包
(x, (y, z)), w = ([1, (2, 3)], 4)  # x=1, y=2, z=3, w=4
name, age, (city, country) = ('Alice', 25,
                              ('Beijing', 'China'))  # name='Alice', age=25, city='Beijing', country='China'

# 场景1: 遍历key-value
d = {'a': 1, 'b': 2, 'c': 3}
for k, v in d.items():
    print(k, v)

# 场景2:拉链操作（zip逆操作）
pairs = [('a', 1), ('b', 2), ('c', 3)]
keys, values = zip(*pairs)  # keys=('a','b','c'), values=(1,2,3)


# 场景3:展开函数参数
# args = (1, 2, 3)
# func(*args)
# kwargs = {'name': 'Alice', 'age': 25}
# func(**kwargs)


# ---------- 2. 闭包 ----------
# 定义：内部函数引用外部函数的变量，外部函数返回内部函数
# 三要素：1. 外层函数定义变量 2. 内层函数引用外层变量 3. 外层函数返回内层函数

def outer(x):  # 外部函数
    def inner(y):  # 内部函数
        return x + y  # 引用了外部函数的变量 x

    return inner  # 返回内部函数


closure = outer(10)  # outer返回inner，x=10被捕获
print(closure(5))  # 15，x=10 被保留
print(closure(3))  # 13，x=10 依然有效


# 场景1. 函数工厂（避免重复计算）
def make_multiplier(n):
    return lambda x: x * n


double = make_multiplier(2)  # x*2
triple = make_multiplier(3)  # x*3
print(double(5))  # 10
print(triple(5))  # 15


# 场景2. 计数器
def counter():
    count = 0

    def inc():
        nonlocal count
        count += 1
        return count

    return inc


c = counter()
print(c())  # 1
print(c())  # 2
print(c())  # 3


# 场景3. 装饰器（本质就是闭包）
def logger(func):
    def wrapper(*args):
        print(f'Calling {func.__name__}')
        return func(*args)

    return wrapper


# ---------- 3. 装饰器 ----------
# 定义：装饰器是包装函数的语法糖，在不修改原函数的情况下增强功能
import functools
import time


def timer(func):
    """计时装饰器"""

    @functools.wraps(func)  # 1. 装饰器函数
    def wrapper(*args, **kwargs):  # 2. 包装函数
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} 耗时: {time.time() - start:.4f}s")
        return result

    return wrapper


def retry(max_attempts=3):
    """重试装饰器"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"重试中... {e}")
            return None

        return wrapper

    return decorator


@timer  # 3. 语法糖
def slow_function():
    time.sleep(0.1)
    return "done"
