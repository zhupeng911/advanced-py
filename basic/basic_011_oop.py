# 类
# 涉及语法: 类属性、实例属性、类方法、静态方法、property、__str__、__repr__、__slots__、运算符重载
# 封装
class Student:
    # ----------1.类属性与类方法----------
    # 类公有属性: 外部可用
    school_name = '苏州大学'

    # 类受保护属性: 外部可访问，但约定不要访问
    _count = 0

    # 类私有属性: 外部无法访问
    __sex = False

    @classmethod
    def create_default_student(cls, name):
        return cls(name, 20, 80)

    @classmethod
    def get_student_count(cls):
        return cls._count

    # ----------2.实例属性与实例方法----------
    # __slots__限制实例能拥有的属性（节省内存、防止随意添加属性，只能有这三个属性）
    __slots__ = ('_name', '_age', '_score', '_id')

    # 构造方法： 给实例属性赋值
    def __init__(self, name, age, score):
        self._name = name
        self._age = age
        self._score = score
        self._id = Student._count
        Student._count += 1

    def introduce(self):
        print("姓名: {}，年龄: {}，成绩: {}".format(self._name, self._age, self._score))

    def if_pass_exam(self, threshold=60):
        return self._score >= threshold

    # ---------- 3.静态方法 ----------
    @staticmethod
    def is_adult(age):
        return age >= 18

        # ----------4.property 装饰器----------

    # ---------- 让你像访问属性一样调用方法，同时保留对读写的控制权
    # 类似于java的set get
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not name:  # value 为空字符串、None、0 等
            raise ValueError('姓名不能为空')
        self._name = name

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        if age < 0:
            raise ValueError('年龄不能为负数')
        self._age = age

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        if not 0 <= score <= 100:
            raise ValueError('成绩不能为负数')
        else:
            self._score = score

    # ---------- 5.运算符重载 ----------
    def __eq__(self, other):
        if isinstance(other, Student):
            return self._name == other._name and self._age == other._age
        return False

    def __str__(self):
        """供 print() 或 str() 调用"""
        return f'Student({self._name}, age={self._age}, score={self._score})'

    def __repr__(self):
        """供 repr() 调用或调试时显示"""
        return f"Student(name='{self._name}', age={self._age}, score={self._score})"

    # 运算符重载
    def __add__(self, other):
        if isinstance(other, Student):
            return self._score + other._score
        return NotImplemented


# 类属性访问/类方法调用
print(Student.school_name)  # 输出:  苏州大学
print(Student._count)  # 输出:  0，不推荐
print(Student.__sex)  # 报错，外部无法访问，AttributeError
print(Student.create_default_student("Alice"))  # 类方法创建默认学生
print(Student.get_student_count())  # 输出:  3
print(Student.is_adult(90))  # 静态方法

# 创建实例
s1 = Student("zhupeng", 23, 100)
s2 = Student("zhucaixai", 22, 99)
s3 = Student.create_default_student("Alice")
print(s1.introduce())  # 输出: 姓名: zhupeng，年龄: 23，成绩: 100
print(s1.if_pass_exam())  # 输出:  True

# property 装饰器
print(s1.name)  # 输出: zhupeng
print(s1.age)  # 输出: 23
print(s1.score)  # 输出: 100

# 运算符重载
print(s1)  # __str__
print(repr(s1))  # __repr__
print(s1 == s2)  # __eq__
print(s1 + s2)  # __add__ 成绩相加


# 继承
class StudentWithSubject(Student):
    """继承 Student，新增学科属性"""

    def __init__(self, name, age, score, subject):
        super().__init__(name, age, score)
        self._subject = subject

    # 方法重写
    def introduce(self):
        return f'{super().introduce()}，专业是{self._subject}'


# 继承类
s4 = StudentWithSubject('David', 21, 88, '计算机')
print(s4.introduce())
print(isinstance(s1, Student))
print(issubclass(StudentWithSubject, Student))


# 多态
# 多态性是通过使用方法覆盖或方法重载来实现的
# 方法覆盖是指子类提供对父类中已定义方法的自己实现。这允许子类在不更改方法名称或签名的情况下修改方法的行为。
# 方法重载是指多个方法具有相同的名称但参数不同。Python 不直接支持方法重载，但可以通过使用默认参数或可变长度参数来实现。
class Shape:
    def area(self):
        pass


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius  # 初始化 radius 实例变量

    def area(self):
        return 3.14 * self.radius ** 2  # 使用 pi * r^2 返回圆的面积


shapes = [Rectangle(4, 5), Circle(7)]
for shape in shapes:
    print(shape.area())
