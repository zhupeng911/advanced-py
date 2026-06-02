import time


# ---------- 装饰器 ----------
# 定义：装饰器是包装函数的语法糖，在不修改原函数源码的情况下增强功能
# 本质：装饰器也是闭包，外层函数接收原函数，内层函数负责增强并调用原函数
# 特点：不修改原函数代码，还能添加功能；只能在原函数运行之前或者之后添加，不能在原函数运行一半时添加
# 实现过程：1.将原函数的引用当做实参传递到闭包 2.修改原函数的指向为闭包中的内部函数
# 功能
# 	引入日志
# 	函数执行时问统计
# 	执行函数前预备处理
# 	执行函数后清理功能
# 	权限校验等场景
# 	缓存

# 案例1: 无参函数的装饰器
def time_func_1(func):
    def wrapper_func():
        print("%s被调用，开始调用时间: %s" % (func.__name__, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        func()
        print("%s被调用，结束调用时间: %s \n" % (func.__name__, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    return wrapper_func


@time_func_1  # 使用装饰器time_func_1进行装饰，等价于foo_1 = time_func(foo_1)
def foo_1():
    print("本体函数被调用")


foo_1()  # 相对于调用wrapper_func函数


# 案例2: 有参函数的装饰器
# 1．如果被装饰的函数有2个参数，那么在定义闭包的时候，就需要在内部函数中，要有2个形参变量
# 2．当调用原函数的时候，实参会传递到 闭包中的内部函数的 形参变量中，在内部函数执行的时候 将这些数据 当做实参 传递到原函数中
def time_func_2(func):
    def wrapper_func(a, b):
        print("a:", a, "b:", b)
        print("%s被调用，开始调用时间: %s" % (func.__name__, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        func(a, b)
        print("%s被调用，结束调用时间: %s \n" % (func.__name__, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    return wrapper_func


@time_func_2  # 使用装饰器time_func_2进行装饰，等价于foo_2 = time_func(foo_2)
def foo_2(a, b):
    print("本体函数被调用")


foo_2(1, 3)


# 案例3: 通用装饰器，可以对有参数、无参数、有返回值、无返回值的函数装饰
def time_func_3(func):
    def wrapper_func(*args, **kwargs):
        print(args, kwargs)
        print("%s被调用，开始调用时间: %s" % (func.__name__, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        ret = func(*args, **kwargs)
        print("%s被调用，结束调用时间: %s \n" % (func.__name__, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        return ret

    return wrapper_func


@time_func_3
def foo_4():
    print("无参数-本体函数被调用")


foo_4()


@time_func_3
def foo_3(a, b):
    print("有参数-本体函数被调用")


foo_3(1, 3)


@time_func_3
def foo_5():
    print("有返回值-本体函数被调用")
    return 1, 2, 3


foo_5()


# 案例4: 多层装饰器
# 装饰器叠加执行顺序：从内到外
# 执行到@make_bold，发现下一行并不是函数所以暂停执行，而是让下面的装饰器@make_italic先执行
def make_bold(func):
    def wrapper():
        return "<b>" + func() + "</b>"

    return wrapper


def make_italic(func):
    def wrapper():
        return "<i>" + func() + "</i>"

    return wrapper


@make_bold
@make_italic
def hello():
    return "Hello, World!"


print(hello())  # <b><i>Hello, World!</i></b>


# 案例5: 闭包与装饰器的区别
# 总结：如果将闭包用作装饰器，那么在闭包中 内部函数里面，是将外部函数中的变量，当做函数来调用
# 定义闭包
def who(name):
    def call(content):
        print("%s: %s" % (name, content))

    return call


zhangsan = who("zhangsan")
zhangsan("Hello, lisi!")
lisi = who("lisi")
lisi("Hello, zhangsan!")


# 定义装饰器
def log(func):
    def call():
        ret = func()
        return ret

    return call


@log
def foo():
    return "Hello, World!"


print(foo())


# 案例6: 装饰器的执行顺序
# @check_login这个装饰器对f1装饰的时间 不是 因为f1（）的调用，而是在Python解释器从上向下解析到第12行的时候就会执行，即开始装饰
def check(func):
    print("-----1----")

    def wrapper():
        print("-----2----")
        func()
        print("-----3----")

    print("-----4----")
    return wrapper


@check
def test():
    print("-----5----")


test()


# 案例7: 带参数的装饰器
def call_out2(timeout=0):
    def call_out1(func):
        def call():
            print("-----1----")
            time.sleep(timeout)
            ret = func()
            print("-----2----")
            return ret

        return call

    return call_out1


# 装饰过程
# 1.执行call_out2=call_out2(2)，得到的返回值call_out1
# 2.此时会执行call_out1(print_hello),得到的返回值call
# 3.将第2步得到的返回值call赋值给print_hello

@call_out2(timeout=2)
def print_hello():
    print("Hello, World!")
    return "OK"


print(print_hello())


# 案例8: 类当作装饰器
class Test(object):
    def __init__(self, func):
        print("-----初始化----")
        print("func: %s" % func.__name__)
        self.__func = func

    def __call__(self, *args, **kwargs):
        print("-----装饰器功能----")
        self.__func()


# 说明：
# 1 当用Test来装作装饰器对test函数进行装饰的时候，首先会创建Test的实例对象，并且会把test这个函数名当做参数传递到__init__方法中
# 2 test指向了用Test创建出来的实例对象
# 3 当在使用test（）进行调用时，就相当于直接调用实例对象，因此会调用这个对象的__call__方法
# 4 为了能够在__call__方法中调用原来test指向的函数体，所以在__init__方法中就需要一个实例属性来保存这个函数体的引用，所以才有了self.__func = func这句代码

@Test  # 等价于test = Test(test)
def test():
    print("hello")


test()  # 如果把这句话注释，重新运行程序，依然会看到“—-初始化一-”


# 案例9: 有参数类当作装饰器
class Test(object):
    def __init__(self, num):
        print("-----__init__----")
        self.__num = num

    def __call__(self, func):
        print("-----__call__----")
        self.__func = func
        return self.call_old_func

    def call_old_func(self):
        print("-----开始调用装饰器中的功能1----")
        self.__func()
        print("-----开始调用装饰器中的功能2----")


@Test(10)  # 等价于print_hello = Test(10)(print_hello)
def print_hello():
    print("hello")


print_hello()
