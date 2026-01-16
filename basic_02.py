class Student:
    # 公有属性
    name = ''
    age = 0
    # 私有属性
    __score = 0

    # 构造方法
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.__score = score

    # 普通方法
    def speak(self):
        print("%s 说: 我 %d 岁。" % (self.name, self.age))
        print("成绩: %d" % self.__score)

    # 私有方法
    def __getScore(self):
        return self.__score


# 1.函数-默认值参数
def ask_ok(prompt, retries=4, reminder='Please try again!'):
    while True:
        ok = input(prompt)
        if ok in ('y', 'ye', 'yes'):
            return True
        if ok in ('n', 'no', 'nop', 'nope'):
            return False
        retries = retries - 1
        if retries < 0:
            raise ValueError('invalid user response')
        print(reminder)


if __name__ == '__main__':
    # stu = Student("zhupeng", 23, 100)
    # print(stu.name)
    # print(stu.age)
    # stu.speak()
    ask_ok('请输入提示词')
    ask_ok('请输入提示词', 3)
    ask_ok('请输入提示词', 5, '请重新输入')
