# 函数
# 涉及语法: 位置参数、关键字参数、*args、**kwargs、高阶函数、lambda、map、filter、reduce、闭包、递归
# ---------- 1. 函数参数 ----------
def say_hello(name, age):
    print(f'Hello:{name} age: {age}')


# 位置参数：必须记住参数定义的顺序，常用, 位置参数必须放在关键字参数之前
say_hello('Carlos', 18)

# 关键字参数：让你直接指名道姓，代码可读性更强
say_hello(age=18, name='Carlos')


# 强制关键字参数：* 后面只能传关键字参数
def func_only_kwargs(a, *, b, c):
    """* 后只能传字典多余关键字参数"""
    print(f'a={a}, b={b}, c={c}')


func_only_kwargs(1, b=2, c=3)


# 任意数量的关键字参数: **kwargs, ** 将它们打包成一个字典
def func_params(a, b, c=10, *args, d=20, e=30, **kwargs):
    """
        *args：把多余的位置参数打包成一个 元组
        **kwargs：把多余的关键字参数打包成一个 字典
        顺序：位置参数 -> 默认参数 -> *args -> **kwargs
    """
    print(f'a={a}, b={b}, c={c}')
    print(f'args={args}')  # 元组
    print(f'd={d}, e={e}')
    print(f'kwargs={kwargs}')  # 字典


func_params(1, 2, 3, 4, 5, d=40, e=50, name='Alice')
func_params(1, 2, 3, 4, 5, 40, 50, name='Alice')


# ---------- 2. 函数返回值 ----------
# 单返回值
def add(x, y):
    return x + y


result = add(3, 5)


# 多返回值
def compute(x, y):
    return x + y, x - y, x * y, x / y


a, b, c, d = compute(3, 5)
print(a, b, c, d)

# ---------- 3. 函数作用域 ----------
# 全局变量：随处可访问
global_variable = 'I am available everywhere'


def some_function():
    print(global_variable)  # 可以访问全局变量
    # 局部变量：仅在此函数内存在
    local_variable = "only available within this function"
    print(local_variable)
    # 更新全局变量
    global global_variable
    global_variable = 'I am updated'


some_function()
print(global_variable)


# ---------- 4. 高阶函数 ----------
def add(x, y):
    return x + y


def multiply(x, y):
    return x * y


def apply_operation(func, x, y):
    """函数作为参数"""
    return func(x, y)


# ---------- 5. lambda 表达式 ----------
square = lambda x: x ** 2
add_three = lambda x, y, z: x + y + z


# ---------- 6. 闭包 ----------
# 定义：内部函数引用外部函数的变量，外部函数返回内部函数
# 三要素：1. 外层函数定义变量 2. 内层函数引用外层变量 3. 外层函数返回内层函数

def outer(x):  # 外部函数
    def inner(y):  # 内部函数
        return x + y  # 引用了外部函数的变量 x

    return inner  # 返回内部函数


closure = outer(10)
print(closure(5))  # 15，x=10 被保留
print(closure(3))  # 13，x=10 依然有效

# ---------- 7. 装饰器 ----------
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


# ---------- 8. 匿名函数与闭包结合 ----------
def make_power_func(exp):
    return lambda x: x ** exp


square_func = make_power_func(2)
cube_func = make_power_func(3)


# ---------- 9. 函数式组合 ----------
def compose(f, g):
    """函数组合: compose(f, g)(x) = f(g(x))"""
    return lambda x: f(g(x))


import math

sqrt_of_abs = compose(math.sqrt, abs)
print(sqrt_of_abs(-16))  # 4.0

# ---------- 10. 偏函数 ----------
from functools import partial


def power(base, exp):
    return base ** exp


# square = partial(power, exp=2)
cube = partial(power, exp=3)
