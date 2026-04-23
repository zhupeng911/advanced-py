# 案例1: 简单计算器模块
# 涉及语法: 函数定义、条件语句、异常处理
import functools
import time


def calculate(num1, num2, op):
    try:
        if op == '+':
            return num1 + num2
        elif op == '-':
            return num1 - num2
        elif op == '*':
            return num1 * num2
        elif op == '/':
            if num2 == 0:
                raise ValueError('Cannot divide by 0')  # 抛出内置的异常
            return num1 / num2
        else:
            raise ValueError('Invalid operation')
    except Exception as e:
        print(e)
        return None


# 案例2: 文件读写与数据处理 todo
# 涉及语法:文件操作、列表推导式、上下文管理器
def read_and_process_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file if line.strip()]
            numbers = [int(line) for line in lines if line.isdigit()]
            return numbers
    except FileNotFoundError:
        print(f"文件 {filename} 不存在")
        return []


def write_result(filename, data):
    """写入处理结果"""
    with open(filename, 'w', encoding='utf-8') as file:
        for item in data:
            file.write(f"{item}\n")


# 案例3: 面向对象编程 - 银行账户系统
# 涉及语法: 类定义、继承、封装、多态
class Account:
    def __init__(self, account_number, balance):
        self._account_number = account_number  # 受保护的属性，本类以及子类可见
        self.__balance = balance  # 私有属性，仅本类可见

    def get_balance(self):
        return self.__balance

    # 账户存钱
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        else:
            return False

    # 账户取钱
    def withdraw(self, amount):
        if self.__balance >= amount:
            self.__balance -= amount
            return True
        else:
            return False


# 子类，新增字段rate
class SavingAccount(Account):
    def __init__(self, account_number, balance, rate):
        super().__init__(account_number, balance)
        self.__rate = rate

    # 计算利息
    def add_interest(self):
        # interest = self.__rate * self.__balance 私有属性__balance子类无法直接访问
        interest = self.__rate * self.get_balance()
        self.deposit(interest)
        return interest


# 案例4: 装饰器应用 - 性能监控
# 涉及语法:装饰器、闭包、functools
# 计算函数执行耗时
def timer(func):
    @functools.wraps(func)  # 通过闭包实现装饰器时, 解决元数据丢失问题
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 执行时间: {end_time - start_time:.4f}秒")
        return result

    return wrapper


# 接口重试
def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    time.sleep(delay)
            return None

        return wrapper

    return decorator


@retry(max_attempts=3, delay=1)
@timer
def testTimer():
    print("testTimer")


# 案例5: 生成器与迭代器
# 涉及语法:生成器函数、yield、迭代器协议
def fibonacci_generator(n):
    """斐波那契数列生成器"""
    a, b = 0, 1
    for i in range(n):
        yield a
        a, b = b, a + b


def file_line_generator(filename):
    """文件行生成器"""
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.strip()

if __name__ == '__main__':
    # 案例1
    print(calculate(10, 20, '+'))
    print(calculate(10, 20, '-'))
    print(calculate(10, 20, '+'))
    print(calculate(10, 0, '/'))

    # 案例3
    account1 = Account("zhupeng", 100)
    account1.deposit(10)
    print(account1.get_balance())
    account1.withdraw(10)
    print(account1.get_balance())

    account2 = SavingAccount("zhupeng", 100, 0.1)
    print(account2.get_balance())
    account2.add_interest()
    print(account2.get_balance())

    # 案例4
    testTimer()

    # 案例5
    print(fibonacci_generator(10))
