# 函数
# 涉及语法: 位置参数、关键字参数、*args、**kwargs、高阶函数、lambda、map、filter、reduce、闭包、递归
# ---------- 1. 函数参数 ----------
from functools import reduce


def func_params(a, b, c=10, *args, d=20, e=30, **kwargs):
    """
        *args 元组 多余位置参数：args 后面的参数必须用关键字参数传值（即使有默认值也要 d=40）
        **kwargs 字典 多余关键字参数
    """
    print(f'a={a}, b={b}, c={c}')
    print(f'args={args}')  # 元组
    print(f'd={d}, e={e}')
    print(f'kwargs={kwargs}')  # 字典


def func_only_kwargs(a, *, b, c):
    """* 后只能传字典多余关键字参数"""
    print(f'a={a}, b={b}, c={c}')


# ---------- 2. 高阶函数 ----------
def add(x, y):
    return x + y


def multiply(x, y):
    return x * y


def apply_operation(func, x, y):
    """函数作为参数"""
    return func(x, y)


# ---------- 3. lambda 表达式 ----------
square = lambda x: x ** 2
add_three = lambda x, y, z: x + y + z


# ---------- 4. map、filter、reduce ----------
def map_filter_reduce(numbers):
    squared = list(map(lambda x: x ** 2, numbers))  # map: 转换每个元素
    even = list(filter(lambda x: x % 2 == 0, numbers))  # filter: 过滤
    total = reduce(lambda x, y: x + y, numbers, 0)  # 初始值 0
    product = reduce(lambda x, y: x * y, numbers, 1)
    return squared, even, total, product


# ---------- 5. 列表/字典/集合推导式 ----------
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares_dict = {x: x ** 2 for x in range(5)}
even_set = {x for x in numbers if x % 2 == 0}
matrix = [[i * j for j in range(3)] for i in range(3)]


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

if __name__ == '__main__':
    # ---------- 1. 函数参数 ----------
    print("=== 1. 函数参数 ===")
    func_params(1, 2, 3, 4, 5, d=40, e=50, name='Alice')
    func_params(1, 2, 3, 4, 5, 40, 50, name='Alice')
    func_only_kwargs(1, b=2, c=3)
    dict1 = {'b': 2, 'c': 3}
    func_only_kwargs(1, **dict1)

    # ---------- 2. 高阶函数 ----------
    print("\n=== 2. 高阶函数 ===")
    print(apply_operation(add, 3, 4))  # 7
    print(apply_operation(multiply, 3, 4))  # 12

    # ---------- 3. lambda ----------
    print("\n=== 3. lambda ===")
    print(square(5))  # 25
    print(add_three(1, 2, 3))  # 6

    # ---------- 4. map、filter、reduce ----------
    print("\n=== 4. map、filter、reduce ===")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    res = map_filter_reduce(numbers)
    print(f"squared={res[0]}, even={res[1]}, total={res[2]}, product={res[3]}")

    # ---------- 5. 推导式 ----------
    print("\n=== 5. 推导式 ===")
    print(f'squares_dict={squares_dict}')
    print(f'even_set={even_set}')
    print(f'matrix={matrix}')

    # ---------- 6. 闭包 ----------
    print("\n=== 6. 闭包 ===")
    print(closure(5))

    # ---------- 7. 装饰器 ----------
    print("\n=== 7. 装饰器 ===")
    slow_function()

    # ---------- 8. lambda + 闭包 ----------
    print("\n=== 10. lambda + 闭包 ===")
    print(square_func(4))  # 16
    print(cube_func(3))  # 27

    # ---------- 9. 函数组合 ----------
    print("\n=== 11. 函数组合 ===")
    print(sqrt_of_abs(-16))

    # ---------- 10. 偏函数 ----------
    print("\n=== 12. 偏函数 ===")
    print(square(5))  # 25
    print(cube(3))  # 27
