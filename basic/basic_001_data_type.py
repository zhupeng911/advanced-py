# 技术点：基础数据类型+运算符+字符串
# 1. 基础数据类型
name = "LabEx"  # str: 字符串
age = 10  # int: 整数
pi = 3.14159  # float: 浮点数
is_active = True  # bool: 布尔值 (True/False)
nothing = None  # NoneType: 表示“无值”或“空”
correlate = 2 + 3j  # complex: 复数
print(f'name: {name}, age: {age}, pi: {pi}, is_active: {is_active}, nothing: {nothing}, correlate: {correlate}')
print(
    f'type(name): {type(name)}, type(age): {type(age)}, type(pi): {type(pi)}, type(is_active): {type(is_active)}, type(nothing): {type(nothing)}, type(correlate): {type(correlate)}')

# 2. 运算符
# 算术运算符
a, b = 10, 3
print(f"整除: {a // b}")  # 3 (丢弃余数)
print(f"取模: {a % b}")  # 1 (余数)
print(f"幂运算: {a ** b}")  # 1000 (10的3次方)

# 增强赋值运算符
a += b  # 等价于 a = a + b
a -= b  # 等价于 a = a - b
a *= b  # 等价于 a = a * b
a /= b  # 等价于 a = a / b
a //= b  # 等价于 a = a // b
a %= b  # 等价于 a = a % b
a **= b  # 等价于 a = a ** b

# 海象运算符
print(my_var := "Hello World!")

# 逻辑运算符
is_admin = True
is_logged_in = True
print(f"is_admin and is_logged_in: {is_admin and is_logged_in}")
print(f"is_admin or is_logged_in: {is_admin or is_logged_in}")
print(f"not is_admin: {not is_admin}")
is_valid = 5 < a <= 15  # True 链式比较
print(f"is_valid: {is_valid}")

# 4. 字符串
text = "Python Programming"
print(text[0:6])  # "Python" (切片: [起始:结束])
print(text[::-1])  # "gnimmargorP nohtyP" (反转字符串)
print(f"大写: {text.upper()}")  # 格式化字符串 f-string

# 原始字符串（r 前缀）：将反斜杠视为字面字符
print(r"Hello there!\nHow are you?\nI\'m doing fine.")  # \n 按字面意思打印

# 多行字符串
multiply_text = """
    Dear Alice,
    Eve's cat has been arrested for catnapping,
    cat burglary, and extortion.
    Sincerely,
    Bob
"""
print(multiply_text)

# 字符串操作
spam = 'hello world!'
print(spam[0])
print(spam[1:3])
print(spam[-1])
print("Hello" in spam)
print("world" not in spam)
print(spam.upper())
print(spam.lower())
print(spam.title()) # 将字符串中每个单词的首字母大写，其余字母小写

print(spam.isalpha())  # 如果字符串仅由字母组成，则返回 True
print(spam.isalnum())  # 如果字符串仅由字母和数字组成，则返回 True
print(spam.isdecimal())  # 如果字符串仅由数字组成，则返回 True
print(spam.isspace())  # 如果字符串仅由空格组成，则返回 True
print(spam.startswith('hello'))
print(spam.endswith('world'))

# join: 接受可迭代对象（如 列表、字典、元组 或 集合）中的所有项，并将它们连接成一个字符串
name = ["Alice", "Bob", "Charlie"]
print(''.join(name))
print('-'.join(name))
print(','.join(name))

# split: 将一个 string 分割成一个 list
spam_str = spam.split(' ')
print(spam_str)
print('My,name,is,Simon'.split(','))

spam2 = '    Hello World     '
print(spam2.strip())  # 去除两端空格
print(spam2.lstrip())  # 去除左端空格
print(spam2.rstrip())  # 去除右端空格

print(spam2.count('H'))  # 统计字符 'H' 出现的次数
print(spam2.upper().count('H'))  # 统计字符 'H' 出现的次数,忽略大小写

print(spam2.replace('Hello', 'Hi'))

# 格式化
name = 'Alice'
age = 23
score = 95.51
num = 1230991

print(f'{num:,}')  # 千分位
print(f'{score:.2f}')  # 四舍五入
print(f'{score:.2%}')  # 百分比
print(f'{age:#x}')  # 十六进制

# % 不推荐
print("name:%s" % name)
print("age:%d" % age)

# str.format() 推荐
print("name:{}".format(name))
print("age:{}".format(age))
print('name: {}, age: {}, score: {}'.format(name, age, score))

# f-string (Python 3.6+) 推荐
print(f'name: {name}, age: {age}, score: {score}')
print(f'name: {name}, age: {age}, score: {score:.1f}')

print('不换行', end=',')
print('不换行', end='')
print()
