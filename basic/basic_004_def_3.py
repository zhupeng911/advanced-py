import functools
import time
# 装饰器

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
