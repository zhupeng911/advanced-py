# 函数：解包、闭包

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
# 定义：如果一个函数内部嵌套定义了另一个函数，并且内部函数引用了外部函数的局部变量或形参，那么这个内部函数以及用到的外部函数中的变量就被称为闭包
# 三要素：1. 外部函数嵌套定义内部函数 2. 内层函数引用了外部函数的局部变量或形参 3. 外部函数返回了内层函数的引用
def person(name):  # 外部函数
    num = 100  # 局部变量

    def say(content):  # 内部函数
        return name + " says " + content  # 引用了外部函数的变量name

    return say  # 返回内部函数


alice = person('Alice')
bob = person('Bob')
alice('Hello')  # Alice says Hello
bob('Hi')  # Bob says Hi


# 案例1：
def test(number):
    def test_in(number_in):
        return number + number_in

    return test_in


# 给test函数赋值，这个20就是给参数number
ret = test(20)
# 注意这里的100其实给参数number_in
print(ret(100))
# 注意这里的100其实给参数number_i
print(ret(200))


# 说明：
# 1.正常来说，调用一个函数的时候，这个函数中的所有局部变量+形参 都只会在这个函数执行的过程中才会保留，只要这个函数 执行完毕，那么这些局部变量+形參就会被自动释放。
# 2. 闭包比普通函数强大的地方在于，它在外部函数执行完毕之后，这个外部函数中所有局部变量+形參，都不会被释放，以便于在 调用内部函数的时候
# 可以使用
#
# 闭包的好处：可以将局部变量 永久存儲存储
# 坏处：占用内存
# 	如果调用了100次的闭包函数，那么意味着 创建了100个 闭包，占用了大量的无用内存
# 	如果调用了100次的普通函数，那么意味着 调用100次函数时 申请了100次空间，然后又释放了100次空间，不会占用大量内存


# 案例2：nonlocal闭包中修改外部函数中变量的值
def counter(start=0):
    def add_one():
        nonlocal start  # 添加nonlocal 可以让start在闭包中的内部函数进行修改，否则会产生异常
        start += 1  # 在闭包中的 内部函数中，如果没有用特殊的关键字来 声明 外部函数中的变量，则不能对其进行修改
        return start

    return add_one


c1 = counter(5)  # 创建一个闭包
print(c1())
print(c1())

c2 = counter(50)  # 再创建一个闭包
print(c2())
print(c2())

# 上面已经创建了2个闭包，下面的代码故意再次对C1/C2进行调用，检测 是否会因为 第二次创建闭包 导致第一次创建的闭包 失效，结果发现 没有任何影响
# 说明了一个道理：可以创建多个闭包，多个闭包之间没有任何关系
print(c1())
print(c1())
print(c2())
print(c2())


# 感觉闭包与对象有些类似，对象其实可通俗的理解为数据（属性）+功能（方法），闭包也可以理解为数据+功能，只不过此时数据是外部函数中的那些局部变量或者形参，而功能则是内部函数。
# 对象适合完成较为复杂的功能，而闭包则更轻量
# 对象：可以由N个属性 + N个方法组成
# 闭包：可以由N个变量 +1个函数组成（当然也可以有N个函数，但是一般 只会写一个）

def line_conf(a, b):
    def line(x):
        return a * x + b

    def line2(x):
        return 2 * a * x + 2 * b

    return line, line2


line, line2 = line_conf(1, 2)
print(line(5))
print(line2(5))
