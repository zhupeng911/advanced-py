# 函数：解包、闭包、装饰器
import functools
import time

# ---------- 1. 解包 ----------
# 解包（Unpacking）：就是把一个容器（列表、元组、字典等）拆开，把里面的元素单独取出来的过程
# 基本解包：列表/元组
a, b, c = [1, 2, 3]  # a=1, b=2, c=3
e, f = (10, 20)  # e=10, f=20
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

# 场景2：拉链操作（zip逆操作）
pairs = [('a', 1), ('b', 2), ('c', 3)]
keys, values = zip(*pairs)  # keys=('a','b','c'), values=(1,2,3)


# 场景3：展开函数参数
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


# 场景1：函数工厂（避免重复计算）
def make_multiplier(n):
    return lambda number: number * n


double = make_multiplier(2)  # x*2
triple = make_multiplier(3)  # x*3
print(double(5))  # 10
print(triple(5))  # 15


# 场景2：计数器
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


# ---------- 3. 装饰器 ----------
# 定义：装饰器是包装函数的语法糖，在不修改原函数源码的情况下增强功能
# 本质：装饰器也是闭包，外层函数接收原函数，内层函数负责增强并调用原函数

def logger(func):
    """日志装饰器：记录函数调用前后的信息"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"调用函数: {func.__name__}")
        print(f"位置参数: {args}, 关键字参数: {kwargs}")
        result = func(*args, **kwargs)
        print(f"返回结果: {result}")
        return result

    return wrapper


def timer(func):
    """计时装饰器：统计函数运行耗时"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        cost = time.perf_counter() - start
        print(f"{func.__name__} 耗时: {cost:.4f}s")
        return result

    return wrapper


def retry(max_attempts=3, delay=0, exceptions=(Exception,)):
    """带参数装饰器：函数失败后自动重试

    max_attempts：最多执行次数
    delay：每次失败后的等待秒数
    exceptions：只捕获并重试指定异常类型
    """
    if max_attempts < 1:
        raise ValueError("max_attempts 必须大于等于 1")

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as error:
                    last_error = error
                    if attempt == max_attempts:
                        break
                    print(f"第 {attempt} 次失败: {error}，准备重试...")
                    if delay > 0:
                        time.sleep(delay)
            print(f"{func.__name__} 最终失败: {last_error}")
            raise last_error

        return wrapper

    return decorator


@logger
def greet(name, greeting="你好"):
    """普通装饰器示例：支持位置参数和关键字参数"""
    return f"{greeting}, {name}"


@timer
def slow_function():
    """计时装饰器示例"""
    time.sleep(0.1)
    return "done"


@retry(max_attempts=3, delay=0.1)
def unstable_task():
    """带参数装饰器示例：模拟前两次失败，第三次成功"""
    unstable_task.calls += 1
    if unstable_task.calls < 3:
        raise ValueError("网络临时异常")
    return "请求成功"


unstable_task.calls = 0


@timer
@logger
def add(a, b):
    """多个装饰器叠加：执行顺序等价于 add = timer(logger(add))"""
    return a + b


if __name__ == '__main__':
    print(greet("小明", greeting="早上好"))
    print(slow_function())
    print(unstable_task())
    print(add(10, 20))

    # functools.wraps 会保留原函数名称和文档字符串，方便调试和生成文档
    print(greet.__name__)  # greet
    print(greet.__doc__)  # 普通装饰器示例：支持位置参数和关键字参数
