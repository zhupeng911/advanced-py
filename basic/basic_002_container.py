# 技术点：四大容器
# 列表List: 有序、可变（可以增删改）、允许重复
#    students = ['alice', 'bob', 'red', 'cat']
#
# 元组Tuple: 不可变的列表,有序、不可变、允许重复
#     names = ("Alice", "Bob")
#
# 集合Set：去重神器,无序、可变、不允许重复
#     tags = {"python", "java", "python", "c++"}
#
# 字典Dictionary：键值对,键（Key）必须唯一且不可变，值（Value）可以任意
#     user = {"name": "Gemini", "age": 1, "city": "Mountain View"}

def basic_container():
    # 1.列表List，有序、可变（可以增删改）、允许重复
    students = ['alice', 'bob', 'red', 'cat']

    # 增
    students.append('alice')
    students.insert(5, 'alice')
    # 删
    del students[0]
    students.remove('bob')
    # 改
    students[0] = 'alice22'
    # 查
    print(students)
    print(students[1:2])  # 使用切片获取子列表
    print(students[:2])  # 返回前两个元素
    print(students[1:])  # 返回从第二个元素开始到末尾的所有元素
    print(students[:])  # 返回所有元素
    print(students[0])
    print(students[-1])  # 返回最后一个元素
    print(len(students))  # 返回列表长度
    print('alice' in students)
    print('alice' not in students)
    print(students.count('alice'))  # 出现次数
    print(students.index('alice'))  # 首次出现下标,如果没有会报错

    # 遍历
    for stu in students:
        print(stu)
    for i in range(len(students)):
        print(students[i])

    # 拼接
    teachers = ['alice', 'bob', 'red', 'cat']
    all = students + teachers
    print(all)

    # zip,在多个列表中循环
    for stu, tea in zip(students, teachers):
        print(stu)
        print(tea)

    # 排序
    scores = [100, 78, 78, 67, 90]
    scores.sort()
    print(scores)
    print(len(scores))
    print(max(scores))
    print(min(scores))
    print(sum(scores))
    scores.reverse()  # 反向列表中元素
    scores.sort(key=None, reverse=True)  # 对原列表进行排序

    # 2.元组Tuple，不可变的列表、有序、允许重复
    tuple1 = (1, 2, 3, 4, 5)
    # 不支持增、删、改
    # 查
    print(tuple1)
    print(tuple1[0:2])
    print(tuple1[1:3])
    print(tuple1[2:4])
    print(tuple1[:2])

    # 类型转换
    names = ['alice', 'bob', 'red', 'cat']
    tuple2 = tuple(names)
    print(tuple2)
    list2 = list(tuple2)
    print(list2)

    # 3.集合Set，去重神器,无序、可变、不允许重复
    set1 = {1, 2, 3, 3, 4, 1}  # 使用花括号
    # 增
    set1.add(6)
    # 删
    set1.remove(1)  # 如果值不存在，remove() 会引发 key error。
    set1.discard(2)  # 移除元素(安全，缺失时不报错)
    # 改
    set1.update({4, 5})
    set1.update([4, 5])
    # 查
    print(set1)
    print(len(set1))
    print(set1.pop())
    print(1 in set1)
    # 遍历
    for item in set1:
        print(item)

    # 集合运算
    set2 = set("abcde")
    set3 = set("defgh")
    print(set2 - set3)  # 集合a中包含而集合b中不包含的元素
    print(set2 | set3)  # 集合a或b中包含的所有元素
    print(set2 & set3)  # 集合a和b中都包含了的元素
    print(set2 ^ set3)  # 不同时包含于a和b的元素

    # 4.字典map：键值对,键（Key）必须唯一且不可变，值（Value）可以任意
    stuInfo = {
        "name": "zhangsan",
        "age": 23
    }
    # 增
    stuInfo.setdefault("city", "上海")
    # 删
    del stuInfo["name"]
    stuInfo.pop("name")
    # del stuInfo
    # 改
    stuInfo["age"] = 24
    # 查
    print(stuInfo)
    print(stuInfo["name"])
    print(len(stuInfo))
    print(stuInfo.keys())
    print(stuInfo.values())
    print(stuInfo.items())
    print("name" in stuInfo.keys())  # 判断键是否存在'
    print("zhupeng" in stuInfo.values())  # 判断值是否存在

    # 遍历
    for key in stuInfo.keys():
        print(key, stuInfo[key])

    for key, value in stuInfo.items():
        print(key, value)

    # 类型转换
    str = '123123'
    list_str = list(str)
    set_str = set(str)
    print(list_str)
    print(set_str)


# 3.基本逻辑控制语句
def basic_logic_control():
    # if相关
    num = int(input("input a number: "))
    if num % 2 == 0:
        if num % 3 == 0:
            print("你输入的数字可以整除 2 和 3")
        else:
            print("你输入的数字可以整除 2，但不能整除 3")
    else:
        if num % 3 == 0:
            print("你输入的数字可以整除 3，但不能整除 2")
        else:
            print("你输入的数字不能整除 2 和 3")

    age = int(input("请输入你家狗狗的年龄: "))
    if age <= 0:
        print("你是在逗我吧!")
    elif age == 1:
        print("相当于 14 岁的人。")
    elif age == 2:
        print("相当于 22 岁的人。")
    elif age > 2:
        human = 22 + (age - 2) * 5
        print("对应人类年龄: ", human)

    # 循环
    count = 1
    sum = 0
    while count <= 100:
        sum += count
        count += 1
    else:
        print(count, "大于100，结束")
    print(sum)

    for n in range(2, 10):
        for x in range(2, n):
            if n % x == 0:
                print(n, 'equals', x, '*', n // x)
                break
        else:  # 与if语句相比，循环的else子句更像try的else子句
            print(n, 'is a prime number')

    for x in range(5, 10):
        if x % 2 == 0:
            print("找到偶数: ", x)
            continue
        print(x)

    # pass 语句:pass 语句不执行任何操作
    # match语句


from datetime import datetime, timedelta, date


def basic_date_format():
    # 1.标准datetime 年 月 日 时 分 秒
    now = datetime.now()
    print("now:", now)
    print("年:", now.year, "月:", now.month, "日:", now.day)
    print("时:", now.hour, "分:", now.minute, "秒:", now.second)

    one_year_later = now + timedelta(days=365)
    print("one_year_later:", one_year_later)
    one_day_later = now + timedelta(days=1)
    print("one_day_later:", one_day_later)
    one_hour_before = one_day_later - timedelta(hours=1)
    print("one_hour_before:", one_hour_before)

    # 字符串->时间
    date_time_str = "2023-04-01 12:00:00"
    date_time_format = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    print("date_format:", date_time_format)

    date_one_year_later = date_time_format + timedelta(days=365)
    print("date_one_year_later:", date_one_year_later)

    # 2.标准date
    today = date.today()
    today2 = datetime.now().date()
    print("today:", today)
    print("today2:", today2)
    print("年:", today.year, "月:", today.month, "日:", today.day)
    one_day_later = today + timedelta(days=1)
    print("one_day_later:", one_day_later)
    one_day_before = today - timedelta(days=1)
    print("one_day_before:", one_day_before)

    date_str = "2023-04-01"
    date_format = date.strptime(date_str, "%Y-%m-%d")
    print("date_format:", date_format)


if __name__ == '__main__':
    basic_container()
    basic_logic_control()
    basic_date_format()
