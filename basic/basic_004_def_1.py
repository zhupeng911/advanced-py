# 函数基础: 位置参数、关键字参数、*args、**kwargs、高阶函数、lambda
# ---------- 1. 函数参数 ----------
def say_hello(name, age):
    print(f'Hello:{name} age: {age}')


# 位置参数：必须记住参数定义的顺序，常用, 位置参数必须放在关键字参数之前
say_hello('Carlos', 18)

# 关键字参数：让你直接指名道姓，代码可读性更强
say_hello(age=18, name='Carlos')


# 强制关键字参数：*args 后面只能传关键字参数
def func_only_kwargs(a, *, b, c):
    """* 后只能传字典多余关键字参数"""
    print(f'a={a}, b={b}, c={c}')


func_only_kwargs(1, b=2, c=3)  # 直接关键字传参
func_only_kwargs(1, **{'b': 2, 'c': 3})  # 解包字典传参，** 把字典变成关键字参数


# func_only_kwargs(1, b=2) # TypeError: func_only_kwargs() missing 1 required keyword-only argument: 'c'


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
func_params(1, 2, 3, 4, 5, 40, 50, name='Alice', age=18)


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
# Lambda 表达式是 Python 的匿名函数，用一行代码创建简单函数
square = lambda x: x ** 2
add_three = lambda x, y, z: x + y + z

def is_positive(x):
    return x > 0
judge = lambda x: is_positive(x)
print(judge(5))

# 应用1: 排序自定义key
students = [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 20}]
sorted(students, key=lambda x: x['age'])  # 按age排序，升序
sorted(students, key=lambda x: x['age'], reverse=True)  # 按age排序，降序

# 应用2：map批量处理
nums = [1, 2, 3, 4]
list(map(lambda x: x ** 2, nums))  # [1, 4, 9, 16]

# 应用3：filter过滤
nums = [1, 2, 3, 4, 5, 6]
list(filter(lambda x: x % 2 == 0, nums))  # [2, 4, 6]
