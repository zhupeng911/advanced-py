# Python 魔法函数（Magic Methods / Dunder Methods）核心常用版
# 魔法函数：以双下划线开头和结尾的特殊方法，由 Python 解释器在特定场景自动调用
# 涉及：对象生命周期、字符串表示、比较运算、算术运算、容器协议、可调用对象、上下文管理器、属性访问


# ==================== 1. 对象生命周期：__init__ / __new__ / __del__ ====================
# cls与self区别
# 1.名字不是强制的，self/cls 只是约定俗成
# 2.self：指代调用者是当前对象实例，即 book；
# 3.cls：指代调用者是当前类，即 Book
class Book:
    """演示对象的创建、初始化和销毁过程"""

    def __new__(cls, *args, **kwargs):
        # __new__ 在 __init__ 之前调用，负责创建实例（返回类的实例）
        # 一般不需要重写，单例模式/不可变对象会用到
        print(f'[__new__] 创建 {cls.__name__} 实例')
        instance = super().__new__(cls)
        return instance

    # PS：Python实例属性不需要提前声明-赋值即创建，self.title = title本身就是在 "创造" 这个属性
    def __init__(self, title, price):
        # __init__ 在实例创建后调用，负责初始化属性
        print(f'[__init__] 初始化 Book: {title}')
        self.title = title
        self.price = price

    def __del__(self):
        # __del__ 在对象被垃圾回收时调用（不保证立即触发）
        print(f'[__del__] 销毁 Book: {self.title}')


# ==================== 2. 字符串表示：__str__ / __repr__ ====================
class User:
    """演示对象的两种字符串表示"""

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        # __str__ 面向用户，由 print() / str() 触发，要求可读
        return f'用户 {self.name}（{self.age} 岁）'

    def __repr__(self):
        # __repr__ 面向开发者，由 repr() / 解释器直接显示触发，要求无歧义
        # 一般应能通过 eval(repr(obj)) 重建对象
        return f"User(name='{self.name}', age={self.age})"


# ==================== 3. 比较运算：__eq__ / __lt__ / __hash__ ====================
class Score:
    """演示比较运算符重载，使对象可比较、可排序、可哈希"""

    def __init__(self, subject, value):
        self.subject = subject
        self.value = value

    def __eq__(self, other):
        # == 运算符：判断两个分数是否相等
        if not isinstance(other, Score):
            return NotImplemented
        return self.value == other.value

    def __lt__(self, other):
        # < 运算符：定义后可使用 sorted() 排序
        if not isinstance(other, Score):
            return NotImplemented
        return self.value < other.value

    def __hash__(self):
        # 重写 __eq__ 后需要重写 __hash__，否则对象不能放入 set/dict 的 key
        return hash((self.subject, self.value))

    def __repr__(self):
        return f'Score({self.subject}={self.value})'


# ==================== 4. 算术运算：__add__ / __sub__ / __mul__ ====================
class Vector:
    """演示算术运算符重载（二维向量）"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        # + 运算符：向量相加
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        # - 运算符：向量相减
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, scalar):
        # * 运算符：向量乘以标量
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        return NotImplemented

    def __repr__(self):
        return f'Vector({self.x}, {self.y})'


# ==================== 5. 容器协议：__len__ / __getitem__ / __setitem__ / __contains__ ====================
class MyList:
    """演示自定义容器，支持 len() / 索引 / in 运算符"""

    def __init__(self, items=None):
        self._items = list(items) if items else []

    def __len__(self):
        # len() 触发
        return len(self._items)

    def __getitem__(self, index):
        # obj[index] 读取触发，支持 for 循环遍历
        return self._items[index]

    def __setitem__(self, index, value):
        # obj[index] = value 触发
        self._items[index] = value

    def __contains__(self, item):
        # in 运算符触发
        return item in self._items

    def __repr__(self):
        return f'MyList({self._items})'


# ==================== 6. 可调用对象：__call__ ====================
class Counter:
    """演示让实例像函数一样被调用"""

    def __init__(self, start=0):
        self.count = start

    def __call__(self, step=1):
        # 实例() 触发，相当于 instance.__call__()
        self.count += step
        return self.count


# ==================== 7. 上下文管理器：__enter__ / __exit__ ====================
class FileOpener:
    """演示自定义 with 语句，自动管理资源"""

    def __init__(self, filename, mode='r'):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        # 进入 with 块时调用，返回值赋给 as 后的变量
        print(f'[__enter__] 打开文件 {self.filename}')
        self.file = open(self.filename, self.mode, encoding='utf-8')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 退出 with 块时调用（无论是否异常），用于清理资源
        # 返回 True 会吞掉异常，返回 False/None 会传播异常
        print(f'[__exit__] 关闭文件 {self.filename}')
        if self.file:
            self.file.close()
        return False


# ==================== 8. 属性访问：__getattr__ / __setattr__ ====================
class Config:
    """演示动态属性访问，类似字典但支持点号语法"""

    def __init__(self):
        # 注意：这里赋值会触发 __setattr__，所以用 object.__setattr__ 绕过
        object.__setattr__(self, '_data', {})

    def __getattr__(self, name):
        # 只有访问不存在的属性时才触发（区别于 __getattribute__）
        if name in self._data:
            return self._data[name]
        raise AttributeError(f'Config 没有属性: {name}')

    def __setattr__(self, name, value):
        # 任何属性赋值都会触发，包括 self.x = 1
        self._data[name] = value

    def __repr__(self):
        return f'Config({self._data})'


# ==================== 运行演示 ====================
if __name__ == '__main__':
    print('---------- 1. 对象生命周期 ----------')
    book = Book('Python 编程', 59.0)
    del book  # 主动触发销毁

    print('\n---------- 2. 字符串表示 ----------')
    user = User('zhupeng', 23)
    print(str(user))  # __str__ -> 用户 zhupeng（23 岁）
    print(repr(user))  # __repr__ -> User(name='zhupeng', age=23)

    print('\n---------- 3. 比较运算 ----------')
    s1 = Score('数学', 90)
    s2 = Score('英语', 90)
    s3 = Score('语文', 80)
    print(s1 == s2)  # True
    print(s1 < s3)  # False
    print(sorted([s1, s2, s3]))  # 按 value 升序
    print({s1, s2, s3})  # 可放入 set

    print('\n---------- 4. 算术运算 ----------')
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    print(v1 + v2)  # Vector(4, 6)
    print(v2 - v1)  # Vector(2, 2)
    print(v1 * 3)  # Vector(3, 6)

    print('\n---------- 5. 容器协议 ----------')
    ml = MyList([10, 20, 30])
    print(len(ml))  # 3
    print(ml[1])  # 20
    ml[1] = 99
    print(20 in ml)  # False
    print(99 in ml)  # True
    for item in ml:  # 依赖 __getitem__ 实现迭代
        print(item, end=' ')
    print()

    print('\n---------- 6. 可调用对象 ----------')
    counter = Counter()
    print(counter())  # 1
    print(counter())  # 2
    print(counter(10))  # 12

    print('\n---------- 7. 上下文管理器 ----------')
    # 示例：with FileOpener('test.txt', 'w') as f:
    #          f.write('hello')
    # 这里仅演示语法，不实际写文件
    print('用法：with FileOpener("path") as f: ...')

    print('\n---------- 8. 属性访问 ----------')
    cfg = Config()
    cfg.host = 'localhost'  # 触发 __setattr__
    cfg.port = 8080
    print(cfg.host)  # 触发 __getattr__ -> localhost
    print(cfg.port)  # 8080
    print(cfg)  # Config({'host': 'localhost', 'port': 8080})
